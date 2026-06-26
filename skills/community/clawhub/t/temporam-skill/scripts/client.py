
import requests
import os
import random
import string

class TemporamClient:
    BASE_URL = "https://api.temporam.com/v1"

    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get("TEMPORAM_API_KEY")
        if not self.api_key:
            raise ValueError("API Key is required. Please set TEMPORAM_API_KEY environment variable or pass it to the constructor.")
        self.headers = {"Authorization": f"Bearer {self.api_key}"}

    def _make_request(self, method, endpoint, params=None, data=None):
        url = f"{self.BASE_URL}{endpoint}"
        try:
            response = requests.request(method, url, headers=self.headers, params=params, json=data)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {e.response.status_code} - {e.response.text}")
            raise
        except requests.exceptions.RequestException as e:
            print(f"Request Error: {e}")
            raise

    def get_domains(self):
        """Returns a list of available email domains."""
        response = self._make_request("GET", "/domains")
        if response and not response.get("error") and response.get("data"):
            return [d["domain"] for d in response["data"]]
        return []

    def list_emails(self, email_address, page=1, limit=20):
        """Returns a list of emails received by a specific email address."""
        params = {"email": email_address, "page": page, "limit": limit}
        response = self._make_request("GET", "/emails", params=params)
        if response and not response.get("error") and response.get("data"):
            return response["data"]
        return []

    def get_email_detail(self, email_id):
        """Returns full details of a specific email, including the email content."""
        endpoint = f"/emails/{email_id}"
        response = self._make_request("GET", endpoint)
        if response and not response.get("error") and response.get("data"):
            return response["data"]
        return None

    def get_latest_email(self, email_address):
        """Returns the most recent email received by a specific email address, including full content."""
        params = {"email": email_address}
        response = self._make_request("GET", "/emails/latest", params=params)
        if response and not response.get("error") and response.get("data"):
            return response["data"]
        return None

    def generate_random_email(self, domain=None):
        """Generates a random email address using an available domain."""
        if not domain:
            domains = self.get_domains()
            if not domains:
                raise ValueError("No available domains found.")
            domain = random.choice(domains)
        
        username_length = random.randint(8, 12)
        username = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(username_length))
        return f"{username}@{domain}"

if __name__ == '__main__':
    # Example usage (for testing purposes)
    # Set your API key as an environment variable: export TEMPORAM_API_KEY="YOUR_API_KEY"
    try:
        client = TemporamClient()
        
        # 1. Generate a random email
        print("Generating random email...")
        random_email = client.generate_random_email()
        print(f"Generated Email: {random_email}")

        # 2. List emails for the generated address (initially empty)
        print(f"\nListing emails for {random_email}...")
        emails = client.list_emails(random_email)
        if emails:
            for email in emails:
                print(f"  - Subject: {email['subject']}, From: {email['from_email']}")
        else:
            print("  No emails found yet.")

        # 3. (Optional) If you manually send an email to random_email, you can then fetch its content
        # email_id = "<ID_OF_A_RECEIVED_EMAIL>"
        # print(f"\nGetting detail for email ID {email_id}...")
        # email_detail = client.get_email_detail(email_id)
        # if email_detail:
        #     print(f"  Subject: {email_detail['subject']}")
        #     print(f"  Content: {email_detail['content'][:200]}...") # Print first 200 chars
        # else:
        #     print("  Email not found.")

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
