import requests
from bs4 import BeautifulSoup
import csv
import time
from requests.exceptions import RequestException
from urllib3.exceptions import ProtocolError
from requests.exceptions import ChunkedEncodingError
import re

filename = 'Course_Info(Final).csv'
fields = ['title', 'Provider', 'taught_by', 'Link', 'url', 'side_card', 'what_learn_1', 'what_learn_2','ratings','no_of_ratings']

with open(filename, 'w', newline='', encoding='UTF8') as f:
    writer = csv.writer(f)
    writer.writerow(fields)

for i in range(1, 661):
    # Define the URL of the webpage containing the links to be scraped
    url = 'https://www.classcentral.com/provider/udemy?page=' + str(i)

    # Define the headers to be used for making requests to the website
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
        "Accept-Encoding": "gzip, deflate",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "DNT": "1", "Connection": "close",
        "Upgrade-Insecure-Requests": "1"}

    # Send a GET request to the website and parse the HTML content using BeautifulSoup
    while True:
        try:
            page = requests.get(url, headers=headers)
            break
        except (RequestException, ProtocolError) as e:
            print(f"Error: {e}")
            time.sleep(2)  # wait for 2 seconds before retrying
            continue

    soup1 = BeautifulSoup(page.content, 'html.parser')
    soup2 = BeautifulSoup(soup1.prettify(), 'html.parser')

    # Loop through all the links in the webpage and scrape the data inside each of them
    for link in soup2.find_all('a', attrs={'class': 'color-charcoal course-name'}):
        link_url = link['href']
        link_url = 'https://www.classcentral.com' + link_url
        print(link_url, i)
        if link_url == 'https://www.classcentral.com/course/udemy-copywriter-32281 121':
            continue

        # Send a GET request to the link and parse the HTML content using BeautifulSoup
        retry_count = 0
        while retry_count < 3:
            try:
                link_page = requests.get(link_url, headers=headers)
                link_soup1 = BeautifulSoup(link_page.content, 'html.parser')
                link_soup2 = BeautifulSoup(link_soup1.prettify(), 'html.parser')
                time.sleep(2)

                # Scrape the data inside the link using BeautifulSoup
                try:
                    title = link_soup2.find('h1', attrs={'class': 'head-2'}).get_text().strip()
                except AttributeError:
                    print("Title not available. Retrying...")
                    time.sleep(2)
                    retry_count += 1
                    continue

                try:
                    ratings = link_soup2.find('p', attrs={'class': 'text-2 medium-down-margin-top-xsmall large-up-margin-left-xsmall inline-block'}).get_text().strip()
                    ratings = ratings.replace('\n', ' ').replace('\r', '')  # Replace line breaks with spaces
                    ratings = re.sub(' +', ' ', ratings)  # Replace multiple spaces with a single space
                except AttributeError:
                    print("Title not available. Retrying...")
                    time.sleep(2)
                    retry_count += 1
                    continue

                # Extract the rating and number of ratings using regular expressions
                rating_match = re.search(r'(\d+(\.\d+)?) rating', ratings)
                number_of_ratings_match = re.search(r'based on (\d+) ratings', ratings)

                # Assign the extracted values to separate variables
                rating = float(rating_match.group(1))
                number_of_ratings = int(number_of_ratings_match.group(1))


                try:
                    provider = link_soup2.find('a', attrs={'class': 'text-1 link-gray-underline'}).get_text().strip()
                except AttributeError:
                    print("Provider not available. Retrying...")
                    time.sleep(2)
                    retry_count += 1
                    continue

                try:
                    h3_with_class = link_soup2.find('div', class_='course-noncollapsable-section')
                    p_with_class = h3_with_class.find('p', class_='text-1')
                    taught_by = p_with_class.get_text().strip()
                except AttributeError:
                    print("Taught by not available. Retrying...")
                    time.sleep(2)
                    retry_count += 1
                    continue

                try:
                    link = link_soup2.find('a', attrs={'class': 'btn-blue btn-medium width-100 padding-horz-xlarge'}).get('href').strip()
                    link = 'https://www.classcentral.com' + link
                except AttributeError:
                    print("Link not available. Retrying...")
                    time.sleep(2)
                    retry_count += 1
                    continue

                try:
                    a_element = link_soup2.find('a', class_='text-1 link-gray-underline')
                    url = a_element['href']
                except AttributeError:
                    print("URL not available. Retrying...")
                    time.sleep(2)
                    retry_count += 1
                    continue

                try:
                    li_list = link_soup2.find_all('li', class_='course-details-item border-gray-light')
                    side_cards = []

                    for li_with_class in li_list:
                        span_with_class = li_with_class.find('span', class_='text-2 line-tight')
                        if span_with_class:
                            side_card = span_with_class.get_text().strip()
                            side_cards.append(side_card)
                        else:
                            a_with_class = li_with_class.find('a', class_='text-2 color-charcoal line-tight')
                            if a_with_class:
                                side_card = a_with_class.get_text().strip()
                                side_cards.append(side_card)

                except AttributeError:
                    print("side_card not available. Retrying...")
                    time.sleep(2)
                    retry_count += 1
                    continue

                try:
                    content_element = link_soup2.find('div', class_='truncatable-area')
                    if content_element is None:
                        content_element = link_soup2.find('div', class_='wysiwyg text-1 line-wide')

                    # Extract the text from the element
                    what_learn_1 = content_element.get_text(strip=True)
                    separator = "What you'll learn:"
                    if separator in what_learn_1:
                        what_learn_1 = what_learn_1.split(separator, 1)[0].strip()

                except AttributeError:
                    print("What you'll learn-1 not available. Retrying...")
                    time.sleep(2)
                    retry_count += 1
                    continue

                try:
                    div_element = link_soup2.find('div', class_='truncatable-area')
                    if div_element is None:
                        div_element = link_soup2.find('div', class_='wysiwyg text-1 line-wide')

                    # Remove attributes from the initial div element
                    div_element.attrs = {}

                    # Find the separator string
                    separator = "What you'll learn:"
                    separator_index = div_element.get_text().find(separator)

                    if separator_index != -1:
                        # Extract the portion of HTML after the separator
                        what_learn_2 = str(div_element)[separator_index + len(separator):].strip()

                    else:
                        print("What you'll learn-2 not available. Retrying...")
                        time.sleep(2)
                        retry_count += 1
                        continue

                except AttributeError:
                    print("What you'll learn-2 not available. Retrying...")
                    time.sleep(2)
                    retry_count += 1
                    continue

                # Write the data to the CSV file
                with open(filename, 'a+', newline='', encoding='UTF8') as f:
                    writer = csv.writer(f)
                    writer.writerow([title,rating,number_of_ratings, provider, taught_by, link, url, side_cards, what_learn_1, what_learn_2])
                break
            except AttributeError:
                print(f"Data not available. Retrying in 2 seconds... Retry count: {retry_count}")
                time.sleep(2)
                retry_count += 1
