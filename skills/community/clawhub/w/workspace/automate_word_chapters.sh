#!/bin/bash

echo "🤖 Starting Word Automation for Chapters 5-7"
echo "=========================================="

# Step 1: Copy chapter contents to clipboard
echo "📋 Step 1: Copying chapter contents to clipboard..."

# Copy Chapter 5
if [ -f "chapter5_clean.txt" ]; then
    cat chapter5_clean.txt | pbcopy
    echo "✅ Chapter 5 copied to clipboard"
else
    echo "❌ chapter5_clean.txt not found"
    exit 1
fi

# Step 2: Create AppleScript
echo "📝 Step 2: Creating AppleScript for automation..."

cat > /tmp/word_automation.scpt << 'EOF'
-- Word Automation Script
tell application "Microsoft Word"
	activate
	delay 2
	
	-- Go to end of document
	tell active document
		-- Method 1: Try keyboard shortcut
		tell application "System Events"
			keystroke "e" using {command down, shift down}
		end tell
	end tell
	
	delay 1
	
	-- Insert page break
	tell application "System Events"
		keystroke return using command down
	end tell
	
	delay 1
	
	-- Type Chapter 5 title
	tell application "System Events"
		keystroke "فصل ۵: پیاده‌سازی لایه سرویس‌های در سطح کاربر"
		delay 1
		
		-- Apply Heading 1 (Cmd+Option+1)
		keystroke "1" using {command down, option down}
		delay 1
		
		-- Press Enter
		key code 36
		delay 1
		
		-- Paste Chapter 5 content
		keystroke "v" using command down
		delay 2
		
		-- Press Enter for next chapter
		key code 36
		delay 1
		
		-- Insert page break
		keystroke return using command down
		delay 1
		
		-- Type Chapter 6 title
		keystroke "فصل ۶: پایش، سخت‌سازی امنیتی، آزمون‌ها و تحویل نهایی"
		delay 1
		
		-- Apply Heading 1
		keystroke "1" using {command down, option down}
		delay 1
		
		-- Press Enter
		key code 36
		delay 1
	end tell
	
	-- Save document
	save active document
	delay 1
	
	display dialog "Chapters 5-6 added. Please manually paste Chapter 7." buttons {"OK"}
end tell
EOF

echo "✅ AppleScript created"

# Step 3: Run the automation
echo "🚀 Step 3: Running automation..."
echo ""
echo "⚠️  IMPORTANT: Make sure Word document is open and ready"
echo "   The script will:"
echo "   1. Go to end of document"
echo "   2. Add Chapter 5"
echo "   3. Add Chapter 6"
echo "   4. Save"
echo "   5. Prompt for Chapter 7"
echo ""
read -p "Press Enter to continue..." dummy

# Run AppleScript
osascript /tmp/word_automation.scpt

# Step 4: Prepare Chapter 7
echo ""
echo "📋 Step 4: Preparing Chapter 7..."
if [ -f "chapter7_clean.txt" ]; then
    cat chapter7_clean.txt | pbcopy
    echo "✅ Chapter 7 copied to clipboard"
    echo ""
    echo "📝 Instructions for Chapter 7:"
    echo "1. After script completes, you'll be at the end of Chapter 6"
    echo "2. Press Enter to start new paragraph"
    echo "3. Type: فصل ۷: خلصه، نتیجه‌گیری و کارهای آینده"
    echo "4. Apply Heading 1 style (Cmd+Option+1)"
    echo "5. Press Enter"
    echo "6. Paste Chapter 7 content (Cmd+V)"
    echo "7. Save document (Cmd+S)"
else
    echo "❌ chapter7_clean.txt not found"
fi

echo ""
echo "🎉 Automation script ready!"
echo "Run: osascript /tmp/word_automation.scpt"