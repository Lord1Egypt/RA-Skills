import os
import argparse
import time
from playwright.sync_api import sync_playwright

STATE_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "state.json")
PUBLISH_URL = "https://creator.xiaohongshu.com/publish/publish"

def post(title, content, files):
    if not os.path.exists(STATE_FILE):
        print(f"Error: Session file not found at {STATE_FILE}.")
        print("Please run the login.py script first to authenticate.")
        return

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(storage_state=STATE_FILE)
        page = context.new_page()

        print("Navigating to publish page...")
        page.goto(PUBLISH_URL)

        # 1. Upload Files
        print(f"Attempting to upload files: {files}")
        try:
            # Look for the file input element. Xiaohongshu might use standard input[type="file"]
            # wrapped in their UI components.
            file_input = page.locator('input[type="file"]').first
            file_input.set_input_files(files)
            
            # Wait a moment for the upload preview to process
            print("Files selected, waiting for upload to process...")
            page.wait_for_timeout(5000) 
        except Exception as e:
            print(f"Failed to upload files: {e}")
            return

        # 2. Fill Title
        print("Filling title...")
        try:
            # Common placeholders or class names for the title input
            title_input = page.locator('input[placeholder*="标题"]').first
            if not title_input.is_visible():
                 title_input = page.locator('.c-input_inner').first 
            
            title_input.fill(title)
        except Exception as e:
             print(f"Warning: Could not fill title: {e}")

        # 3. Fill Content/Description
        print("Filling description content...")
        try:
            # The description area is usually a contenteditable div
            desc_input = page.locator('#post-textarea').first
            if not desc_input.is_visible():
                desc_input = page.locator('.c-editor').first
            if not desc_input.is_visible():
                desc_input = page.locator('[contenteditable="true"]').first
            
            desc_input.fill(content)
        except Exception as e:
            print(f"Warning: Could not fill content: {e}")

        # 4. Click Publish Button
        print("Looking for publish button...")
        try:
            publish_btn = page.locator('button:has-text("发布")').first
            publish_btn.click()
            
            print("Publish button clicked! Waiting to confirm...")
            page.wait_for_timeout(5000)
            
        except Exception as e:
            print(f"Error clicking publish button: {e}")
            print("You may need to click it manually in the browser window.")
        
        # Keep browser open briefly so user can see result
        page.wait_for_timeout(3000)
        browser.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Publish content to Xiaohongshu")
    parser.add_argument("--title", required=True, help="Title of the post")
    parser.add_argument("--content", required=True, help="Description/body of the post")
    parser.add_argument("--files", nargs='+', required=True, help="One or more file paths to upload")
    
    args = parser.parse_args()
    
    # Verify files exist
    valid_files = []
    for f in args.files:
        abs_path = os.path.abspath(f)
        if os.path.exists(abs_path):
            valid_files.append(abs_path)
        else:
            print(f"Warning: File not found: {abs_path}")
            
    if not valid_files:
        print("Error: No valid files provided. Exiting.")
        exit(1)
        
    post(args.title, args.content, valid_files)
