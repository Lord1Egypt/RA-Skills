#!/usr/bin/env python3
"""
Word Chapter Merger Automation
Automates adding chapters 4-7 to Word document following university format
"""

import pyautogui
import time
import subprocess
import os
import sys
from pathlib import Path

# Configuration
WORD_DOC = "BSc-project-report-with-chapters5-7.docx"
CHAPTERS = [
    (5, "فصل ۵: پیاده‌سازی لایه سرویس‌های در سطح کاربر"),
    (6, "فصل ۶: پایش، سخت‌سازی امنیتی، آزمون‌ها و تحویل نهایی"),
    (7, "فصل ۷: خلصه، نتیجه‌گیری و کارهای آینده")
]

# Safety features
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5

def check_prerequisites():
    """Check if required files and applications exist"""
    print("🔍 Checking prerequisites...")
    
    # Check if Word document exists
    if not os.path.exists(WORD_DOC):
        print(f"❌ Word document '{WORD_DOC}' not found")
        return False
    
    # Check if chapter text files exist
    for chapter_num, _ in CHAPTERS:
        txt_file = f"chapter{chapter_num}_clean.txt"
        if not os.path.exists(txt_file):
            print(f"❌ Chapter file '{txt_file}' not found")
            return False
    
    print("✅ All prerequisites satisfied")
    return True

def open_word_document():
    """Open the Word document"""
    print(f"📄 Opening Word document: {WORD_DOC}")
    
    try:
        # Open Word document
        subprocess.run(["open", "-a", "Microsoft Word", WORD_DOC], check=True)
        time.sleep(3)  # Wait for Word to load
        
        # Activate Word window
        pyautogui.hotkey('command', 'space')
        time.sleep(0.5)
        pyautogui.typewrite('Microsoft Word')
        time.sleep(0.5)
        pyautogui.press('enter')
        time.sleep(2)
        
        # Maximize window (optional)
        pyautogui.hotkey('command', 'option', 'm')
        time.sleep(1)
        
        return True
    except Exception as e:
        print(f"❌ Failed to open Word: {e}")
        return False

def go_to_end_of_document():
    """Navigate to end of document (after existing chapters)"""
    print("📝 Navigating to end of document...")
    
    # Go to end of document
    pyautogui.hotkey('command', 'end')
    time.sleep(0.5)
    
    # Add some blank lines
    pyautogui.press('enter', presses=2)
    time.sleep(0.5)
    
    return True

def add_chapter(chapter_num, chapter_title):
    """Add a chapter to the Word document"""
    print(f"📖 Adding Chapter {chapter_num}: {chapter_title}")
    
    # Insert page break
    pyautogui.hotkey('command', 'enter')
    time.sleep(0.5)
    
    # Type chapter title
    pyautogui.typewrite(chapter_title)
    time.sleep(0.5)
    
    # Apply Heading 1 style
    pyautogui.hotkey('command', 'option', '1')
    time.sleep(0.5)
    
    # Add blank lines
    pyautogui.press('enter', presses=2)
    time.sleep(0.5)
    
    # Open chapter text file
    txt_file = f"chapter{chapter_num}_clean.txt"
    print(f"   Opening text file: {txt_file}")
    
    subprocess.run(["open", "-a", "TextEdit", txt_file], check=False)
    time.sleep(2)
    
    # Select all and copy
    pyautogui.hotkey('command', 'a')
    time.sleep(0.5)
    pyautogui.hotkey('command', 'c')
    time.sleep(0.5)
    
    # Switch back to Word
    pyautogui.hotkey('command', 'tab')
    time.sleep(1)
    
    # Paste content
    pyautogui.hotkey('command', 'v')
    time.sleep(2)  # Wait for paste to complete
    
    # Apply Heading 2 to section titles
    print(f"   Applying Heading 2 styles to sections...")
    
    # Find and format section headers (like ۵.۱, ۵.۲, etc.)
    for section in range(1, 9):  # Assuming up to 8 sections per chapter
        # Find section
        pyautogui.hotkey('command', 'f')
        time.sleep(0.5)
        
        # Type section number in Persian
        if chapter_num == 5:
            section_num = f"۵.{section}"
        elif chapter_num == 6:
            section_num = f"۶.{section}"
        elif chapter_num == 7:
            # Chapter 7 has different numbering
            if section == 1:
                section_num = "۷-۱"
            elif section == 2:
                section_num = "۷-۲"
            elif section == 3:
                section_num = "۷-۳"
            else:
                break
        
        pyautogui.typewrite(section_num)
        time.sleep(0.5)
        pyautogui.press('enter')
        time.sleep(0.5)
        
        # Apply Heading 2
        pyautogui.hotkey('command', 'option', '2')
        time.sleep(0.5)
        
        # Close find dialog
        pyautogui.press('escape')
        time.sleep(0.5)
    
    # Add space after chapter
    pyautogui.press('enter', presses=2)
    time.sleep(0.5)
    
    print(f"✅ Chapter {chapter_num} added successfully")
    return True

def apply_university_formatting():
    """Apply university formatting guidelines"""
    print("🎓 Applying university formatting...")
    
    # Note: This would need to be customized based on the PDF guidelines
    # For now, we'll apply some basic formatting
    
    # Go to beginning of document
    pyautogui.hotkey('command', 'home')
    time.sleep(0.5)
    
    # Update table of contents (if exists)
    # This is a manual step that depends on document structure
    print("   ⚠️  Please manually update Table of Contents")
    print("   ⚠️  Check formatting against university PDF guide")
    
    return True

def main():
    """Main automation function"""
    print("=" * 60)
    print("WORD CHAPTER MERGER AUTOMATION")
    print("=" * 60)
    
    # Check prerequisites
    if not check_prerequisites():
        print("❌ Please fix prerequisites and run again")
        return
    
    # Confirmation
    print("\n⚠️  WARNING: This will automate Word operations")
    print("⚠️  Make sure Word is NOT currently editing important documents")
    print("⚠️  Keep hands away from keyboard/mouse during automation")
    
    response = input("\nContinue? (y/n): ").strip().lower()
    if response != 'y':
        print("❌ Automation cancelled")
        return
    
    print("\n🚀 Starting automation in 5 seconds...")
    print("   Move mouse to top-left corner to abort")
    time.sleep(5)
    
    try:
        # Step 1: Open Word document
        if not open_word_document():
            return
        
        # Step 2: Go to end of document
        go_to_end_of_document()
        
        # Step 3: Add each chapter
        for chapter_num, chapter_title in CHAPTERS:
            if not add_chapter(chapter_num, chapter_title):
                print(f"❌ Failed to add chapter {chapter_num}")
                break
        
        # Step 4: Apply formatting
        apply_university_formatting()
        
        print("\n" + "=" * 60)
        print("✅ AUTOMATION COMPLETE")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Review the document for formatting")
        print("2. Update Table of Contents (References → Update Table)")
        print("3. Check against university PDF guidelines")
        print("4. Save final version")
        
    except pyautogui.FailSafeException:
        print("\n❌ Automation aborted (mouse moved to corner)")
    except KeyboardInterrupt:
        print("\n❌ Automation interrupted by user")
    except Exception as e:
        print(f"\n❌ Error during automation: {e}")
    
    print("\n💡 Tip: Run 'open ~/Downloads/BSc-Projects-Docs--1401/BSc-project-report-format.pdf'")
    print("      to open the university formatting guide")

if __name__ == "__main__":
    main()