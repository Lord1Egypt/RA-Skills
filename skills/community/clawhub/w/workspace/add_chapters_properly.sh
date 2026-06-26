#!/bin/bash

echo "🔧 PROPER CHAPTER ADDITION - ONE AT A TIME"
echo "=========================================="

# Function to copy chapter and give instructions
add_chapter() {
    local chapter_num=$1
    local title=$2
    local filename=$3
    
    echo ""
    echo "🔄 PREPARING CHAPTER $chapter_num..."
    echo "================================="
    
    # Clear clipboard first
    echo "" | pbcopy
    sleep 1
    
    # Copy the chapter content
    if [ ! -f "$filename" ]; then
        echo "❌ ERROR: File not found: $filename"
        return 1
    fi
    
    echo "📋 Copying $filename to clipboard..."
    cat "$filename" | pbcopy
    
    # Verify copy worked
    clipboard_content=$(pbpaste | head -c 50)
    if [ -z "$clipboard_content" ]; then
        echo "❌ ERROR: Clipboard is empty!"
        return 1
    fi
    
    echo "✅ SUCCESS: Chapter $chapter_num copied to clipboard"
    echo "   First 50 chars: $clipboard_content..."
    echo ""
    
    echo "🎯 INSTRUCTIONS FOR CHAPTER $chapter_num:"
    echo "----------------------------------------"
    echo "1. Make sure Word document is open and active"
    echo "2. Scroll to the VERY END of the document"
    echo "3. Insert → Page Break (or press Cmd+Enter)"
    echo "4. Type this EXACT title:"
    echo "   \"$title\""
    echo "5. Select the title and apply 'Heading 1' style"
    echo "   (Format → Style → Heading 1 OR Cmd+Option+1)"
    echo "6. Press Enter to start a new paragraph"
    echo "7. Paste the chapter content (Cmd+V)"
    echo "8. Find and format subheadings:"
    echo "   - Look for '${chapter_num}.۱', '${chapter_num}.۲', etc."
    echo "   - Select each one and apply 'Heading 2' style"
    echo "9. SAVE the document (Cmd+S)"
    echo ""
    
    read -p "⏳ Press Enter ONLY AFTER you've completed ALL steps above... " dummy
    
    # Verify file size increased
    echo ""
    echo "📊 VERIFICATION:"
    echo "Please check:"
    echo "1. Is the chapter title visible? ✓"
    echo "2. Is the content pasted? ✓"
    echo "3. Are subheadings formatted as Heading 2? ✓"
    echo "4. Is document saved? ✓"
    echo ""
    
    read -p "✅ Confirm Chapter $chapter_num is added correctly (y/n): " confirm
    if [ "$confirm" != "y" ]; then
        echo "⚠️  Please fix Chapter $chapter_num before continuing"
        return 1
    fi
    
    echo "🎉 CHAPTER $chapter_num COMPLETE!"
    return 0
}

echo ""
echo "📁 AVAILABLE CHAPTER FILES:"
echo "1. chapter5_clean.txt - فصل ۵: پیاده‌سازی لایه سرویس‌های در سطح کاربر"
echo "2. chapter6_clean.txt - فصل ۶: پایش، سخت‌سازی امنیتی، آزمون‌ها و تحویل نهایی"
echo "3. chapter7_clean.txt - فصل ۷: خلصه، نتیجه‌گیری و کارهای آینده"
echo ""

echo "🚀 STARTING WITH CHAPTER 5..."
add_chapter 5 "فصل ۵: پیاده‌سازی لایه سرویس‌های در سطح کاربر" "chapter5_clean.txt"

if [ $? -eq 0 ]; then
    echo ""
    echo "➡️  MOVING TO CHAPTER 6..."
    add_chapter 6 "فصل ۶: پایش، سخت‌سازی امنیتی، آزمون‌ها و تحویل نهایی" "chapter6_clean.txt"
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "➡️  MOVING TO CHAPTER 7..."
        add_chapter 7 "فصل ۷: خلصه، نتیجه‌گیری و کارهای آینده" "chapter7_clean.txt"
        
        if [ $? -eq 0 ]; then
            echo ""
            echo "🎉🎉🎉 ALL CHAPTERS ADDED SUCCESSFULLY! 🎉🎉🎉"
            echo ""
            echo "📋 FINAL STEPS:"
            echo "1. Update Table of Contents (References → Update Table)"
            echo "2. Check all page numbers are correct"
            echo "3. Save final version (Cmd+S)"
            echo "4. Check file size (should be > 250KB)"
            echo ""
            echo "📊 EXPECTED RESULT:"
            echo "- Document should have 7 complete chapters"
            echo "- All text should be justified"
            echo "- Headings properly formatted"
            echo "- Ready for ChatGPT review"
        else
            echo "❌ Chapter 7 failed. Please fix manually."
        fi
    else
        echo "❌ Chapter 6 failed. Please fix manually."
    fi
else
    echo "❌ Chapter 5 failed. Please fix manually."
fi