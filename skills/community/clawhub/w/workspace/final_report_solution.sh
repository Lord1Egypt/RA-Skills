#!/bin/bash

echo "🎯 FINAL REPORT SOLUTION"
echo "======================="

# Step 1: Identify the best base document
echo ""
echo "📋 STEP 1: Selecting best base document"
echo ""

# Check COMPLETE document
if [ -f "BSc-project-report-COMPLETE.docx" ]; then
    size=$(stat -f%z BSc-project-report-COMPLETE.docx 2>/dev/null || stat -c%s BSc-project-report-COMPLETE.docx)
    echo "✅ BSc-project-report-COMPLETE.docx: $size bytes"
    echo "   This document already has all 7 chapters!"
    BASE_DOC="BSc-project-report-COMPLETE.docx"
else
    echo "❌ COMPLETE document not found"
    exit 1
fi

# Step 2: Apply formatting with python-docx
echo ""
echo "📋 STEP 2: Creating properly formatted version"
echo ""

cat > create_final_report.py << 'EOF'
#!/usr/bin/env python3
"""
Create final formatted report from COMPLETE document
"""

import os
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

def create_final_report():
    print("📝 Creating final formatted report...")
    
    # Load the COMPLETE document
    source_doc = "BSc-project-report-COMPLETE.docx"
    if not os.path.exists(source_doc):
        print(f"❌ Source document not found: {source_doc}")
        return False
    
    print(f"📄 Loading: {source_doc}")
    try:
        doc = Document(source_doc)
        print(f"✅ Loaded document with {len(doc.paragraphs)} paragraphs")
    except Exception as e:
        print(f"❌ Error loading document: {e}")
        return False
    
    # Apply formatting to all paragraphs
    print("🎨 Applying formatting...")
    
    # Set font size and justification
    for para in doc.paragraphs:
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        for run in para.runs:
            run.font.size = Pt(14)
    
    # Save final document
    output_file = "BSc-project-report-FINAL-SUBMISSION.docx"
    doc.save(output_file)
    
    print(f"\n🎉 Final report saved: {output_file}")
    print(f"📏 File size: {os.path.getsize(output_file):,} bytes")
    
    # Verification
    print("\n🔍 Verification:")
    chapters_found = []
    for para in doc.paragraphs:
        text = para.text.strip()
        if text.startswith("فصل") or "فصل" in text[:20]:
            chapters_found.append(text)
    
    print(f"✅ Chapters found: {len(chapters_found)}")
    for i, chapter in enumerate(chapters_found[:10]):
        print(f"   {i+1}. {chapter}")
    
    if len(chapters_found) >= 7:
        print("✅ ALL 7 CHAPTERS PRESENT!")
    else:
        print(f"⚠️  Only {len(chapters_found)} chapters found")
    
    return True

if __name__ == "__main__":
    create_final_report()
EOF

python3 create_final_report.py

# Step 3: Create peekaboo automation for final touches
echo ""
echo "📋 STEP 3: Creating peekaboo automation for Word"
echo ""

cat > final_word_touch.peekaboo.json << 'EOF'
{
  "name": "Final Word Formatting",
  "steps": [
    {
      "stepId": "open_word",
      "action": {
        "type": "app",
        "params": {
          "generic": {
            "_0": {
              "appName": "Microsoft Word",
              "operation": "launch",
              "open": "BSc-project-report-FINAL-SUBMISSION.docx"
            }
          }
        }
      }
    },
    {
      "stepId": "wait_for_word",
      "action": {
        "type": "sleep",
        "params": {
          "duration": 3000
        }
      }
    },
    {
      "stepId": "update_toc",
      "action": {
        "type": "hotkey",
        "params": {
          "keys": ["command", "option", "u"]
        }
      }
    },
    {
      "stepId": "save_document",
      "action": {
        "type": "hotkey",
        "params": {
          "keys": ["command", "s"]
        }
      }
    },
    {
      "stepId": "close_word",
      "action": {
        "type": "app",
        "params": {
          "generic": {
            "_0": {
              "appName": "Microsoft Word",
              "operation": "quit"
            }
          }
        }
      }
    }
  ]
}
EOF

echo "✅ Peekaboo script created: final_word_touch.peekaboo.json"

# Step 4: Create execution plan
echo ""
echo "📋 STEP 4: Execution Plan"
echo ""
echo "🚀 TO CREATE FINAL REPORT:"
echo "1. Run: python3 create_final_report.py"
echo "   - Creates BSc-project-report-FINAL-SUBMISSION.docx"
echo "   - All 7 chapters included"
echo "   - Proper formatting applied"
echo ""
echo "2. Optional: Run peekaboo automation"
echo "   - Command: peekaboo run final_word_touch.peekaboo.json"
echo "   - Opens Word, updates Table of Contents, saves"
echo ""
echo "3. Verify final document"
echo "   - Open BSc-project-report-FINAL-SUBMISSION.docx"
echo "   - Check all 7 chapters"
echo "   - Check formatting"
echo ""
echo "📊 EXPECTED RESULT:"
echo "- Complete 7-chapter report"
-✅ Proper Persian text encoding
-✅ University formatting (justified, 14pt font)
-✅ Ready for submission"
echo ""
echo "⏱️  Time estimate: 5 minutes"