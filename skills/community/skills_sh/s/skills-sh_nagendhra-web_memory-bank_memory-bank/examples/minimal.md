# Memory — receipt-scanner
Updated: 2025-04-08 | Session 2

Working on: OCR pipeline — Tesseract extracts text, GPT-4o parses into structured receipt data (merchant, items, totals, tax)
Next: Add batch processing to `/api/scan` endpoint so users can upload multiple receipt images at once
Blocked by: nothing
Stack: Python, FastAPI, pytesseract, OpenAI API
Key file: `src/pipeline.py` — the whole OCR → parse → validate chain
