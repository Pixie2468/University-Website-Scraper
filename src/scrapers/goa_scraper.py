import requests
from bs4 import BeautifulSoup

def scrape_goa_notifications():
    """Scrape announcements from Goa University page."""
    url = "https://www.unigoa.ac.in/systems/c/admissions/announcementsnotices.html"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch page: Status code {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')

    # Locate the container
    inside_wrapper = soup.find('div', class_='details1')
    if not inside_wrapper:
        print("Container 'inside_wrapper' not found.")
        return []


    # details1 = inside_wrapper.find('div')
    
    details1_left = inside_wrapper.find('div', class_='details1_left')
    if not details1_left:
        print("Container 'details1_left' not found.")
        return []

    # Extract titles and details
    notifications = []
    for h4 in details1_left.find_all('h4'):
        title = h4.text.strip()
        next_element = h4.find_next_sibling()
        details = [li.text.strip() for li in next_element.find_all('li')]
        notifications.append({
            'university': 'Goa',
            'title': title,
            'details': details
        })

    return notifications

# Example usage
if __name__ == "__main__":
    announcements = scrape_goa_notifications()
    for announcement in announcements:
        print(announcement)