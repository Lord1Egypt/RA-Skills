# PDF Processing Patterns

## Text Extraction

### Using PyMuPDF (fitz)
```bash
pip install PyMuPDF
```

```python
import fitz  # PyMuPDF

doc = fitz.open("document.pdf")
for page_num, page in enumerate(doc):
    text = page.get_text()
    print(f"--- Page {page_num + 1} ---")
    print(text)
```

### Using pdfplumber (better for tables)
```bash
pip install pdfplumber
```

```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        tables = page.extract_tables()
```

## Table Extraction

### Using camelot-py (best for well-structured tables)
```bash
pip install camelot-py[cv]
```

```python
import camelot

tables = camelot.read_pdf("document.pdf", pages="1-3")
for table in tables:
    print(table.df)  # DataFrame
    # table.to_csv("table.csv")
```

## PDF Generation

### Using reportlab
```bash
pip install reportlab
```

```python
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

c = canvas.Canvas("output.pdf", pagesize=A4)
c.drawString(100, 700, "Hello, PDF!")
c.save()
```

### Using fpdf2 (simpler)
```bash
pip install fpdf2
```

```python
from fpdf import FPDF

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.cell(200, 10, text="Hello, PDF!", new_x="LMARGIN", new_y="NEXT")
pdf.output("output.pdf")
```

## PDF Merge / Split

```python
# Merge PDFs
from PyPDF2 import PdfWriter, PdfReader

writer = PdfWriter()
for pdf_file in ["file1.pdf", "file2.pdf"]:
    reader = PdfReader(pdf_file)
    for page in reader.pages:
        writer.add_page(page)

writer.write("merged.pdf")
```
