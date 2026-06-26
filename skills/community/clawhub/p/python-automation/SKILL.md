---
name: python-automation
description: "Full-stack Python automation toolkit for file processing, data extraction, PDF manipulation, Excel/workbook automation, web scraping, and system tasks. Use when the user needs to: (1) Process/rename/organize files in bulk, (2) Extract data from PDFs, CSVs, or web pages, (3) Generate or modify Excel reports, (4) Automate repetitive system tasks (cron, file watching), (5) Build quick CLI tools for data processing."
---

# Python Automation

## Core Libraries Quick Reference

| Task | Library | Installation |
|------|---------|-------------|
| File system | `pathlib`, `shutil`, `os` | stdlib |
| CSV | `csv` | stdlib |
| Excel | `openpyxl` | `pip install openpyxl` |
| Excel (old) | `xlrd` / `xlwt` | `pip install xlrd xlwt` |
| PDF text | `PyMuPDF` (fitz) | `pip install PyMuPDF` |
| PDF tables | `camelot-py` / `tabula-py` | `pip install camelot-py` |
| Web scraping | `requests` + `BeautifulSoup4` | `pip install requests beautifulsoup4` |
| Browser automation | `playwright` or `selenium` | `pip install playwright` |
| CLI | `argparse` (stdlib) or `click` | stdlib / `pip install click` |
| Rich terminal | `rich` | `pip install rich` |
| File watching | `watchdog` | `pip install watchdog` |
| Scheduling | `schedule` or cron | `pip install schedule` |

## Common Patterns

### 1. Batch File Processing

```python
from pathlib import Path

for f in Path(".").glob("**/*.txt"):
    content = f.read_text()
    # transform content
    f.write_text(content)
```

### 2. CSV Read/Write

```python
import csv
with open("input.csv", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row["column_name"])

with open("output.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["col1", "col2"])
    writer.writerow(["val1", "val2"])
```

### 3. Excel Generation

```python
from openpyxl import Workbook
wb = Workbook()
ws = wb.active
ws["A1"] = "Hello"
ws["B1"] = 42
wb.save("output.xlsx")
```

### 4. Web Scraping

```python
import requests
from bs4 import BeautifulSoup

resp = requests.get("https://example.com", timeout=10)
soup = BeautifulSoup(resp.text, "html.parser")
for link in soup.select("a[href]"):
    print(link["href"], link.text.strip())
```

## Scripts

See [scripts/](scripts/) for ready-to-use automation scripts:
- `rename_batch.py` — Batch rename files with pattern matching
- `csv_to_excel.py` — Convert CSV files to Excel workbooks

## Reference Files

- [references/pandas.md](references/pandas.md) — Advanced data analysis with pandas
- [references/pdf.md](references/pdf.md) — PDF extraction patterns
