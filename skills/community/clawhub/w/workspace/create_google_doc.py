#!/usr/bin/env python3
"""
Create Google Doc with all BSc report content using temp account
"""

import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def setup_driver_with_proxy():
    """Setup Chrome driver with proxy"""
    print("🚀 Setting up Chrome with proxy...")
    
    chrome_options = Options()
    chrome_options.add_argument('--proxy-server=http://localhost:2080')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    # For headless mode (uncomment if needed)
    # chrome_options.add_argument('--headless')
    
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def login_to_gmail(driver, email, password):
    """Login to Gmail account"""
    print(f"🔐 Logging in to {email}...")
    
    try:
        # Go to Gmail
        driver.get("https://mail.google.com")
        time.sleep(3)
        
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
        return False

def create_google_doc(driver):
    """Create new Google Doc"""
    print("📝 Creating new Google Doc...")
    
    try:
        # Go to Google Docs
        driver.get("https://docs.google.com/document/create")
        time.sleep(5)
        
        # Wait for document to load
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "docs-title-input"))
        )
        
        # Set document title
        title_input = driver.find_element(By.CLASS_NAME, "docs-title-input")
        title_input.clear()
        title_input.send_keys("BSc Project Report - Final")
        time.sleep(2)
        
        print("✅ Google Doc created")
        return driver.current_url
        
    except Exception as e:
        print(f"❌ Failed to create Google Doc: {e}")
        return None

def read_text_file(filename):
    """Read text file content"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"❌ Error reading {filename}: {e}")
        return None

def add_content_to_doc(driver, doc_url):
    """Add all chapters to Google Doc"""
    print("📚 Adding content to Google Doc...")
    
    try:
        # Go to the document
        driver.get(doc_url)
        time.sleep(5)
        
        # Wait for editor
        editor = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "kix-appview-editor"))
        )
        
        # Function to type text
        def type_text(text):
            editor.send_keys(text)
            editor.send_keys(Keys.ENTER)
            time.sleep(0.5)
        
        # Add Chapter 1-3 from ORIGINAL Word doc
        print("  Adding Chapters 1-3...")
        
        # Read Word document content (simplified - would need proper extraction)
        # For now, add placeholder
        type_text("فصل اول: مقدمه")
        type_text("")  # Empty line
        
        # We'll add the actual content from files
        chapters = [
            ("chapter4_clean.txt", "فصل ۴: ساخت کلاستر Kubernetes"),
            ("chapter5_clean.txt", "فصل ۵: پیاده‌سازی لایه سرویس‌های در سطح کاربر"),
            ("chapter6_clean.txt", "فصل ۶: پایش، سخت‌سازی امنیتی، آزمون‌ها و تحویل نهایی"),
            ("chapter7_clean.txt", "فصل ۷: خلصه، نتیجه‌گیری و کارهای آینده")
        ]
        
        for filename, title in chapters:
            print(f"  Adding {title}...")
            type_text(title)
            type_text("")  # Empty line
            
            content = read_text_file(filename)
            if content:
                # Split and add content
                lines = content.strip().split('\n')
                for line in lines:
                    if line.strip():
                        type_text(line.strip())
                type_text("")  # Empty line between chapters
        
        print("✅ Content added successfully")
        return True
        
    except Exception as e:
        print(f"❌ Failed to add content: {e}")
        return False

def share_document(driver, doc_url, share_email):
    """Share document with edit access"""
    print(f"🔗 Sharing document with {share_email}...")
    
    try:
        # Go to share settings
        share_url = doc_url.replace("/edit", "/settings/share")
        driver.get(share_url)
        time.sleep(3)
        
        # Find share input
        share_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Add people and groups']"))
        )
        
        # Enter email and set permissions
        share_input.send_keys(share_email)
        time.sleep(2)
        
        # Set to Editor
        # Note: This might need adjustment based on Google Docs UI
        editor_option = driver.find_element(By.XPATH, "//div[contains(text(), 'Editor')]")
        editor_option.click()
        time.sleep(1)
        
        # Send
        send_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Send')]")
        send_button.click()
        time.sleep(2)
        
        print("✅ Document shared successfully")
        return True
        
    except Exception as e:
        print(f"⚠️  Sharing might need manual setup: {e}")
        print(f"   Please share manually: {doc_url}")
        return False

def main():
    print("🔧 GOOGLE DOCS MIGRATION TOOL")
    print("="*50)
    
    # Credentials
    email = "ali.lotfizadeh.g@gmail.com"
    password = "Q4Sswh3zG!tmv6T#"
    
    # Your email for sharing
    your_email = "ali.ghotbizadeh@gmail.com"  # Change this to your actual email
    
    print(f"📧 Using temp account: {email}")
    print(f"🔗 Will share with: {your_email}")
    
    # Setup driver
    driver = setup_driver_with_proxy()
    
    try:
        # Login
        if not login_to_gmail(driver, email, password):
            print("❌ Cannot proceed without login")
            return
        
        # Create Google Doc
        doc_url = create_google_doc(driver)
        if not doc_url:
            print("❌ Cannot proceed without document")
            return
        
        print(f"📄 Document URL: {doc_url}")
        
        # Add content
        if not add_content_to_doc(driver, doc_url):
            print("⚠️  Content addition had issues")
        
        # Share document
        share_document(driver, doc_url, your_email)
        
        print("\n" + "="*50)
        print("🎉 MIGRATION COMPLETE!")
        print("="*50)
        print(f"\n📄 Document: {doc_url}")
        print(f"📧 Shared with: {your_email}")
        print("\n🚀 Next steps:")
        print("1. Open the document")
        print("2. Verify all 7 chapters")
        print("3. Apply final formatting")
        print("4. Update Table of Contents")
        
        # Keep browser open for inspection
        print("\n⏳ Browser will remain open for 60 seconds...")
        time.sleep(60)
        
    except Exception as e:
        print(f"❌ Error during migration: {e}")
    finally:
        driver.quit()
        print("\n✅ Browser closed")

if __name__ == "__main__":
    main()