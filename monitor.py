import requests
from bs4 import BeautifulSoup
import hashlib
import time
import os
from datetime import datetime

# Configuration
URL = "https://www.fansale.de/tickets/all/radiohead/520"
CHECK_INTERVAL = 15  # Check every 15 seconds

# Get webhook from environment variable, or use hardcoded value
WEBHOOK_URL = os.environ.get('WEBHOOK_URL', 'https://discord.com/api/webhooks/1432313145342431233/wu3B4-ZCF7MX74Nw2U2fVOOgFzOfWieCC_qsB_o1BDFC5Xr5hQPpLx-GFeLKi-msGYNJ')


def get_page_hash(url):
    """Fetch page content and return a hash of relevant ticket data"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract ticket listings (adjust selectors based on actual page structure)
        ticket_sections = soup.find_all(['article', 'div'],
                                        class_=lambda x: x and ('ticket' in x.lower() or 'event' in x.lower()))

        # Create a string of ticket content
        content = ' '.join([section.get_text(strip=True) for section in ticket_sections])

        # If no specific sections found, use full page content
        if not content:
            content = soup.get_text()

        # Create hash of content
        return hashlib.md5(content.encode()).hexdigest(), len(ticket_sections)

    except Exception as e:
        print(f"Error fetching page: {e}")
        return None, 0


def send_discord_notification(message, ticket_count=0):
    """Send rich notification to Discord"""
    if not WEBHOOK_URL:
        print(f"ALERT: {message}")
        return

    try:
        # Discord embed for rich formatting
        embed = {
            "title": "🎫 Radiohead Tickets - Change Detected!",
            "description": message,
            "color": 15158332,  # Red color
            "url": URL,
            "fields": [
                {
                    "name": "Ticket Sections Found",
                    "value": str(ticket_count),
                    "inline": True
                },
                {
                    "name": "Time",
                    "value": datetime.now().strftime("%H:%M:%S"),
                    "inline": True
                }
            ],
            "footer": {
                "text": "Ticket Monitor"
            },
            "timestamp": datetime.now().isoformat()
        }

        payload = {
            "content": "@everyone **TICKETS CHANGED!**",  # Ping everyone
            "embeds": [embed]
        }

        response = requests.post(WEBHOOK_URL, json=payload, timeout=10)
        response.raise_for_status()
        print(f"Discord notification sent: {message}")
    except Exception as e:
        print(f"Error sending Discord notification: {e}")


def monitor_tickets():
    """Main monitoring loop"""
    print(f"Starting ticket monitor for: {URL}")
    print(f"Checking every {CHECK_INTERVAL} seconds")

    previous_hash = None

    while True:
        try:
            current_hash, ticket_count = get_page_hash(URL)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if current_hash is None:
                print(f"[{timestamp}] Failed to fetch page")
            elif previous_hash is None:
                print(f"[{timestamp}] Initial check - {ticket_count} ticket sections found")
                previous_hash = current_hash
            elif current_hash != previous_hash:
                message = f"**Change detected on Radiohead tickets page!**\n\nCheck immediately: {URL}"
                send_discord_notification(message, ticket_count)  # Fixed function name
                print(f"[{timestamp}] CHANGE DETECTED! Hash changed.")
                previous_hash = current_hash
            else:
                print(f"[{timestamp}] No changes - {ticket_count} tickets")

            time.sleep(CHECK_INTERVAL)

        except KeyboardInterrupt:
            print("\nMonitoring stopped by user")
            break
        except Exception as e:
            print(f"Error in monitoring loop: {e}")
            time.sleep(60)  # Wait a minute before retrying


if __name__ == "__main__":
    monitor_tickets()