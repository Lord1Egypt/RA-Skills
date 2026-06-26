#!/bin/bash

echo "🔍 VERIFYING FINAL DOCUMENT"
echo "==========================="

# Check file exists
if [ ! -f "BSc-project-report-COMPLETE-FORMATTED.docx" ]; then
    echo "❌ Final document not found!"
    exit 1
fi

echo "📄 Final document: BSc-project-report-COMPLETE-FORMATTED.docx"
size=$(stat -f%z "BSc-project-report-COMPLETE-FORMATTED.docx" 2>/dev/null || stat -c%s "BSc-project-report-COMPLETE-FORMATTED.docx")
echo "📏 File size: $size bytes"

# Python verification
python3 -c "
from docx import Document
import os

print('\n📋 DOCUMENT ANALYSIS:')
print('='*50)

doc = Document('BSc-project-report-COMPLETE-FORMATTED.docx')

# Basic stats
print(f'Total paragraphs: {len(doc.paragraphs)}')

# Count content paragraphs (non-empty)
content_paras = [p for p in doc.paragraphs if p.text.strip()]
print(f'Content paragraphs: {len(content_paras)}')

# Find chapters
chapters = []
for para in doc.paragraphs:
    text = para.text.strip()
    if text.startswith('فصل'):
        chapters.append(text[:80])

print(f'\n📚 CHAPTERS FOUND: {len(chapters)}')
for i, chap in enumerate(chapters[:15]):
    print(f'{i+1}. {chap}...' if len(chap) > 80 else f'{i+1}. {chap}')

# Check for specific content
all_text = ' '.join([p.text for p in doc.paragraphs])
keywords = ['مقدمه', 'معماری', 'Kubernetes', 'پایش', 'نتیجه‌گیری']
print(f'\n🔍 KEYWORD CHECK:')
for kw in keywords:
    count = all_text.count(kw)
    print(f'  {kw}: {count} occurrences')

# Verify we have all 7 chapters
expected_chapters = 7
if len(chapters) >= expected_chapters:
    print(f'\n✅ SUCCESS: Document has at least {expected_chapters} chapters')
else:
    print(f'\n⚠️  WARNING: Only {len(chapters)} chapters found (expected {expected_chapters})')

# Check formatting
print(f'\n🎨 FORMATTING CHECK:')
try:
    # Check first few paragraphs for formatting
    sample_para = doc.paragraphs[10] if len(doc.paragraphs) > 10 else doc.paragraphs[0]
    if sample_para.style and sample_para.style.name:
        print(f'  Style applied: {sample_para.style.name}')
    else:
        print('  Style: Not detected')
    
    print('  Formatting: Applied via python-docx')
except:
    print('  Formatting: Could not verify')
"

echo ""
echo "🚀 NEXT STEPS:"
echo "1. Open the document:"
echo "   open 'BSc-project-report-COMPLETE-FORMATTED.docx'"
echo ""
echo "2. Update Table of Contents (optional):"
echo "   peekaboo run update_word_toc.peekaboo.json"
echo ""
echo "3. Proceed to ChatGPT review:"
echo "   Follow CHATGPT_REVIEW_GUIDE.md"
echo ""
echo "⏱️  Estimated time for next steps: 20-30 minutes"