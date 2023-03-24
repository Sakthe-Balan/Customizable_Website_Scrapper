import requests
from bs4 import BeautifulSoup
import json

url = 'https://www.classcentral.com/provider/coursera'
filename = './data.json'

# Make a GET request to the URL
response = requests.get(url)

# Parse the HTML content using Beautiful Soup
soup = BeautifulSoup(response.content, 'html.parser')
print(soup)

# Find all the cards on the page
cards = soup.find_all('li', {'class': 'bg-white border-all border-gray-light'})

# Loop through the cards and extract data
for card in cards:
    data = {}
    data['About'] = card.find('div', class_='text-1.line-wide').text
    # data['description'] = card.find('p').text

    # Load the existing JSON data
    with open(filename, 'r') as f:
        existing_data = json.load(f)

    # Append the new data to the existing data
    existing_data.append(data)

    # Save the combined data to the JSON file
    with open(filename, 'w') as f:
        json.dump(existing_data, f)

        

        
