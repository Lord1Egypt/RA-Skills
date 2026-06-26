#!/usr/bin/env python3
"""
Word Automation using pyautogui for adding chapters 5-7
"""

import subprocess
import time
import os
import sys

def check_dependencies():
    """Check if pyautogui is installed"""
    try:
        import pyautogui
        print("✅ pyautogui is installed")
        return True
    except ImportError:
        print("❌ pyautogui not installed")
        print("Installing with pip...")
        try:
            # Use proxy if provided
            proxy = "http://localhost:2080"
            subprocess.run([
                sys.executable, "-m", "pip", "install", "pyautogui",
                "--proxy", proxy, "--user"
            ], check=True)
            print("✅ pyautogui installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install pyautogui: {e}")
            return False

def copy_to_clipboard(text):
    """Copy text to clipboard"""
    process = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
    process.communicate(text.encode('utf-8'))

def read_chapter_file(filename):
    """Read chapter content from file"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"❌ File not found: {filename}")
        return None

def main():
    print("🤖 Word Automation for Chapters 5-7")
    print("=" * 40)
    
    # Check dependencies
    if not check_dependencies():
        print("Please install pyautogui manually: pip install pyautogui")
        return
    
    import pyautogui
    
    # Check if chapter files exist
    chapters = [
        ("chapter5_clean.txt", "فصل ۵: پیاده‌سازی لایه سرویس‌های در سطح کاربر"),
        ("chapter6_clean.txt", "فصل ۶: پایش، سخت‌سازی امنیتی، آزمون‌ها و تحویل نهایی"),
        ("chapter7_clean.txt", "فصل ۷: خلصه، نتیجه‌گیری و کارهای آینده")
    ]
    
    print("\n📋 Chapter files:")
    for filename, title in chapters:
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            print(f"✅ {filename} ({size:,} bytes)")
        else:
            print(f"❌ {filename} (MISSING)")
            return
    
    print("\n🚀 Starting automation...")
    print("Please ensure:")
    print("1. Microsoft Word is open with your document")
    print("2. Word window is active/frontmost")
    print("3. You are ready to proceed")
    
    input("\nPress Enter when ready to continue...")
    
    # Pause for safety
    time.sleep(2)
    
    try:
        # Instructions for manual process
        print("\n📝 MANUAL STEPS TO FOLLOW:")
        print("-" * 30)
        
        for i, (filename, title) in enumerate(chapters, 1):
            chapter_num = 4 + i  # Chapters 5, 6, 7
            
            print(f"\n📖 CHAPTER {chapter_num}:")
            print(f"Title: {title}")
            
            # Read chapter content
            content = read_chapter_file(filename)
            if content:
                # Copy to clipboard
                copy_to_clipboard(content)
                print(f"✅ Content copied to clipboard ({len(content)} chars)")
            
            print(f"\nSteps to add:")
            print(f"1. Go to end of current document")
            print(f"2. Insert → Page Break (or Cmd+Enter)")
            print(f"3. Type the title: {title}")
            print(f"4. Apply Style: 'Heading 1' (Cmd+Option+1)")
            print(f"5. Press Enter for new paragraph")
            print(f"6. Paste content (Cmd+V)")
            print(f"7. Format subheadings (e.g., '۵.۱') as 'Heading 2'")
            
            if i < len(chapters):
                input(f"\nPress Enter when Chapter {chapter_num} is added...")
            else:
                print(f"\n✅ Last chapter! Complete and save document (Cmd+S)")
        
        print("\n" + "=" * 40)
        print("🎉 ALL CHAPTERS READY FOR ADDITION!")
        print("=" * 40)
        
        print("\n📋 Summary:")
        print("• Chapter 5: Copied to clipboard")
        print("• Chapter 6: Copied to clipboard") 
        print("• Chapter 7: Copied to clipboard")
        
        print("\n🚀 Next after adding chapters:")
        print("1. Update Table of Contents")
        print("2. Check page numbering")
        print("3. Save final document")
        print("4. Proceed to ChatGPT review")
        
    except KeyboardInterrupt:
        print("\n⏹️ Automation interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()