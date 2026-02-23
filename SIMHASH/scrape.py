import sys
import requests
from bs4 import BeautifulSoup

# check if URL is provided
if len(sys.argv) < 2:
    print("Usage: python scrape.py <URL>")
    sys.exit(1)

# take URL from command line
url = sys.argv[1]

# fetch HTML from URL
response = requests.get(url)
html = response.text

soup = BeautifulSoup(html, "html.parser")

soup.prettify()

print("Links:")
for link in soup.find_all('a'):
    print(link.get('href'))

print("Title:")
if soup.title:
    print(soup.title.text)

print("Body:")
if soup.body:
    print(soup.body.get_text(separator="\n", strip=True))