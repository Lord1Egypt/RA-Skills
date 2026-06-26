# MANUAL FIX FOR BROKEN CHARACTERS

## Problem:
- Persian text appears broken in Word
- Encoding issues from terminal copy-paste

## Solution 1: Use TextEdit as intermediary (RECOMMENDED)

### For Chapter 5:
1. **Open `chapter5_clean.txt` in TextEdit**
   ```bash
   open -a TextEdit chapter5_clean.txt
   ```
2. **In TextEdit:**
   - Select All (Cmd+A)
   - Copy (Cmd+C)

3. **In Word:**
   - Go to end of original document
   - Insert → Page Break
   - Type: `فصل ۵: پیاده‌سازی لایه سرویس‌های در سطح کاربر`
   - Apply Style: Heading 1
   - Press Enter
   - Paste (Cmd+V) - TextEdit preserves encoding
   - Format subheadings (۵.۱, ۵.۲) as Heading 2

### Repeat for Chapters 6 & 7:
- Open `chapter6_clean.txt` in TextEdit → Copy → Paste in Word
- Open `chapter7_clean.txt` in TextEdit → Copy → Paste in Word

## Solution 2: Check font in Word

If text appears as boxes or question marks:
1. Select the broken text
2. Change font to:
   - **B Nazanin** (best for Persian)
   - **Arial** (fallback)
   - **Tahoma** (good for Persian/English mix)

## Solution 3: Use the new PROPER document

1. Open `BSc-project-report-PROPER.docx`
2. Check if all 7 chapters are present
3. Check if Persian text displays correctly
4. If good, use this as your final document

## Verification Steps:

### Check 1: File Size
- Original: 228,090 bytes
- Current (broken): 245,782 bytes  
- Proper (new): 216,396 bytes
- **Expected final: ~265,000 bytes** (chapters 1-4 + 5-7)

### Check 2: Content
1. Open document
2. Scroll through all 7 chapters
3. Verify:
   - No broken characters
   - Persian text readable
   - All headings present
   - Page numbers continuous

### Check 3: Formatting
1. All text justified
2. Heading 1 for chapter titles
3. Heading 2 for subheadings (۵.۱, ۵.۲, etc.)
4. Consistent font throughout

## If Still Broken:

### Nuclear Option: Create from scratch
1. Create new Word document
2. Copy Chapters 1-4 from original (should be fine)
3. Add Chapters 5-7 using TextEdit method
4. Apply university formatting

### Time Estimate:
- TextEdit method: 20-30 minutes
- Checking/formatting: 10-15 minutes
- **Total: 30-45 minutes**

## Next After Fix:
1. ✅ Apply formatting (justification, styles)
2. ✅ Update Table of Contents
3. ⏳ ChatGPT review (Step 4)
4. ⏳ Add appendix references (Step 5)
5. ⏳ Final review (Step 6)