import os
from playwright.sync_api import sync_playwright

STATE_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "state.json")

def login():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        print("Navigating to Xiaohongshu Creator Studio...")
        page.goto("https://creator.xiaohongshu.com/login")

        print("Please log in manually (e.g., by scanning the QR code).")
        print("Waiting for successful login redirect to creator home...")
        
        try:
            # Wait for the URL to change to the creator home page, indicating successful login
            page.wait_for_url("**/creator/home**", timeout=300000) # 5 minutes timeout
            print("Login successful! Saving session state...")
            
            # Save the authentication state
            context.storage_state(path=STATE_FILE)
            print(f"Session saved to {STATE_FILE}")
            
        except Exception as e:
            print(f"Login process failed or timed out: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    login()
