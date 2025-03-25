import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def scrape_mumbai_notifications():
    """Scrape notifications from Mumbai University department announcements page."""
    # Define the URL
    url = "https://mu.ac.in/department-announcements"
    
    # Fetch the webpage content
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch page: Status code {response.status_code}")
        return []
    
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Initialize list to store notifications
    notifications = []
    
    # Use CSS selector to find the list items
    list_items = soup.select('#main .entry-content .wpb_text_column ul li')
    
    # Check if any items were found
    if not list_items:
        print("No announcements found in the specified structure.")
        return []
    
    # Process each list item
    for li in list_items:
        a_tag = li.find('a')  # Check for a link within the list item
        if a_tag:
            # If there's a link, extract title and URL
            title = a_tag.text.strip()
            link = urljoin(url, a_tag['href'])  # Convert relative URL to absolute
            
            notifications.append({
                'university': 'Mumbai',
                'title': title,
                'link': link,
            })
        else:
            text = li.text.strip()
            notifications.append({
                'university': 'Mumbai',
                'title': text,
                'date': None,
                'description': None,
                'link': None,
            })
    
    return notifications

# Example usage
if __name__ == "__main__":
    announcements = scrape_mumbai_notifications()
    for announcement in announcements:
        print(announcement)