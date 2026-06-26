#!/bin/bash

echo "🔍 Debugging Word Automation Issue"
echo "=================================="

# Test 1: Check clipboard content
echo ""
echo "📋 Test 1: Checking clipboard content..."
echo "Current clipboard (first 200 chars):"
pbpaste | head -c 200
echo ""
echo ""

# Test 2: Check if we can type Persian text
echo "📝 Test 2: Testing Persian text input..."
cat > /tmp/test_persian.scpt << 'EOF'
tell application "System Events"
	tell process "Microsoft Word"
		set frontmost to true
		delay 1
		-- Type simple Persian text
		keystroke "تست فارسی"
		delay 1
	end tell
end tell
EOF

echo "Typing 'تست فارسی' into Word..."
osascript /tmp/test_persian.scpt

if [ $? -eq 0 ]; then
	echo "✅ Persian text input works"
else
	echo "❌ Persian text input failed"
fi

# Test 3: Check actual Word content length
echo ""
echo "📄 Test 3: Checking Word document..."
echo "Current file size: $(stat -f%z BSc-project-report-FINAL-UNIVERSITY.docx 2>/dev/null || stat -c%s BSc-project-report-FINAL-UNIVERSITY.docx) bytes"

# Test 4: Manual verification prompt
echo ""
echo "🔍 MANUAL VERIFICATION NEEDED:"
echo "Please open BSc-project-report-FINAL-UNIVERSITY.docx and check:"
echo "1. Scroll to the end - is there any new content?"
echo "2. Look for 'تست فارسی' text"
echo "3. Check if chapters 5-7 were added"
echo ""
echo "📋 What should be at the end:"
echo "- فصل ۵: پیاده‌سازی لایه سرویس‌های در سطح کاربر"
echo "- فصل ۶: پایش، سخت‌سازی امنیتی، آزمون‌ها و تحویل نهایی"
echo "- فصل ۷: خلصه، نتیجه‌گیری و کارهای آینده"