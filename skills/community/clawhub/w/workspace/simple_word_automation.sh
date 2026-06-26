#!/bin/bash

# Simple Word Automation using AppleScript
# This script helps automate adding chapters to Word

echo "=== Simple Word Chapter Automation ==="
echo ""
echo "This script will:"
echo "1. Open Word document"
echo "2. Open chapter text files"
echo "3. Provide step-by-step instructions"
echo ""

# Step 1: Open all necessary files
echo "📂 Opening files..."
open -a "Microsoft Word" "BSc-project-report-with-chapters5-7.docx"
sleep 2

open -a "TextEdit" "chapter5_clean.txt"
open -a "TextEdit" "chapter6_clean.txt"
open -a "TextEdit" "chapter7_clean.txt"
sleep 1

# Step 2: Open formatting guide
echo "📖 Opening university formatting guide..."
open ~/Downloads/BSc-Projects-Docs--1401/BSc-project-report-format.pdf
sleep 1

echo ""
echo "✅ All files are now open!"
echo ""
echo "📋 MANUAL STEPS TO FOLLOW:"
echo "=========================="
echo ""
echo "1. IN WORD DOCUMENT:"
echo "   - Go to end of Chapter 4 (Cmd + End)"
echo "   - Insert → Page Break (Cmd + Enter)"
echo ""
echo "2. FOR CHAPTER 5:"
echo "   - Type: 'فصل ۵: پیاده‌سازی لایه سرویس‌های در سطح کاربر'"
echo "   - Apply Style: Heading 1 (Cmd + Option + 1)"
echo "   - Switch to TextEdit with Chapter 5"
echo "   - Select All (Cmd + A) and Copy (Cmd + C)"
echo "   - Switch back to Word and Paste (Cmd + V)"
echo "   - Apply Heading 2 to sections ۵.۱ through ۵.۸"
echo ""
echo "3. REPEAT FOR CHAPTERS 6 & 7:"
echo "   - Same steps with appropriate titles"
echo ""
echo "4. FINAL FORMATTING:"
echo "   - Update Table of Contents"
echo "   - Check against PDF formatting guide"
echo "   - Save document"
echo ""
echo "💡 TIP: Use Cmd + Tab to switch between applications"
echo "💡 TIP: Use Cmd + F to find section numbers for styling"
echo ""
echo "The script will now wait for you to complete these steps..."
echo "Press Enter when you're ready to check formatting..."

read -p "Press Enter to continue..."

# AppleScript to help with formatting check
osascript <<EOF
tell application "Microsoft Word"
    activate
    display dialog "FORMATTING CHECKLIST:" & return & return & \
    "1. All chapters 5-7 added?" & return & \
    "2. Headings styled correctly?" & return & \
    "3. Table of Contents updated?" & return & \
    "4. Page numbers correct?" & return & \
    "5. Format matches PDF guide?" & return & return & \
    "Open PDF guide for comparison?" buttons {"Open PDF", "Done"} default button 1
    if button returned of result is "Open PDF" then
        tell application "Finder"
            open POSIX file "/Users/alighotbizadeh/Downloads/BSc-Projects-Docs--1401/BSc-project-report-format.pdf"
        end tell
    end if
end tell
EOF

echo ""
echo "=== Automation Complete ==="
echo "Your document should now have chapters 5-7 added."
echo "Remember to save with a final name like: BSc-project-report-FINAL.docx"