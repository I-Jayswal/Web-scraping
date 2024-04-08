

import requests
from bs4 import BeautifulSoup
import csv
import os

def scrape_and_save(url):
    # Send a GET request to the specified URL
    response = requests.get(url)

    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract required information: Restaurant Name
        restaurant_name_elem = soup.find('h1', class_='css-1se8maq')
        restaurant_name = restaurant_name_elem.text.strip() if restaurant_name_elem else "N/A"
        print(restaurant_name_elem)

        # Extracting reviews
        reviews = []
        review_elements = soup.find_all('li', class_='css-1q2nwpv') # Adjust class name

        if review_elements:
            for review_elem in review_elements:
                try:
                    # Extracting review text
                    review_text_elem = review_elem.find('span', class_='raw__09f24__T4Ezm')
                    review_text = review_text_elem.text.strip() if review_text_elem else "N/A"

                    # Extracting reviewer
                    reviewer_elem = review_elem.find('a', class_='css-19v1rkv')  # Adjust class name
                    reviewer = reviewer_elem.text.strip() if reviewer_elem else "N/A"

                    # Extracting rating
                    rating_elem = review_elem.find('div', class_='css-14g69b3')  # Adjust class name
                    rating = rating_elem['aria-label'].split(' ')[0] if rating_elem else "N/A"

                    print(review_text, reviewer, rating)

                    # Append review data to the reviews list
                    reviews.append({
                        'Review_text': review_text,
                        'Reviewer': reviewer,
                        'Rating': rating
                    })
                except AttributeError:
                    print("Some review elements are missing expected structure.")

            # Create and write to CSV file
            csv_filename = 'restaurant_reviews.csv'
            with open(csv_filename, 'w', newline='', encoding='utf-8') as csv_file:
                # Writing header and data to CSV file
                fieldnames = ['Restaurant_Name'] + list(reviews[0].keys())
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()

                # Writing restaurant name and reviews data
                for review in reviews:
                    writer.writerow({
                        'Restaurant_Name': restaurant_name,
                        **review
                    })

            # Print status messages
            print(f"Data has been scraped and saved to {csv_filename}")
            print("Your file saved in current Working Directory:", os.getcwd())
        else:
            print("No reviews found on the page.")
    else:
        print(f"Failed to fetch the web page. Status code: {response.status_code}")

# Entry point of the script
if __name__ == "__main__":
    # Specify the URL directly
    restaurant_url = "https://www.yelp.ca/biz/pai-northern-thai-kitchen-toronto-5?osq=Restaurants"
    scrape_and_save(restaurant_url)


def get_page():
	global url
	# Code here - URL
	url = 'https://www.yelp.ca/biz/pai-northern-thai-kitchen-toronto-5?osq=Restaurants'
	# Code ends here



