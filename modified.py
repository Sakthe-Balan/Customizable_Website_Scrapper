import requests
from bs4 import BeautifulSoup
import csv

# Define the URL of the webpage containing the links to be scraped
url = 'https://www.classcentral.com/provider/coursera'

# Define the headers to be used for making requests to the website
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}

# Send a GET request to the website and parse the HTML content using BeautifulSoup
page = requests.get(url, headers=headers)
soup1 = BeautifulSoup(page.content, 'html.parser')
soup2 = BeautifulSoup(soup1.prettify(), 'html.parser')

# Define the CSV file and attributes
filename = 'example_data.csv'
fields = ['About']

# Loop through all the links in the webpage and scrape the data inside each of them
for link in soup2.find_all('a', attrs={'class': 'color-charcoal course-name'}):
    link_url = link['href']
    
    link_url ='https://www.classcentral.com'+link_url
    print(link_url)
    # Send a GET request to the link and parse the HTML content using BeautifulSoup
    link_page = requests.get(link_url, headers=headers)
    link_soup1 = BeautifulSoup(link_page.content, 'html.parser')
    link_soup2 = BeautifulSoup(link_soup1.prettify(), 'html.parser')
    print(link_soup2)

    # Scrape the data inside the link using BeautifulSoup
    About = link_soup2.find('div',attrs={'class':'wysiwyg'}).get_text().strip()
    

    # Write the data to the CSV file
    with open(filename, 'a+', newline='', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow([About])
