# SIMPLE STEP-BY-STEP CHAPTER ADDITION

## CURRENT STATE:
- Word document is open with Chapters 1-4
- Chapter 5 content is READY in clipboard
- You need to manually paste it

## STEP 1: ADD CHAPTER 5 RIGHT NOW

1. **Make Word active** - Click on Word window
2. **Go to end of document** - Press `Cmd + End` (or scroll to very end)
3. **Insert page break** - Press `Cmd + Enter`
4. **Type the title**: `فصل ۵: پیاده‌سازی لایه سرویس‌های در سطح کاربر`
5. **Apply Heading 1**:
   - Select the title text
   - Press `Cmd + Option + 1`
6. **Press Enter** for new paragraph
7. **Paste content**: `Cmd + V`
8. **Format subheadings**:
   - Find `۵.۱` in the text
   - Select it
   - Press `Cmd + Option + 2` (Heading 2)
   - Repeat for `۵.۲`, `۵.۳`, etc.
9. **Save**: `Cmd + S`

## STEP 2: PREPARE CHAPTER 6

After you complete STEP 1, run this command to copy Chapter 6:

```bash
cat chapter6_clean.txt | pbcopy
```

Then add Chapter 6 using same steps (with title: `فصل ۶: پایش، سخت‌سازی امنیتی، آزمون‌ها و تحویل نهایی`)

## STEP 3: PREPARE CHAPTER 7

After Chapter 6, run:

```bash
cat chapter7_clean.txt | pbcopy
```

Then add Chapter 7 (title: `فصل ۷: خلصه، نتیجه‌گیری و کارهای آینده`)

## VERIFICATION:

After adding all chapters, check:
1. File size should be > 250KB
2. Document has 7 chapters
3. All text is justified
4. Headings are properly styled

## TROUBLESHOOTING:

If paste shows broken text:
1. Open `chapter5_clean.txt` in TextEdit
2. Select All (`Cmd + A`)
3. Copy (`Cmd + C`)
4. Paste in Word (`Cmd + V`)

---

**Start with STEP 1 now. Once Chapter 5 is added, reply and I'll give you the next command.**