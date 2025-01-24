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
            max_tokens=4096,
            messages=[{
                "role": "user",
                "content": f"This website contains information about investment rates. I need you to extract the rates options and give them back to me in text I can simply do a json.loads with to store in a database.:\n\n{text}"
            }]
        )
        
        return message.content[0].text
        
    except Exception as e:
        print(f"Error calling Claude API: {str(e)}")
        return None

def main():
    # Get API key from environment variable
    load_dotenv()
    
    api_key = os.getenv("ANTHROPIC_API_KEY")
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