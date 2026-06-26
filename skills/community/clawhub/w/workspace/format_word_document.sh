#!/bin/bash

echo "📝 Word Document Formatting Script"
echo "=================================="

# Get the current directory
CURRENT_DIR=$(pwd)
DOCUMENT="BSc-project-report-FINAL-UNIVERSITY.docx"
DOCUMENT_PATH="$CURRENT_DIR/$DOCUMENT"

echo "Current directory: $CURRENT_DIR"
echo "Document: $DOCUMENT_PATH"

# Check if document exists
if [ ! -f "$DOCUMENT_PATH" ]; then
    echo "❌ Document not found: $DOCUMENT_PATH"
    echo "Creating a copy from original..."
    cp "BSc-project-report-ORIGINAL.docx" "$DOCUMENT_PATH"
fi

echo "✅ Document ready: $DOCUMENT_PATH"

# Create AppleScript for Word formatting
cat > /tmp/format_word.applescript << 'EOF'
tell application "Microsoft Word"
	activate
	
	-- Get the document path from shell
	set docPath to POSIX file "/Users/alighotbizadeh/.openclaw/workspace/BSc-project-report-FINAL-UNIVERSITY.docx"
	
	try
		-- Open the document
		open docPath
		delay 3
		
		display dialog "Document opened. Please wait for formatting..." buttons {"OK"} default button 1 giving up after 2
		
		-- Select all text
		tell active document
			select (content of text object of it)
		end tell
		
		delay 1
		
		-- Apply justification (Cmd+Shift+J)
		tell application "System Events"
			keystroke "j" using {command down, shift down}
		end tell
		
		delay 1
		
		-- Set font size to 14 (Cmd+Shift+P, type 14, Enter)
		tell application "System Events"
			keystroke "p" using {command down, shift down}
			delay 0.5
			keystroke "14"
			delay 0.5
			key code 36 -- Enter key
		end tell
		
		delay 1
		
		-- Save the document (Cmd+S)
		tell application "System Events"
			keystroke "s" using {command down}
		end tell
		
		delay 2
		
		display dialog "Formatting applied successfully!\\n\\n• Text justified\\n• Font size set to 14pt\\n• Document saved" buttons {"OK"} default button 1
		
	on error errMsg
		display dialog "Error: " & errMsg buttons {"OK"} default button 1
	end try
end tell
EOF

echo "📋 Formatting Instructions:"
echo "1. Justify all text paragraphs"
echo "2. Set consistent font size (14pt for body)"
echo "3. Ensure all chapters have same style"
echo "4. Set line spacing to 1.5"

echo ""
echo "🚀 To apply formatting automatically:"
echo "   Run: osascript /tmp/format_word.applescript"
echo ""
echo "🛠️  Or manually in Word:"
echo "   1. Open $DOCUMENT"
echo "   2. Select all text (Cmd+A)"
echo "   3. Justify text (Cmd+Shift+J)"
echo "   4. Set font size to 14pt"
echo "   5. Set line spacing to 1.5"
echo "   6. Save (Cmd+S)"

echo ""
echo "📁 Next steps after formatting:"
echo "   1. Add chapters 5-7 from text files"
echo "   2. Review with ChatGPT"
echo "   3. Add appendix references"
echo "   4. Final review"