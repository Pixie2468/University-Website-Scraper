# Admission Announcements Scraper

This project is a web scraper designed to extract admission-related announcements from university websites, store the data in a Supabase database, and serve it via a FastAPI server hosted on Render. The scraper runs periodically as a background worker on Render, ensuring fresh data without overloading target websites.

## Features

- **Scraping**: Extracts announcements from specified university websites (e.g., University of Goa, Bangalore University, Mumbai University).
- **Data Storage**: Stores scraped data in a Supabase PostgreSQL database with a predefined schema.
- **API**: Provides a FastAPI server to query announcements efficiently.
- **Deployment**: Hosted on Render with separate services for the API and periodic scraping.
- **PDF Handling**: Extracts text from PDF links in announcements (if applicable).

## Project Structure

```
project/
├── src/
│   ├── scrapers/
│   │   ├── __init__.py
│   │   ├── goa_scraper.py        # Scraper for University of Goa
│   │   ├── bangalore_scraper.py  # Scraper for Bangalore University
│   │   ├── mumbai_scraper.py     # Scraper for Mumbai University
│   ├── database/
│   │   ├── __init__.py
│   │   ├── supabase_client.py    # Supabase client initialization
│   │   ├── db_operations.py      # Database operations for Supabase
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── pdf_extractor.py      # Utility to extract text from PDFs
│   └── main.py                   # FastAPI server entry point
├── scripts/
│   └── update_notifications.py   # Script to run all scrapers
├── .env                          # Environment variables (not tracked by Git)
├── .gitignore                    # Git ignore file
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## Prerequisites

- Python 3.8+
- A Supabase account with a project set up (see schema in `supabase_schema.sql`)
- A Render account for deployment
- Git installed for version control

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/admission-scraper.git
cd admission-scraper
```

### 2. Install Dependencies

Create a virtual environment and install required packages:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the project root with your Supabase credentials:

```
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-service-role-key
```

- Find these in your Supabase dashboard under **Settings > API**.
- **Note**: Use the service role key for full access, but keep it secure.

### 4. Set Up Supabase

1. Create a new Supabase project.
2. Apply the schema from your provided SQL (e.g., `supabase_schema.sql`) via the Supabase SQL editor.
3. Pre-populate reference tables (`websites`, `states`, `programs`) with data relevant to your universities:
   ```sql
   INSERT INTO websites (name, url, description) VALUES
   ('University of Goa', 'https://www.unigoa.ac.in', 'Goa University announcements'),
   ('Bangalore University', 'https://bangaloreuniversity.karnataka.gov.in', 'Bangalore University notifications'),
   ('Mumbai University', 'https://mu.ac.in', 'Mumbai University announcements');
   ```

### 5. Test Locally

Run the scraper script to verify it works:

```bash
python scripts/update_notifications.py
```

This scrapes data from all configured universities and inserts it into Supabase.

Run the FastAPI server locally:

```bash
uvicorn src.main:app --reload
```

Visit `http://localhost:8000/announcements` to see the scraped data.

## Deployment on Render

### 1. Push to GitHub

1. Initialize a Git repository:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```
2. Create a GitHub repository and push your code:
   ```bash
   git remote add origin https://github.com/yourusername/admission-scraper.git
   git push -u origin main
   ```

### 2. Deploy FastAPI Server

1. In Render, create a new **Web Service**:
   - Connect your GitHub repo.
   - Set:
     - **Runtime**: Python 3
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `uvicorn src.main:app --host 0.0.0.0 --port $PORT`
   - Add environment variables in the Render dashboard:
     - `SUPABASE_URL`: Your Supabase URL
     - `SUPABASE_KEY`: Your Supabase service role key
2. Deploy and note the URL (e.g., `https://your-api.onrender.com`).

### 3. Deploy Scraper as a Background Worker

1. In Render, create a new **Background Worker**:
   - Connect the same GitHub repo.
   - Set:
     - **Runtime**: Python 3
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `python scripts/update_notifications.py`
   - Add the same `SUPABASE_URL` and `SUPABASE_KEY` environment variables.
2. Set a cron schedule (e.g., `0 0 * * *` for daily at midnight UTC) in the Render dashboard under **Cron Jobs** to trigger the scraper periodically.

## Usage

- **API Endpoint**: Access announcements via the FastAPI server:
  - `GET /announcements`: Returns all announcements from Supabase.
    ```
    curl https://your-api.onrender.com/announcements
    ```
- **Scraping**: The background worker runs automatically based on the cron schedule, updating Supabase with fresh data.

## API Examples

- **Get All Announcements**:
  ```
  GET https://your-api.onrender.com/announcements
  Response:
  [
      {
          "announcement_id": "uuid",
          "title": "Admission Open 2024",
          "content": "Applications now open.",
          "url": "https://www.unigoa.ac.in/admission-2024",
          "website_id": "uuid",
          "published_date": "2023-10-01"
      }
  ]
  ```

## Schema

The Supabase database uses a schema with tables like:

- `websites`: Source websites being scraped.
- `announcements`: Core scraped data.
- `institutions`, `states`, `programs`: Reference data.
  See `supabase_schema.sql` for the full schema (not included here, but assumed to match your provided SQL).

## Notes

- **Rate Limiting**: Adjust the cron schedule to avoid overwhelming target websites.
- **PDF Extraction**: The `pdf_extractor.py` utility extracts text from PDF links if present in announcements.
- **Security**: The Supabase service role key is used for full access. Ensure Render’s environment variables are secure and not exposed.

## Troubleshooting

- **Scraper Fails**: Check logs in Render for errors (e.g., network issues, HTML changes).
- **API Errors**: Verify Supabase connectivity and credentials in Render’s environment settings.
- **Missing Data**: Inspect the target website’s HTML and update scraper selectors.

## Contributing

Feel free to fork this repository, submit issues, or pull requests to improve functionality.
