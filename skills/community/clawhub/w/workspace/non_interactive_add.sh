#!/bin/bash

echo "⚡ NON-INTERACTIVE CHAPTER ADDITION"
echo "==================================="

# First, let's just copy each chapter and give exact instructions
echo ""
echo "📋 CHAPTER FILES READY:"
echo "1. chapter5_clean.txt - 18,837 bytes"
echo "2. chapter6_clean.txt - 11,811 bytes"
echo "3. chapter7_clean.txt - 7,793 bytes"
echo ""

# Copy Chapter 5 to clipboard
echo "📋 COPYING CHAPTER 5 TO CLIPBOARD..."
cat chapter5_clean.txt | pbcopy
clip_len=$(pbpaste | wc -c)
echo "✅ Chapter 5 copied ($clip_len characters)"

echo ""
echo "🎯 ACTION REQUIRED - CHAPTER 5:"
echo "================================"
echo "1. Click Word window"
echo "2. Press Cmd+End (go to end)"
echo "3. Press Cmd+Enter (page break)"
echo "4. Type: فصل ۵: پیاده‌سازی لایه سرویس‌های در سطح کاربر"
echo "5. Select title → Cmd+Option+1 (Heading 1)"
echo "6. Press Enter"
echo "7. Press Cmd+V (paste)"
echo "8. Find '۵.۱' → Select → Cmd+Option+2 (Heading 2)"
echo "9. Repeat for '۵.۲', '۵.۳'"
echo "10. Press Cmd+S (save)"
echo ""
echo "⏳ After completing Chapter 5, press Enter to continue..."
read dummy

# Copy Chapter 6 to clipboard
echo ""
echo "📋 COPYING CHAPTER 6 TO CLIPBOARD..."
cat chapter6_clean.txt | pbcopy
clip_len=$(pbpaste | wc -c)
echo "✅ Chapter 6 copied ($clip_len characters)"

echo ""
echo "🎯 ACTION REQUIRED - CHAPTER 6:"
echo "================================"
echo "1. Press Cmd+End (go to end)"
echo "2. Press Cmd+Enter (page break)"
echo "3. Type: فصل ۶: پایش، سخت‌سازی امنیتی، آزمون‌ها و تحویل نهایی"
echo "4. Select title → Cmd+Option+1 (Heading 1)"
echo "5. Press Enter"
echo "6. Press Cmd+V (paste)"
echo "7. Find '۶.۱' → Select → Cmd+Option+2 (Heading 2)"
echo "8. Repeat for '۶.۲', '۶.۳'"
echo "9. Press Cmd+S (save)"
echo ""
echo "⏳ After completing Chapter 6, press Enter to continue..."
read dummy

# Copy Chapter 7 to clipboard
echo ""
echo "📋 COPYING CHAPTER 7 TO CLIPBOARD..."
cat chapter7_clean.txt | pbcopy
clip_len=$(pbpaste | wc -c)
echo "✅ Chapter 7 copied ($clip_len characters)"

echo ""
echo "🎯 ACTION REQUIRED - CHAPTER 7:"
echo "================================"
echo "1. Press Cmd+End (go to end)"
echo "2. Press Cmd+Enter (page break)"
echo "3. Type: فصل ۷: خلصه، نتیجه‌گیری و کارهای آینده"
echo "4. Select title → Cmd+Option+1 (Heading 1)"
echo "5. Press Enter"
echo "6. Press Cmd+V (paste)"
echo "7. Find '۷.۱' → Select → Cmd+Option+2 (Heading 2)"
echo "8. Repeat for '۷.۲', '۷.۳'"
echo "9. Press Cmd+S (save)"
echo ""

echo "✅ ALL CHAPTERS READY FOR ADDITION!"
echo ""
echo "📊 VERIFICATION:"
echo "- Original file: 228,090 bytes"
echo "- Expected after: ~265,000 bytes"
echo "- Check: File → Properties → Size"
echo ""
echo "🚀 NEXT: Update Table of Contents"
echo "   References → Update Table"