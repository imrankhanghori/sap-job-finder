"""
SAP Job Finder - Streamlit Application
Find SAP jobs posted recently on LinkedIn
"""
import streamlit as st
from datetime import datetime
from linkedin_api import LinkedInJobAPI


# Page configuration
st.set_page_config(
    page_title="SAP Job Finder",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    /* Main container styling */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Card styling */
    .job-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
        border-left: 4px solid #667eea;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .job-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 12px rgba(0, 0, 0, 0.15);
    }
    
    .job-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: #1a202c;
        margin-bottom: 0.5rem;
    }
    
    .job-company {
        font-size: 1.1rem;
        color: #4a5568;
        margin-bottom: 0.5rem;
    }
    
    .job-meta {
        font-size: 0.9rem;
        color: #718096;
        margin-bottom: 0.5rem;
    }
    
    .badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
    }
    
    .badge-remote {
        background: #d4edda;
        color: #155724;
    }
    
    .badge-location {
        background: #cce5ff;
        color: #004085;
    }
    
    .badge-type {
        background: #fff3cd;
        color: #856404;
    }
    
    /* Button styling */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    /* Header styling */
    .header-container {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        text-align: center;
    }
    
    .app-title {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .app-subtitle {
        font-size: 1.2rem;
        color: #4a5568;
    }
</style>
""", unsafe_allow_html=True)


def display_job_card(job, index):
    """Display a job in a card format"""
    with st.container():
        remote_badge = "<span class='badge badge-remote'>🌐 Remote</span>" if job.get("remote") else ""

        # Build HTML without any leading indentation so Markdown doesn't
        # interpret it as a code block.
        job_card_html = (
            f"<div class=\"job-card\">"
            f"<div class=\"job-title\">{job['title']}</div>"
            f"<div class=\"job-company\">🏢 {job['company']}</div>"
            f"<div class=\"job-meta\">"
            f"<span class=\"badge badge-location\">📍 {job['location']}</span>"
            f"{remote_badge}"
            f"<span class=\"badge badge-type\">⏰ {job['posted_date']}</span>"
            f"</div>"
            f"</div>"
        )

        st.markdown(job_card_html, unsafe_allow_html=True)
        
        # Expandable description
        with st.expander("📄 View Full Description"):
            st.write(job['description'])
            
            col1, col2 = st.columns([3, 1])
            with col2:
                if job['apply_url'] and job['apply_url'] != "#":
                    st.link_button("Apply Now", job['apply_url'], use_container_width=True)


def main():
    """Main application function"""
    
    # Header
    st.markdown("""
    <div class="header-container">
        <div class="app-title">💼 SAP Job Finder</div>
        <div class="app-subtitle">Find SAP jobs recently posted LinkedIn</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize API client
    api_client = LinkedInJobAPI()
    
    # Sidebar filters
    with st.sidebar:
        st.header("🔍 Search Filters")
        
        # Location filter
        location = st.selectbox(
            "Location",
            ["All Locations", "India", "Mumbai", "Delhi", "Bangalore", "Hyderabad", 
             "Chennai", "Pune", "Kolkata", "Ahmedabad", "Gurugram", "Noida", 
             "Chandigarh", "Jaipur", "Remote"],
            help="Filter jobs by location"
        )
        
        # Remote filter
        remote_only = st.checkbox("Remote Jobs Only", value=False)
        
        # Days back filter
        days_back = st.slider(
            "Posted Within (Days)",
            min_value=1,
            max_value=30,
            value=7,
            help="Filter jobs posted within the last N days"
        )
        
        # Results per page
        results_per_page = st.select_slider(
            "Results Per Page",
            options=[10, 25, 50, 100],
            value=25
        )
        
        st.divider()
        
        # Search button
        search_button = st.button("🔎 Search Jobs", use_container_width=True, type="primary")
    
    # Initialize session state for pagination
    if 'page_offset' not in st.session_state:
        st.session_state.page_offset = 0
    
    if 'search_results' not in st.session_state:
        st.session_state.search_results = None
    
    # Handle search
    if search_button or st.session_state.search_results is not None:
        # Build search parameters
        location_param = None if location == "All Locations" else location
        remote_param = True if remote_only else None
        
        # Show loading state
        with st.spinner("🔍 Searching for SAP jobs..."):
            results = api_client.search_sap_jobs(
                days_back=days_back,
                location=location_param,
                remote=remote_param,
                limit=results_per_page,
                offset=st.session_state.page_offset,
                include_text=True
            )
        
        st.session_state.search_results = results
        
        # Display results
        if results['success']:
            jobs = results['jobs']
            
            if jobs:
                # Results summary
                st.success(f"✅ Found {results['total']} SAP jobs!")
                
                # Display jobs
                for idx, job in enumerate(jobs):
                    display_job_card(job, idx)
                
                # Pagination
                st.divider()
                col1, col2, col3 = st.columns([1, 2, 1])
                
                with col1:
                    if st.session_state.page_offset > 0:
                        if st.button("⬅️ Previous Page", use_container_width=True):
                            st.session_state.page_offset -= results_per_page
                            st.rerun()
                
                with col2:
                    st.markdown(f"<div style='text-align: center; padding: 0.5rem;'>Page {st.session_state.page_offset // results_per_page + 1}</div>", unsafe_allow_html=True)
                
                with col3:
                    if len(jobs) == results_per_page:
                        if st.button("Next Page ➡️", use_container_width=True):
                            st.session_state.page_offset += results_per_page
                            st.rerun()
            else:
                st.warning("⚠️ No SAP jobs found matching your criteria. Try adjusting your filters.")
        else:
            st.error(f"❌ Error: {results['error']}")
    else:
        # Initial state - show instructions
        st.info("👈 Use the sidebar to set your search filters and click 'Search Jobs' to find SAP opportunities!")
        
        # Display some stats/info cards
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="job-card" style="text-align: center;">
                <div style="font-size: 2.5rem;">🎯</div>
                <div style="font-size: 1.2rem; font-weight: 600; color: #1a202c;">Targeted Search</div>
                <div style="color: #718096;">Find SAP-specific roles</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="job-card" style="text-align: center;">
                <div style="font-size: 2.5rem;">⚡</div>
                <div style="font-size: 1.2rem; font-weight: 600; color: #1a202c;">Fresh Listings</div>
                <div style="color: #718096;">Jobs from last 7 days</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="job-card" style="text-align: center;">
                <div style="font-size: 2.5rem;">🌐</div>
                <div style="font-size: 1.2rem; font-weight: 600; color: #1a202c;">Global Reach</div>
                <div style="color: #718096;">Jobs from worldwide</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Footer
    st.divider()
    st.markdown("""
    <div style="text-align: center; color: white; padding: 1rem;">
        <p>💼 SAP Job Finder | Powered by LinkedIn via RapidAPI</p>
        <p style="font-size: 0.9rem; opacity: 0.8;">Find your next SAP opportunity today!</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
