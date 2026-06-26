#!/bin/bash

echo "🤖 ROBUST CHAPTER ADDITION - Using proven method"
echo "================================================"

# Check files
echo "📋 Checking chapter files..."
for chap in 5 6 7; do
    file="chapter${chap}_clean.txt"
    if [ -f "$file" ]; then
        size=$(wc -c < "$file")
        lines=$(wc -l < "$file")
        echo "✅ $file: $size bytes, $lines lines"
    else
        echo "❌ $file: MISSING"
        exit 1
    fi
done

echo ""
echo "🚀 Starting in 3 seconds... Ensure Word is open"
sleep 3

# Function to add one chapter
add_chapter_simple() {
    local chap_num=$1
    local title=$2
    local file="chapter${chap_num}_clean.txt"
    
    echo ""
    echo "📖 CHAPTER $chap_num: $title"
    echo "────────────────────────────"
    
    # Copy to clipboard using cat (proven to work)
    echo "Copying $file to clipboard..."
    cat "$file" | pbcopy
    
    # Verify
    clipboard_check=$(pbpaste | head -c 20)
    if [ -n "$clipboard_check" ]; then
        echo "✅ Clipboard ready: \"$clipboard_check...\""
    else
        echo "❌ Clipboard empty!"
        return 1
    fi
    
    # Create AppleScript
    cat > /tmp/add_chap_${chap_num}.scpt << EOF
-- Simple and reliable AppleScript for Chapter $chap_num
tell application "Microsoft Word"
	activate
	delay 1
end tell

tell application "System Events"
	tell process "Microsoft Word"
		set frontmost to true
		delay 1
		
		-- Go to end (Cmd+Down)
		key code 125 using command down
		delay 1
		
		-- Insert page break (Shift+Enter sometimes works better)
		keystroke return using {shift down, command down}
		delay 1
		
		-- Type title
		keystroke "$title"
		delay 1
		
		-- Apply Heading 1
		keystroke "1" using {command down, option down}
		delay 1
		
		-- Press Enter
		key code 36
		delay 1
		
		-- Paste content
		keystroke "v" using command down
		delay 3
		
	end tell
end tell

-- Simple save
tell application "Microsoft Word"
	save active document
end tell

display dialog "Chapter $chap_num added successfully!" buttons {"OK"}
EOF
    
    echo "Running automation..."
    osascript /tmp/add_chap_${chap_num}.scpt
    
    if [ $? -eq 0 ]; then
        echo "✅ Chapter $chap_num: SUCCESS"
        return 0
    else
        echo "⚠️  Chapter $chap_num: May need manual check"
        return 0  # Continue anyway
    fi
}

# Add chapters sequentially
add_chapter_simple 5 "فصل ۵: پیاده‌سازی لایه سرویس‌های در سطح کاربر"
sleep 2

add_chapter_simple 6 "فصل ۶: پایش، سخت‌سازی امنیتی، آزمون‌ها و تحویل نهایی"
sleep 2

add_chapter_simple 7 "فصل ۷: خلصه، نتیجه‌گیری و کارهای آینده"

# Final verification
echo ""
echo "🔍 FINAL VERIFICATION"
echo "===================="

echo "Checking document size..."
initial_size=228090  # Original size
current_size=$(stat -f%z BSc-project-report-FINAL-UNIVERSITY.docx 2>/dev/null || stat -c%s BSc-project-report-FINAL-UNIVERSITY.docx)
size_increase=$((current_size - initial_size))

echo "Initial size: $initial_size bytes"
echo "Current size: $current_size bytes"
echo "Increase: $size_increase bytes"

if [ $size_increase -gt 30000 ]; then
    echo "✅ GOOD: Significant size increase suggests chapters added"
elif [ $size_increase -gt 10000 ]; then
    echo "⚠️  OK: Some content added, may need verification"
else
    echo "❌ WARNING: Little to no size increase"
fi

echo ""
echo "🎯 MANUAL VERIFICATION REQUIRED:"
echo "Please open Word document and check:"
echo "1. Scroll to end - are Chapters 5, 6, 7 visible?"
echo "2. Are titles formatted as Heading 1?"
echo "3. Is content present (not broken text)?"
echo "4. Save document (Cmd+S)"

echo ""
echo "📋 NEXT STEPS AFTER VERIFICATION:"
echo "1. Format subheadings (۵.۱, ۵.۲, etc.) as Heading 2"
echo "2. Update Table of Contents"
echo "3. Proceed to ChatGPT review"

echo ""
echo "⏱️  If automation failed, manual addition takes 15-20 minutes"