#!/bin/bash

echo "🤖 FULL AUTOMATION: Adding Chapters 5-7 to Word"
echo "================================================"

# Check all required files exist
echo "📋 Checking required files..."
required_files=(
    "chapter5_clean.txt"
    "chapter6_clean.txt"
    "chapter7_clean.txt"
)

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        size=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null)
        echo "✅ $file ($size bytes)"
    else
        echo "❌ $file (MISSING)"
        exit 1
    fi
done

echo ""
echo "🚀 Starting automation in 5 seconds..."
echo "Make sure Microsoft Word is open with your document"
sleep 5

# Function to add a chapter
add_chapter() {
    local chapter_num=$1
    local title=$2
    local content_file=$3
    
    echo ""
    echo "📖 Adding Chapter $chapter_num: $title"
    echo "Content from: $content_file"
    
    # Copy content to clipboard
    if [ -f "$content_file" ]; then
        cat "$content_file" | pbcopy
        echo "✅ Content copied to clipboard"
    else
        echo "❌ File not found: $content_file"
        return 1
    fi
    
    # Create AppleScript for this chapter
    cat > /tmp/add_chapter_${chapter_num}.scpt << EOF
tell application "System Events"
	tell process "Microsoft Word"
		set frontmost to true
		delay 1
		
		-- Go to end of document (Cmd+Shift+End)
		keystroke "e" using {command down, shift down}
		delay 1
		
		-- Insert page break (Cmd+Enter)
		keystroke return using command down
		delay 1
		
		-- Type chapter title
		keystroke "$title"
		delay 1
		
		-- Apply Heading 1 style (Cmd+Option+1)
		keystroke "1" using {command down, option down}
		delay 1
		
		-- Press Enter for new paragraph
		key code 36
		delay 1
		
		-- Paste chapter content (Cmd+V)
		keystroke "v" using command down
		delay 3
		
	end tell
end tell
EOF
    
    # Run the AppleScript
    echo "Running automation for Chapter $chapter_num..."
    osascript /tmp/add_chapter_${chapter_num}.scpt
    
    if [ $? -eq 0 ]; then
        echo "✅ Chapter $chapter_num added successfully"
        return 0
    else
        echo "❌ Failed to add Chapter $chapter_num"
        return 1
    fi
}

# Add Chapter 5
add_chapter 5 "فصل ۵: پیاده‌سازی لایه سرویس‌های در سطح کاربر" "chapter5_clean.txt"

# Wait a moment between chapters
sleep 2

# Add Chapter 6  
add_chapter 6 "فصل ۶: پایش، سخت‌سازی امنیتی، آزمون‌ها و تحویل نهایی" "chapter6_clean.txt"

# Wait a moment between chapters
sleep 2

# Add Chapter 7
add_chapter 7 "فصل ۷: خلصه، نتیجه‌گیری و کارهای آینده" "chapter7_clean.txt"

# Final save and completion
echo ""
echo "💾 Saving final document..."

cat > /tmp/final_save.scpt << 'EOF'
tell application "Microsoft Word"
	activate
	delay 1
	save active document
	display dialog "✅ ALL CHAPTERS ADDED SUCCESSFULLY!

Chapters 5-7 have been added to the document.

Next steps:
1. Update Table of Contents
2. Check page numbering
3. Review formatting
4. Proceed to ChatGPT review" buttons {"OK"} default button 1
end tell
EOF

osascript /tmp/final_save.scpt

echo ""
echo "🎉 AUTOMATION COMPLETE!"
echo "========================"
echo ""
echo "📋 What was done:"
echo "1. ✅ Chapter 5 added: پیاده‌سازی لایه سرویس‌های در سطح کاربر"
echo "2. ✅ Chapter 6 added: پایش، سخت‌سازی امنیتی، آزمون‌ها و تحویل نهایی"
echo "3. ✅ Chapter 7 added: خلصه، نتیجه‌گیری و کارهای آینده"
echo "4. ✅ Document saved"
echo ""
echo "🚀 Next steps:"
echo "1. Update Table of Contents in Word"
echo "2. Format subheadings (۵.۱, ۵.۲, etc.) as 'Heading 2'"
echo "3. Proceed to ChatGPT review (Step 4)"
echo ""
echo "⏱️  Estimated time for next steps: 10-15 minutes"