import sys
import os
# Adjust the system path to import scraper modules from the src directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.scrapers.goa_scraper import scrape_goa_notifications
from src.scrapers.bangalore_scraper import scrape_bangalore_notifications
from src.scrapers.mumbai_scraper import scrape_mumbai_notifications

def display_notifications():
    """Scrape and display notifications from all universities on the terminal."""
    print("Scraping Goa University...")
    goa_notifications = scrape_goa_notifications()
    print_notifications("Goa", goa_notifications)

    print("\nScraping Bangalore University...")
    bangalore_notifications = scrape_bangalore_notifications()
    print_notifications("Bangalore", bangalore_notifications)

    print("\nScraping Mumbai University...")
    mumbai_notifications = scrape_mumbai_notifications()
    print_notifications("Mumbai", mumbai_notifications)

def print_notifications(university, notifications):
    """Print notifications for a given university in a formatted way."""
    print(f"\n=== {university} University Notifications ===")
    if not notifications:
        print("No notifications found.")
        return

    for notif in notifications:
        print(f"Title: {notif.get('title', 'N/A')}")
        if 'date' in notif:
            print(f"Date: {notif['date']}")
        if 'description' in notif:
            print(f"Description: {notif['description']}")
        if 'link' in notif:
            print(f"Link: {notif['link']}")
            if notif['link'].lower().endswith('.pdf'):
                print("  (PDF file)")
        print("-" * 50)

if __name__ == "__main__":
    display_notifications()