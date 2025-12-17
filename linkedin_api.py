"""
LinkedIn Job Search API Client using RapidAPI
"""
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import streamlit as st


class LinkedInJobAPI:
    """Client for LinkedIn Job Search API via RapidAPI"""
    
    def __init__(self):
        """Initialize API client with credentials from Streamlit secrets"""
        try:
            self.api_key = st.secrets["rapidapi"]["key"]
            self.api_host = st.secrets["rapidapi"]["host"]
        except Exception as e:
            st.error(f"Error loading API credentials: {e}")
            self.api_key = None
            self.api_host = None
        
        # LinkedIn Job Search API endpoint - correct path from RapidAPI playground
        if not self.api_host:
            self.base_url = "https://linkedin-job-search-api.p.rapidapi.com/active-jb-7d"
        else:
            self.base_url = f"https://{self.api_host}/active-jb-7d"
    
    def search_sap_jobs(
        self,
        days_back: int = 7,
        location: Optional[str] = None,
        remote: Optional[bool] = None,
        limit: int = 100,
        offset: int = 0,
        include_text: bool = True
    ) -> Dict:
        """
        Search for SAP jobs on LinkedIn
        
        Args:
            days_back: Number of days back to search (default: 7)
            location: Location filter (e.g., "United States", "New York")
            remote: Filter for remote jobs (True/False/None)
            limit: Maximum number of results per page (default: 100)
            offset: Pagination offset (default: 0)
            include_text: Include full job description (default: True)
        
        Returns:
            Dictionary with job listings and metadata
        """
        if not self.api_key or not self.api_host:
            return {
                "success": False,
                "error": "API credentials not configured",
                "jobs": []
            }
        
        # Calculate posted_after date (7 days ago)
        posted_after = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
        
        # Build query parameters for LinkedIn Job Search API
        # Based on actual RapidAPI curl command
        params = {
            "title_filter": "SAP",  # Search for SAP in job title
            "limit": limit,
            "offset": offset,
            "description_type": "text"  # Get text descriptions
        }
        
        # Add optional filters
        if location and location != "All Locations":
            params["location_filter"] = location
        
        if remote is True:
            params["remote"] = "true"
        
        # Set up headers
        headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": self.api_host
        }
        
        try:
            # Make API request
            response = requests.get(
                self.base_url,
                headers=headers,
                params=params,
                timeout=30
            )
            
            # Check response status
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "jobs": self._parse_jobs(data),
                    "total": len(data) if isinstance(data, list) else 0,
                    "error": None
                }
            elif response.status_code == 429:
                return {
                    "success": False,
                    "error": "Rate limit exceeded. Please wait a moment and try again.",
                    "jobs": []
                }
            else:
                return {
                    "success": False,
                    "error": f"API error: {response.status_code} - {response.text}",
                    "jobs": []
                }
                
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error": "Request timed out. Please try again.",
                "jobs": []
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"Network error: {str(e)}",
                "jobs": []
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}",
                "jobs": []
            }
    
    def _parse_jobs(self, data) -> List[Dict]:
        """
        Parse job data from API response
        
        Args:
            data: Raw API response data
        
        Returns:
            List of parsed job dictionaries
        """
        jobs = []
        
        # Handle different response formats
        if isinstance(data, list):
            job_list = data
        elif isinstance(data, dict) and "jobs" in data:
            job_list = data["jobs"]
        else:
            return jobs
        
        for job in job_list:
            try:
                # Extract location from locations_derived array
                location = "N/A"
                if job.get("locations_derived"):
                    location = ", ".join(job["locations_derived"][:2])  # First 2 locations
                elif job.get("location"):
                    location = job["location"]
                
                parsed_job = {
                    "title": job.get("title", "N/A"),
                    "company": job.get("organization", "N/A"),  # Use 'organization' field
                    "location": location,
                    "posted_date": job.get("date_posted", job.get("posted_at", "N/A")),
                    "description": job.get("description_text", job.get("description", "No description available")),
                    "apply_url": job.get("url", job.get("apply_url", "#")),
                    "type": ", ".join(job.get("employment_type", [])) if job.get("employment_type") else "N/A",
                    "remote": job.get("remote_derived", job.get("remote", False)),
                    "salary": job.get("salary_raw", "Not specified"),
                    "industry": job.get("linkedin_org_industry", "N/A")
                }
                jobs.append(parsed_job)
            except Exception as e:
                # Skip jobs that fail to parse
                continue
        
        return jobs
