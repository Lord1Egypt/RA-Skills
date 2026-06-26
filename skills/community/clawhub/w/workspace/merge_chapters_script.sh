#!/bin/bash

# Script to merge markdown chapters into Word document workflow
# Created for Ali Ghotbizadeh's BSc project report

echo "=== BSc Project Report Chapter Merger ==="
echo "Status: Chapters 1-4 manually edited in Word"
echo "Action: Need to add chapters 5-7 from markdown files"
echo ""

# Step 1: Create a copy of the original Word document
ORIGINAL_DOC="~/Documents/University/Final Project/BSc-project-report.docx"
NEW_DOC="BSc-project-report-with-chapters5-7.docx"

echo "1. Please create a copy of your Word document:"
echo "   cp \"$ORIGINAL_DOC\" \"$NEW_DOC\""
echo "   Then open \"$NEW_DOC\" in Microsoft Word"
echo ""

# Step 2: Prepare markdown content for copying
CHAPTERS_DIR="$HOME/Documents/PersonalProjects/report-agent/outputs/chapters"

echo "2. I'll prepare the markdown content for easy copying:"
echo ""

# Create clean text versions of chapters 5-7
for chapter in 5 6 7; do
    echo "   Chapter $chapter ready in: chapter${chapter}_clean.txt"
done

echo ""
echo "3. Manual Steps in Microsoft Word:"
echo "   a. Open the new document in Word"
echo "   b. Go to the end of chapter 4"
echo "   c. Add new page for chapter 5"
echo "   d. Copy content from chapter5_clean.txt"
echo "   e. Apply styles (Heading 1, Heading 2, etc.)"
echo "   f. Repeat for chapters 6 and 7"
echo ""

# Step 3: Create the clean text files
echo "4. Creating clean text files now..."
echo ""

# Function to clean markdown for Word
clean_markdown_for_word() {
    local input_file="$1"
    local output_file="$2"
    
    # Remove markdown formatting, keep structure
    sed 's/^# //g' "$input_file" | \
    sed 's/^## //g' | \
    sed 's/^### //g' | \
    sed 's/\*\*//g' | \
    sed 's/\*//g' | \
    sed 's/`//g' | \
    sed 's/\[.*\]//g' > "$output_file"
    
    echo "   Created: $output_file"
}

# Create clean versions
clean_markdown_for_word "$CHAPTERS_DIR/ch05.md" "chapter5_clean.txt"
clean_markdown_for_word "$CHAPTERS_DIR/ch06.md" "chapter6_clean.txt"
clean_markdown_for_word "$CHAPTERS_DIR/ch07.md" "chapter7_clean.txt"

echo ""
echo "=== Script Complete ==="
echo ""
echo "Next steps:"
echo "1. Run: chmod +x merge_chapters_script.sh"
echo "2. Run: ./merge_chapters_script.sh"
echo "3. Follow the instructions above"
echo ""
echo "For GUI automation, I can use AppleScript to control Word"
echo "Would you like me to create an AppleScript instead?"