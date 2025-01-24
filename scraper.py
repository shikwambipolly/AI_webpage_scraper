import requests
from bs4 import BeautifulSoup
import anthropic
from dotenv import load_dotenv
import os
from urllib.parse import urlparse

def scrape_website(url):
    """
    Scrape text content from a website
    """
    try:
        # add headers to mimic a browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Make the request
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # Parse with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # remove script and style elements
        for script in soup(['script', 'style', 'header', 'footer', 'nav']):
            script.decompose()
            
        # Get text content
        text = soup.get_text(separator='\n', strip=True)
        
        # Clean up the text
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text
        
    except Exception as e:
        print(f"Error scraping website: {str(e)}")
        return None

def analyze_with_claude(text, api_key):
    """
    Send text to Claude 3.5 Sonnet for analysis
    """
    try:
        client = anthropic.Client(api_key=api_key)
        
        # Create the message
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            system="""
            You are an expert at parsing scrapes HTML content and processing whatever data you are asked to find. You are also an expert at return simple JSON payloads that are ready to database insertion.
            For every prompt you get, simply parse the given HTML content, look for whatever data you are asked to look for in the prompt, and return a single or list of JSON objects in text, so that I can simply run
            'data = json.loads(response)'
            DO NOT OUTPUT ANYTHING ELSE. I ONLY WANT THE JSON TEXT SO THAT I CAN LOAD YOUR RESPONSE DIRECTLY TO JSON
            """,
            max_tokens=4096,
            messages=[{
                "role": "user",
                "content": f"This git repo contains some files. I need you to extract the file information and only return the data in json.loads() ready text.:\n\n{text}"
            }]
        )
        
        return message.content[0].text
        
    except Exception as e:
        print(f"Error calling Claude API: {str(e)}")
        return None

def main():
    # Get API key from environment variable
    load_dotenv()
    api_key = os.getenv('API_KEY')
    
    if not api_key:
        print("Please set your ANTHROPIC_API_KEY environment variable")
        return
    
    # Get URL from user
    url = input("Enter the website URL to analyze: ")
    
    # Validate URL
    try:
        result = urlparse(url)
        if not all([result.scheme, result.netloc]):
            print("Invalid URL. Please include the full URL with http:// or https://")
            return
    except Exception:
        print("Invalid URL format")
        return
    
    # Scrape website
    print("Scraping website...")
    text = scrape_website(url)
    
    if text:
        print("\nSending to Claude for analysis...")
        analysis = analyze_with_claude(text, api_key)
        
        if analysis:
            print("\nClaude's Analysis:")
            print(analysis)
        else:
            print("Failed to get analysis from Claude")
    else:
        print("Failed to scrape website")

if __name__ == "__main__":
    main()