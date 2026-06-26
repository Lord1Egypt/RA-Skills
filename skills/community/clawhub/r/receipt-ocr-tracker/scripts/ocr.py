import sys
import pytesseract
from PIL import Image
import re
import csv

if len(sys.argv) < 2:
    print("Usage: python3 ocr.py <image_path>")
    sys.exit(1)

img_path = sys.argv[1]
text = pytesseract.image_to_string(Image.open(img_path))

# Parse receipt (simple regex $ amount, date, items)
lines = text.split('\n')
expenses = []
total = 0
date = re.search(r'\d{1,2}/\d{1,2}/\d{4}|\d{4}-\d{2}-\d{2}', text)
for line in lines:
    amount = re.search(r'\$?(\d+\.?\d*)', line)
    if amount:
        exp = float(amount.group(1))
        total += exp
        expenses.append({'item': line.strip(), 'amount': exp})

with open('expenses.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['date', 'item', 'amount'])
    writer.writeheader()
    for e in expenses:
        writer.writerow({'date': date.group() if date else 'N/A', 'item': e['item'], 'amount': e['amount']})

print(f"CSV saved. Total: ${total:.2f}")
print("Sample:")
print("date,item,amount")
for e in expenses[:3]:
    print(f"N/A,{e['item']},${e['amount']:.2f}")
