# Word Document Chapter Merge Workflow

## Current Status
- ✅ Chapters 1-4: Already manually edited in Word document
- 📁 Chapters 5-7: Available as markdown files
- 📄 Format guide: `~/Downloads/BSc-Projects-Docs--1401/BSc-project-report-format.pdf`

## Files Created

### 1. Clean Text Files (Ready for Copy-Paste)
- `chapter5_clean.txt` - فصل ۵: پیاده‌سازی لایه سرویس‌های در سطح کاربر
- `chapter6_clean.txt` - فصل ۶: پایش، سخت‌سازی امنیتی، آزمون‌ها و تحویل نهایی  
- `chapter7_clean.txt` - فصل ۷: خلصه، نتیجه‌گیری و کارهای آینده

### 2. Automation Scripts
- `merge_chapters_script.sh` - Bash script to prepare files
- `word_automator.scpt` - AppleScript for Word automation

## Quick Start Guide

### Option 1: Manual Method (Recommended)
```bash
# 1. Run the preparation script
chmod +x merge_chapters_script.sh
./merge_chapters_script.sh

# 2. Copy your Word document
cp ~/Documents/University/Final\ Project/BSc-project-report.docx BSc-project-report-with-chapters5-7.docx

# 3. Open the new document in Word
open BSc-project-report-with-chapters5-7.docx

# 4. Open the clean text files
open chapter5_clean.txt chapter6_clean.txt chapter7_clean.txt
```

### Option 2: AppleScript Automation
```bash
# Run the AppleScript
osascript word_automator.scpt
```

## Step-by-Step Word Instructions

### Step 1: Prepare Document
1. Open `BSc-project-report-with-chapters5-7.docx`
2. Go to end of Chapter 4
3. Insert → Page Break (for new chapter)

### Step 2: Add Chapter 5
1. Type: `فصل ۵: پیاده‌سازی لایه سرویس‌های در سطح کاربر`
2. Apply Style: `Heading 1`
3. Copy all text from `chapter5_clean.txt`
4. Paste after the heading
5. Apply `Heading 2` style to section titles: `۵.۱`, `۵.۲`, etc.

### Step 3: Add Chapters 6 & 7
Repeat Step 2 for:
- Chapter 6: `فصل ۶: پایش، سخت‌سازی امنیتی، آزمون‌ها و تحویل نهایی`
- Chapter 7: `فصل ۷: خلصه، نتیجه‌گیری و کارهای آینده`

### Step 4: Formatting
1. Apply university template formatting
2. Update Table of Contents
3. Check page numbering
4. Proofread

## Advanced: Direct GUI Control

If you want me to control Word directly via GUI automation:

1. **Peekaboo Skill**: I can use screen automation
2. **AppleScript**: Full Word automation
3. **Python + pyautogui**: Cross-platform automation

Would you like me to:
- [ ] Create a Python script with pyautogui to automate Word?
- [ ] Use Peekaboo to record and replay your actions?
- [ ] Create detailed AppleScript for full automation?

## Verification
After merging, check:
- All 7 chapters are present
- Formatting matches university template  
- Table of Contents is updated
- Page numbers are sequential
- No markdown artifacts remain

## Time Estimate
- Manual copy-paste: 15-20 minutes
- With GUI automation: 5-10 minutes
- Full scripting: 2-3 minutes (but requires setup)