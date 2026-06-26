import os
import re
import time
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

def sanitize_name(text):
    """Removes emojis, illegal OS characters, and trims whitespace for safe folder/file names."""
    # Remove emojis and special characters, keep alphanumeric, spaces, and basic punctuation
    clean_text = re.sub(r'[^\w\s\-\.]', '', text)
    return re.sub(r'[\\/*?:"<>|]', "", clean_text).strip()

def run(channel_name: str, download_directory: str = "./Telegram_Study_Materials", scroll_limit: int = 5):
    # Ensure base directory exists
    base_dir = os.path.abspath(download_directory)
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    print(f"[*] Initializing OpenClaw Telegram Scraper...")
    print(f"[*] Target Channel: {channel_name}")
    print(f"[*] Save Location: {base_dir}")

    # Use Playwright to hook into Chrome. 
    # Launching a persistent context ensures user stays logged in across sessions.
    with sync_playwright() as p:
        # We use a local profile directory so it doesn't ask for login every time
        user_data_dir = os.path.abspath("./openclaw_chrome_profile")
        
        try:
            browser = p.chromium.launch_persistent_context(
                user_data_dir=user_data_dir,
                headless=False, # Must be visible for Telegram Web
                accept_downloads=True,
                viewport={"width": 1280, "height": 800}
            )
            page = browser.new_page()
            
            # 1. NAVIGATION & LOGIN GUARD
            print("[*] Navigating to Telegram Web...")
            page.goto("https://web.telegram.org/a/", timeout=30000)
            
            # Wait for either the chat list OR the login screen
            try:
                # Check for login elements
                page.wait_for_selector("#auth-pages, #sign-in-phone-number, canvas", timeout=8000)
                print("\n[CRITICAL ERROR] User is NOT logged in to Telegram Web.")
                print("[ACTION REQUIRED] A Chrome window has opened. Please log in via QR code or phone number.")
                print("[!] Stopping execution to prevent getting stuck. Restart skill after logging in.\n")
                browser.close()
                return {"status": "error", "message": "User not logged in. Manual login required."}
            except PlaywrightTimeoutError:
                # If we don't see login screens, we assume we are authenticated
                print("[*] Login verified. Proceeding...")

            # 2. FINDING THE CHANNEL
            print(f"[*] Searching for channel: '{channel_name}'")
            try:
                search_box = page.wait_for_selector("input[title='Search']", timeout=10000)
                search_box.fill(channel_name)
                time.sleep(2) # Allow search results to populate
                
                # Click the first chat result
                chat_result = page.wait_for_selector(".search-super-results .ListItem, .chatlist-chat", timeout=10000)
                chat_result.click()
                time.sleep(3) # Allow chat history to render
            except PlaywrightTimeoutError:
                print(f"[ERROR] Could not find the search box or channel '{channel_name}'.")
                browser.close()
                return {"status": "error", "message": "Channel not found."}

            # 3. SCANNING & FILTERING LOGIC
            print("[*] Scanning chat history...")
            
            current_folder = "Uncategorized"
            processed_links = set() # Prevent re-downloading/re-clicking the exact same element
            
            # Anti-stuck scrolling loop
            for scroll_iteration in range(scroll_limit):
                print(f"[*] Scan Batch {scroll_iteration + 1}/{scroll_limit}...")
                
                # Get all visible messages in the DOM
                messages = page.locator(".Message").all()
                
                for msg in messages:
                    try:
                        # Extract the text of the message to use as a header
                        msg_text = msg.inner_text()
                        
                        # --- HEADER DETECTION ---
                        # If message has text, split by newlines. 
                        # We assume the first line (if it doesn't contain 'http' or 'publicearn') is the category header.
                        if msg_text:
                            lines = [line.strip() for line in msg_text.split('\n') if line.strip()]
                            if lines:
                                first_line = lines[0]
                                # Heuristic: If it looks like a title (no URLs, reasonable length)
                                if "http" not in first_line and "publicearn" not in first_line and len(first_line) < 60:
                                    sanitized_header = sanitize_name(first_line)
                                    if sanitized_header:
                                        current_folder = sanitized_header

                        # --- DANGEROUS LINK FILTER & DOWNLOAD ---
                        links = msg.locator("a").all()
                        for link in links:
                            try:
                                href = link.get_attribute("href") or ""
                                text = link.inner_text()
                                link_id = f"{href}_{text}" # Unique identifier for this session
                                
                                if not text or link_id in processed_links:
                                    continue
                                
                                processed_links.add(link_id)

                                # THE SAFETY FILTER (CRITICAL)
                                malicious_domains = ["publicearn.in", "bit.ly", "http://", "https://"]
                                if any(domain in href for domain in malicious_domains):
                                    print(f"   [BLOCKED] Ignored dangerous external link: {text}")
                                    continue
                                
                                # If it passes the filter, it's an internal file/link
                                safe_filename = sanitize_name(text)
                                if not safe_filename:
                                    continue
                                
                                # Ensure it ends with .pdf
                                if not safe_filename.lower().endswith('.pdf'):
                                    safe_filename += ".pdf"

                                # Create target directory based on the current header
                                target_dir = os.path.join(base_dir, current_folder)
                                if not os.path.exists(target_dir):
                                    os.makedirs(target_dir)

                                file_path = os.path.join(target_dir, safe_filename)

                                # Check if already downloaded on disk
                                if os.path.exists(file_path):
                                    print(f"   [SKIPPED] File already exists: {safe_filename} (in {current_folder})")
                                    continue

                                # Execute Download Trigger
                                print(f"   [DOWNLOADING] Found internal file: {safe_filename} -> to folder '{current_folder}'")
                                
                                # We expect a download event when clicking the internal Telegram link
                                with page.expect_download(timeout=15000) as download_info:
                                    # Force click, bypassing any overlay
                                    link.click(force=True)
                                
                                download = download_info.value
                                
                                # Save the file
                                download.save_as(file_path)
                                print(f"   [SUCCESS] Saved: {file_path}")
                                
                            except PlaywrightTimeoutError:
                                print(f"   [TIMEOUT] Clicking '{text}' did not trigger a download. It might just be text. Skipping.")
                                continue
                            except Exception as e:
                                print(f"   [ERROR] Failed to process link '{text}': {str(e)}")
                                continue

                    except Exception as e:
                        # Catch errors at the message level so the whole loop doesn't crash
                        pass

                # Scroll up to load older messages
                print("[*] Scrolling up to load older messages...")
                try:
                    # Target the scrollable area in Telegram Web
                    page.evaluate("document.querySelector('.MessageList').scrollTop -= 2000")
                    time.sleep(2) # Wait for network request to load older messages
                except Exception:
                    # Fallback scroll if .MessageList isn't found
                    page.mouse.wheel(0, -2000)
                    time.sleep(2)

            print("\n[*] Skill execution completed successfully.")
            browser.close()
            return {"status": "success", "message": f"Successfully scraped and organized files into {base_dir}"}

        except Exception as e:
            print(f"\n[FATAL ERROR] An unexpected error occurred: {str(e)}")
            return {"status": "error", "message": str(e)}

# For local testing outside of OpenClaw
if __name__ == "__main__":
    # Replace with a real channel name if running standalone
    run("Test_Channel_Name", "./Test_Downloads", scroll_limit=2)