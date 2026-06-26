---
name: zotero-browse
description: "Browse, search, and read papers from a local Zotero library. Use when the user wants to: (1) Search their Zotero library by title, author, or keyword, (2) Read or summarize a specific PDF stored in Zotero, (3) Get an overview of their Zotero library (item counts, types, recent additions), (4) Find papers related to a specific topic in their collection. Activates on: 'search my Zotero', 'find papers about', 'read the PDF', 'show recent papers', 'Zotero library summary', 'how many papers do I have on X', any query about accessing or reading Zotero papers or PDFs."
metadata:
  openclaw:
    emoji: "📚"
    requires:
      env: []
      bins: ["python3 (with pymupdf, sqlite3 built-in)"]
    primaryEnv: null
---

# Zotero Browse Skill

Read papers, search your library, and extract PDF content from a local Zotero database.

## Database & Storage Locations

- **Database**: `E:\Refer.Hub\zotero.sqlite` (4300+ items, 2112 stored PDFs)
- **PDF storage**: `E:\Refer.Hub\storage\{storageHash}/filename.pdf`
- Python stdlib `sqlite3` for queries; `fitz` (PyMuPDF) for PDF reading

## Scripts

- `scripts/query_items.py` — Search and browse the library
- `scripts/read_pdf.py` — Read PDF text by attachment key or title search

Both scripts are executable directly. Always use `py -3` on Windows.

---

## Common Workflows

### 1. Search library by keyword

```bash
py -3 scripts/query_items.py --search "FGF15"
py -3 scripts/query_items.py --search "fatty liver"
```

Returns: matching items with key, title, authors, date, attachment count.

### 2. Find attachment key for a paper, then read PDF

```bash
# Step 1: search to get the attachment key
py -3 scripts/query_items.py --search "Silibinin"

# Step 2: read the PDF (pass the attachment key shown in output)
py -3 scripts/read_pdf.py ZL42EGES
```

### 3. Read PDF by title search

```bash
py -3 scripts/read_pdf.py --search "Silibinin" --pages 5
```

Prompts for which attachment key to open, then extracts text.

### 4. Library summary

```bash
py -3 scripts/query_items.py --summary
```

Shows total items and breakdown by type (journalArticle, book, etc.).

### 5. Recent additions

```bash
py -3 scripts/query_items.py --recent 10
```

### 6. Get item details by key

```bash
py -3 scripts/query_items.py --key ZL42EGES
```

### 7. Extract full PDF text to file

```bash
py -3 scripts/read_pdf.py ZL42EGES --output extracted.txt
```

---

## Database Schema

For SQL query reference (schema, table structure, query examples), see:

📄 `references/schema.md`

Key tables: `items`, `itemData`, `fields`, `itemDataValues`, `itemAttachments`, `itemTypes`, `creators`, `itemCreators`, `tags`

---

## PDF Resolution Logic

Zotero stores PDFs at `E:\Refer.Hub\storage\{storageHash}/` where `storageHash` is the hash from `itemAttachments.storageHash`. The `itemAttachments.path` field stores the original filename but the folder is named by `storageHash`.

**Direct open by key**:
```python
import sqlite3, fitz, os

DB = r"E:\Refer.Hub\zotero.sqlite"
STORAGE = r"E:\Refer.Hub\storage"

conn = sqlite3.connect(DB, timeout=30)
conn.execute("PRAGMA read_only=ON")
cur = conn.cursor()

cur.execute("""
    SELECT itemAttachments.storageHash
    FROM itemAttachments JOIN items ON itemAttachments.itemID = items.itemID
    WHERE items.key = ? AND itemAttachments.linkMode = 0
""", (key,))
row = cur.fetchone()
if row and row[0]:
    folder = os.path.join(STORAGE, row[0])
    files = [f for f in os.listdir(folder) if f.lower().endswith('.pdf')]
    if files:
        pdf_path = os.path.join(folder, files[0])
        doc = fitz.open(pdf_path)
        text = "\n".join(page.get_text() for page in doc)
```

---

## Tips

- If database is locked, close Zotero application first
- For long PDFs, use `--pages N` to extract just first N pages
- PDF text extraction works for text-based PDFs; scanned PDFs need OCR
- Use `--info` flag to get PDF metadata without extracting full text
- Attachment keys are 8-character Zotero item keys shown in search results
