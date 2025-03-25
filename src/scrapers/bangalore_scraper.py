import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def scrape_bangalore_notifications():
    """Scrape notifications from Bangalore University."""
    url = "https://bangaloreuniversity.karnataka.gov.in/notifications"
    
    # Fetch the webpage with error handling
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise exception if request fails
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return []

    # Parse HTML with default parser (no lxml dependency)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    notifications = []
    
    # Correctly find the div with class 'container' and then the ul inside it
    container = soup.find('div', class_='container')
    if container:
        unordered_list = container.find('ul')
        if unordered_list:
            for item in unordered_list.find_all('li'):
                link_tag = item.find('a')
                if link_tag:
                    # Use link text as title, assuming <i> might not always exist
                    title = link_tag.text.strip() if link_tag.text.strip() else "Untitled"
                    link = urljoin(url, link_tag['href'])
                    
                    notifications.append({
                        'university': 'Bangalore',
                        'title': title,
                        'description': None,
                        'link': link,
                    })
                else:
                    # Handle li items without links
                    title = item.text.strip() if item.text.strip() else "Untitled"
                    notifications.append({
                        'university': 'Bangalore',
                        'title': title,
                        'description': None,
                        'link': None,
                    })
        else:
            print("No <ul> found inside container.")
    else:
        print("No div with class 'container' found.")
    
    return notifications