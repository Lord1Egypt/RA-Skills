#!/bin/bash

echo "📝 MANUAL CHAPTER ADDITION WITH VERIFICATION"
echo "==========================================="

echo ""
echo "📋 Available chapter files:"
echo "1. chapter5_clean.txt - فصل ۵: پیاده‌سازی لایه سرویس‌های در سطح کاربر"
echo "2. chapter6_clean.txt - فصل ۶: پایش، سخت‌سازی امنیتی، آزمون‌ها و تحویل نهایی"
echo "3. chapter7_clean.txt - فصل ۷: خلصه، نتیجه‌گیری و کارهای آینده"
echo ""

# Function to add one chapter with verification
add_chapter_manual() {
    local chapter_num=$1
    local title=$2
    local filename=$3
    
    echo ""
    echo "📖 STEP $chapter_num: Adding $title"
    echo "────────────────────────────────────"
    
    # Copy content to clipboard
    echo "📋 Copying $filename to clipboard..."
    if [ -f "$filename" ]; then
        cat "$filename" | pbcopy
        echo "✅ Content copied to clipboard"
        echo "   Size: $(wc -c < "$filename") bytes"
        echo "   Lines: $(wc -l < "$filename")"
    else
        echo "❌ File not found: $filename"
        return 1
    fi
    
    echo ""
    echo "🖥️  MANUAL STEPS REQUIRED:"
    echo "1. Make sure Microsoft Word is open and active"
    echo "2. Go to END of document (Cmd+End or scroll)"
    echo "3. Insert → Page Break (or Cmd+Enter)"
    echo "4. Type the title: \"$title\""
    echo "5. Apply Style: 'Heading 1' (Cmd+Option+1)"
    echo "6. Press Enter for new paragraph"
    echo "7. Paste content (Cmd+V)"
    echo "8. Format subheadings (e.g., '۵.۱') as 'Heading 2'"
    echo ""
    
    read -p "⏳ Press Enter AFTER you've completed adding Chapter $chapter_num... " dummy
    
    echo "✅ Chapter $chapter_num marked as added"
    return 0
}

# Start the process
echo "🚀 Starting manual chapter addition..."
echo "We'll add one chapter at a time with verification."
echo ""

# Chapter 5
add_chapter_manual 5 "فصل ۵: پیاده‌سازی لایه سرویس‌های در سطح کاربر" "chapter5_clean.txt"

# Wait and verify
echo ""
read -p "📝 Ready for Chapter 6? Press Enter to continue... " dummy

# Chapter 6
add_chapter_manual 6 "فصل ۶: پایش، سخت‌سازی امنیتی، آزمون‌ها و تحویل نهایی" "chapter6_clean.txt"

# Wait and verify
echo ""
read -p "📝 Ready for Chapter 7? Press Enter to continue... " dummy

# Chapter 7
add_chapter_manual 7 "فصل ۷: خلصه، نتیجه‌گیری و کارهای آینده" "chapter7_clean.txt"

# Final steps
echo ""
echo "🎉 ALL CHAPTERS READY FOR ADDITION!"
echo "==================================="
echo ""
echo "📋 Verification checklist:"
echo "1. ✅ Chapter 5: Copied to clipboard"
echo "2. ✅ Chapter 6: Copied to clipboard"
echo "3. ✅ Chapter 7: Copied to clipboard"
echo ""
echo "💾 After adding all chapters:"
echo "1. Update Table of Contents (References → Update Table)"
echo "2. Check page numbering"
echo "3. Save document (Cmd+S)"
echo "4. Check file size increased significantly"
echo ""
echo "⏱️  Estimated time: 15-20 minutes"
echo ""
echo "🔧 Troubleshooting:"
echo "- If paste doesn't work: Select all in text file → Copy → Paste in Word"
echo "- If formatting lost: Use Format Painter tool"
echo "- If headings wrong: Reapply 'Heading 1' and 'Heading 2' styles"