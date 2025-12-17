# 💼 SAP Job Finder

A modern Streamlit web application that helps you find SAP jobs posted in the last 7 days on LinkedIn using RapidAPI.

## Features

- 🎯 **Targeted Search**: Search specifically for SAP-related jobs
- ⚡ **Fresh Listings**: Filter jobs posted within the last 1-30 days (default: 7 days)
- 🌍 **Location Filters**: Search by specific countries or worldwide
- 🌐 **Remote Options**: Filter for remote-only positions
- 📄 **Full Descriptions**: View complete job descriptions
- 🔗 **Direct Apply**: Quick links to application pages
- 📱 **Responsive Design**: Works on desktop and mobile devices
- 🎨 **Modern UI**: Beautiful gradient design with smooth animations

## Technologies Used

- **Streamlit** - Web application framework
- **RapidAPI** - LinkedIn Job Search API integration
- **Python 3.11+** - Backend programming
- **Requests** - HTTP library for API calls

## Local Setup

### Prerequisites

- Python 3.11 or higher
- RapidAPI account with LinkedIn Job Search API subscription

### Installation

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd "job search"
   ```

2. **Create and activate virtual environment**:
   ```bash
   python -m venv env
   .\env\Scripts\Activate.ps1  # Windows
   # source env/bin/activate  # macOS/Linux
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API credentials**:
   Create `.streamlit/secrets.toml` file:
   ```toml
   [rapidapi]
   key = "your-rapidapi-key-here"
   host = "default-application_11394855.proxy-production.allthingsdev.co"
   ```

5. **Run the application**:
   ```bash
   streamlit run app.py
   ```

The app will open in your browser at `http://localhost:8501`

## Deployment to Streamlit Cloud

### Prerequisites

- GitHub account
- Streamlit Cloud account (free at [share.streamlit.io](https://share.streamlit.io))
- RapidAPI credentials

### Deployment Steps

1. **Create GitHub Repository**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: SAP Job Finder"
   git branch -M main
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Deploy to Streamlit Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select your GitHub repository
   - Set main file path: `app.py`
   - Click "Advanced settings"

3. **Configure Secrets**:
   In the Streamlit Cloud dashboard, add secrets:
   ```toml
   [rapidapi]
   key = "your-rapidapi-key-here"
   host = "default-application_11394855.proxy-production.allthingsdev.co"
   ```

4. **Deploy**:
   - Click "Deploy!"
   - Wait for deployment to complete
   - Your app will be live at `https://your-app-name.streamlit.app`

## Usage

1. **Set Filters** (optional):
   - Choose location from dropdown
   - Toggle "Remote Jobs Only" if needed
   - Adjust date range slider (1-30 days)
   - Select results per page

2. **Search**:
   - Click "🔎 Search Jobs" button
   - Wait for results to load

3. **View Results**:
   - Browse job cards with key information
   - Click "View Full Description" to expand details
   - Click "Apply Now" to visit the job posting

4. **Navigate**:
   - Use "Previous Page" and "Next Page" buttons to browse more results

## API Information

This app uses the **LinkedIn Job Search API** via RapidAPI:
- **Endpoint**: Jobs Hourly
- **Rate Limits**: Depends on your RapidAPI subscription plan
- **Data**: Refreshed hourly, includes jobs from last 7 days
- **Coverage**: 50+ countries worldwide

## Project Structure

```
job search/
├── app.py                 # Main Streamlit application
├── linkedin_api.py        # API client module
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore file
├── .streamlit/
│   ├── config.toml       # Streamlit configuration
│   └── secrets.toml      # API credentials (not in git)
└── README.md             # This file
```

## Troubleshooting

### API Errors

- **"API credentials not configured"**: Check your `.streamlit/secrets.toml` file
- **"Rate limit exceeded"**: Wait a moment and try again, or upgrade your RapidAPI plan
- **"No jobs found"**: Try adjusting filters or increasing date range

### Local Issues

- **Module not found**: Ensure virtual environment is activated and dependencies installed
- **Port already in use**: Stop other Streamlit apps or specify different port: `streamlit run app.py --server.port 8502`

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Job data from LinkedIn via [RapidAPI](https://rapidapi.com/)
- Gradient design inspired by modern web applications

---

**Happy Job Hunting! 🚀**
