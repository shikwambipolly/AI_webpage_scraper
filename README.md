# Web Scraper Project

A simple web scraper that extracts webpage data from a given url and returns JSON formatted data for database insertion or processing.

## Setup Instructions

1. **Clone the Repository**
```bash
git clone https://github.com/shikwambipolly/AI_webpage_scraper.git
cd AI_webpage_scraper
```

2. **Create Virtual Environment**
```bash
python -m venv venv

# On Windows
.\venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure Environment Variables**
```bash
cp .env.example .env
# Edit .env file and add your API key
```

5. **Run the Scraper**
```bash
python3 ./scraper
```

## Requirements
- Python 3.7+
- Required packages are listed in requirements.txt

## Note
Make sure to add your API key to the `.env` file before running the scraper.