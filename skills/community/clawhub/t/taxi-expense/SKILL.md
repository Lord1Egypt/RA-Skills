---
name: taxi_expense
description: 识别滴滴打车订单截图，OCR识别文字+坐标，马赛克脱敏目的地，按月生成报销Excel
---

When user sends taxi order screenshots:

## Setup (first time only)
```bash
bash ~/.openclaw/workspace/skills/taxi_expense/scripts/setup.sh
```

## Process Screenshots
```bash
node ~/.openclaw/workspace/skills/taxi_expense/scripts/process.js <image1> [image2] ...
```

The script will:
1. OCR each image with Tesseract.js v4 (uses coordinates to detect text positions)
2. Parse orders: date, time, start/end point, amount
3. Smart amount extraction: handles OCR misreads (¥→%, missing ¥, missing decimal)
4. Filter: only **weekday evening rides (after 21:00)** qualify for reimbursement
5. Auto-exclude closed/cancelled orders (amount = ¥0)
6. White block desensitization on destination address in screenshots (keeps first/last char visible)
7. Desensitize destination text in Excel (e.g. 古*****门)
8. Save screenshots to `~/.openclaw/workspace/taxi_expense/screenshots/`
9. Update `~/.openclaw/workspace/taxi_expense/taxi_data.json` (auto-dedup by date+amount)
10. Generate monthly Excel: `~/.openclaw/workspace/taxi_expense/YYYY-MM-taxi_expense.xlsx`

## Excel Columns
序号 | 日期 | 星期 | 时间 | 起点 | 终点(脱敏) | 金额 | 备注

Sheet 2 contains mosaiced order screenshots.

## Output
Tell user:
- How many new orders were added
- Monthly totals (reimbursable orders only)
- Any skipped orders and why (weekend, before 21:00, closed, ¥0)

## Send Preview (only if user asks)
The script saves desensitized screenshots to the `screenshots/` directory. Send via:
```bash
openclaw message send --channel telegram --target <chat_id> --message "msg" --media <file.xlsx>
```

## Known Issues
- Tesseract Chinese quality is imperfect ("点"→"炭", "轻享"→"轻亭")
- Uses regex `/终[点炭]/` for tolerant matching
- Amount recognition: ¥ may be misread as % or lost entirely
- Amount > 500 is auto-corrected (missing decimal: 1970→19.70)
- Source images must be ORIGINAL screenshots (not previously processed/cropped)
- Multiple images supported: `node process.js img1 img2 img3`
