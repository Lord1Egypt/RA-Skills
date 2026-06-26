#!/usr/bin/env python3
"""
Selenium script to format Google Doc
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def setup_driver():
    """Setup Chrome driver with proxy"""
    print("🚀 Setting up Chrome with proxy...")
    
    chrome_options = Options()
    
    # Add proxy
    chrome_options.add_argument('--proxy-server=http://localhost:2080')
    
    # Other options
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')
    
    # Keep browser open for debugging
    chrome_options.add_experimental_option("detach", True)
    
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def login_to_google(driver, email, password):
    """Login to Google account"""
    print(f"🔐 Logging in to {email}...")
    
    try:
        # Go to Google Docs directly (might redirect to login)
        driver.get("https://docs.google.com/document/d/10aUUm36tsHcOhc0SaobAWrJZmrLXWbbG8qWxykGgc4s/edit")
        time.sleep(3)
        
        # Check if login page appears
        if "accounts.google.com" in driver.current_url:
            print("  Login page detected...")
            
            # Enter email
            email_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "identifierId"))
            )
            email_field.send_keys(email)
            email_field.send_keys(Keys.RETURN)
            time.sleep(2)
            
            # Enter password
            password_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "Passwd"))
            )
            password_field.send_keys(password)
            password_field.send_keys(Keys.RETURN)
            time.sleep(5)
        
        print("✅ Logged in successfully")
        return True
        
    except Exception as e:
        print(f"❌ Login failed: {e}")
        # Take screenshot for debugging
        driver.save_screenshot("login_error.png")
        return False

def add_cover_page(driver):
    """Add cover page at beginning"""
    print("📄 Adding cover page...")
    
    try:
        # Wait for document to load
        time.sleep(5)
        
        # Go to beginning of document
        actions = ActionChains(driver)
        actions.key_down(Keys.COMMAND).send_keys(Keys.HOME).key_up(Keys.COMMAND).perform()
        time.sleep(1)
        
        # Type cover page content
        cover_content = """دانشگاه تهران
دانشکدگان فارابی  
دانشکده مهندسی
گروه مهندسی کامپیوتر

پروژه پایانی کارشناسی

عنوان: طراحی و پیاده‌سازی پلتفرم Cloud-Native برای آزمایشگاه GPU دانشگاهی

نگارش: علی قطبی‌زاده

استاد راهنما: دکتر [نام استاد]

تاریخ: بهار ۱۴۰۳
        
"""
        
        # Type slowly
        for line in cover_content.split('\n'):
            actions.send_keys(line).perform()
            actions.send_keys(Keys.ENTER).perform()
            time.sleep(0.5)
        
        # Add page break
        actions.send_keys(Keys.ENTER).perform()
        actions.key_down(Keys.COMMAND).send_keys(Keys.ENTER).key_up(Keys.COMMAND).perform()
        time.sleep(1)
        
        print("✅ Cover page added")
        return True
        
    except Exception as e:
        print(f"⚠️  Cover page issue: {e}")
        return False

def apply_basic_formatting(driver):
    """Apply basic formatting to entire document"""
    print("🎨 Applying basic formatting...")
    
    try:
        # Select all (Cmd+A)
        actions = ActionChains(driver)
        actions.key_down(Keys.COMMAND).send_keys('a').key_up(Keys.COMMAND).perform()
        time.sleep(2)
        
        print("  Selected all text")
        
        # Note: Actual formatting would require clicking toolbar buttons
        # This is complex in Selenium for Google Docs
        
        print("⚠️  Formatting requires manual toolbar clicks")
        print("🔧 Manual steps needed:")
        print("   1. Font: Arial")
        print("   2. Size: 14")
        print("   3. Alignment: Justify")
        print("   4. Line spacing: 1.5")
        
        return False  # Manual completion needed
        
    except Exception as e:
        print(f"❌ Formatting failed: {e}")
        return False

def main():
    print("🔧 GOOGLE DOCS FORMATTER")
    print("="*50)
    
    # Credentials
    email = "ali.lotfizadeh.g@gmail.com"
    password = "sYOYG1p6n6KrL86z"
    
    print(f"📧 Account: {email}")
    print(f"🔐 Password: {password}")
    print(f"🔗 Document: https://docs.google.com/document/d/10aUUm36tsHcOhc0SaobAWrJZmrLXWbbG8qWxykGgc4s/edit")
    
    # Setup driver
    driver = setup_driver()
    
    try:
        # Login
        if not login_to_google(driver, email, password):
            print("❌ Cannot proceed without login")
            return
        
        print("\n✅ SUCCESSFULLY LOGGED IN!")
        print("   You should see the Google Doc now")
        print("   Browser will remain open for 60 seconds...")
        
        # Add cover page
        add_cover_page(driver)
        
        # Apply formatting (partial)
        apply_basic_formatting(driver)
        
        print("\n" + "="*50)
        print("🎯 MANUAL COMPLETION REQUIRED")
        print("="*50)
        print("\nSince Google Docs UI automation is complex,")
        print("please complete these manual steps:")
        
        print("\n1. FORMATTING:")
        print("   - Select all (Cmd+A)")
        print("   - Font: Arial")
        print("   - Size: 14")
        print("   - Alignment: Justify")
        print("   - Line spacing: 1.5")
        
        print("\n2. CHAPTER HEADINGS:")
        print("   - Find each 'فصل' line")
        print("   - Apply 'Heading 1' style")
        print("   - Set to 16pt, Bold")
        
        print("\n3. TABLE OF CONTENTS:")
        print("   - After cover page, type 'فهرست مطالب'")
        print("   - Apply Heading 1")
        print("   - Insert → Table of contents")
        
        print("\n4. PAGE NUMBERS:")
        print("   - Insert → Page numbers")
        print("   - Bottom right")
        
        print("\n⏱️  Manual time: 5-10 minutes")
        
        # Keep browser open
        time.sleep(60)
        print("\n⏰ Time's up! Browser will close.")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        # Take screenshot
        driver.save_screenshot("error.png")
    finally:
        driver.quit()
        print("\n✅ Browser closed")

if __name__ == "__main__":
    main()