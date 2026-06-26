# Zotero SQLite Database Schema

## Primary Database Location

```
E:\Refer.Hub\zotero.sqlite   (main library, ~223 MB)
```

The database is also at `C:\Users\41406\Zotero\zotero.sqlite` but `E:\Refer.Hub` contains the full indexed library.

## Key Tables

### items — All library entries
| Column | Type | Description |
|--------|------|-------------|
| itemID | INTEGER | Primary key |
| itemTypeID | INT | Type of item (journalArticle, book, etc.) |
| key | TEXT | Zotero item key (8-char alphanumeric, e.g. `ZL42EGES`) |
| libraryID | INT | Library (personal=1 usually) |
| dateAdded | TIMESTAMP | When added |
| dateModified | TIMESTAMP | Last modified |
| synced | INT | Sync state |

### itemTypes
| Column | Type |
|--------|------|
| itemTypeID | INTEGER |
| typeName | TEXT (journalArticle, book, bookSection, conferencePaper, attachment, note...) |

### itemData — All field values (linked table)
| Column | Type |
|--------|------|
| itemID | INT |
| fieldID | INT |
| valueID | INT |

### fields — Field definitions
| fieldID | fieldName |
|---------|-----------|
| ... | title |
| ... | creators |
| ... | date |
| ... | publicationTitle |
| ... | journalAbbreviation |
| ... | DOI |
| ... | abstractNote |
| ... | tags |
| ... | url |
| ... | volume |
| ... | issue |
| ... | pages |
| ... | publisher |
| ... | ISBN |
| ... | ISSN |

### itemDataValues — Actual text values
| Column | Type |
|--------|------|
| valueID | INTEGER |
| value | TEXT |

### itemAttachments — PDF/linked files
| Column | Type | Description |
|--------|------|-------------|
| itemID | INTEGER | Attachment item ID |
| parentItemID | INT | Parent literature item ID |
| linkMode | INT | 0=stored file, 1=linked file, 2=imported file |
| path | TEXT | Path string like `storage:filename.pdf` |
| storageHash | TEXT | Hash of attachment content, matches folder name in `storage/` |
| contentType | TEXT | MIME type (e.g. `application/pdf`) |

### itemCreators — Author/creator links
| Column | Type |
|--------|------|
| itemID | INT |
| creatorID | INT |
| creatorTypeID | INT (author, editor, etc.) |

### creators — Creator details
| Column | Type |
|--------|------|
| creatorID | INTEGER |
| firstName | TEXT |
| lastName | TEXT |

### tags
| Column | Type |
|--------|------|
| name | TEXT |
| type | INT |

### itemTags — Tag associations
| Column | Type |
|--------|------|
| itemID | INT |
| tagID | INT |

### collections — Folders/collections
| Column | Type |
|--------|------|
| name | TEXT |
| parentCollectionID | INT |

## Common Query Patterns

### Search papers by title
```sql
SELECT items.key, itemTypes.typeName, itemDataValues.value AS title
FROM items
JOIN itemTypes ON items.itemTypeID = itemTypes.itemTypeID
JOIN itemData ON items.itemID = itemData.itemID
JOIN fields ON itemData.fieldID = fields.fieldID
JOIN itemDataValues ON itemData.valueID = itemDataValues.valueID
WHERE fields.fieldName = 'title'
AND itemDataValues.value LIKE '%NAFLD%'
ORDER BY items.dateAdded DESC
```

### Get authors of an item
```sql
SELECT creators.firstName, creators.lastName, creatorTypes.creatorType
FROM itemCreators
JOIN creators ON itemCreators.creatorID = creators.creatorID
JOIN creatorTypes ON itemCreators.creatorTypeID = creatorTypes.creatorTypeID
WHERE itemCreators.itemID = ?
```

### Find PDF path for an attachment key
```sql
SELECT items.key, itemAttachments.path, itemAttachments.storageHash
FROM itemAttachments
JOIN items ON itemAttachments.itemID = items.itemID
WHERE items.key = 'ZL42EGES' AND itemAttachments.linkMode = 0
```

### Get recent items with tags
```sql
SELECT items.key, itemTypes.typeName, itemDataValues.value AS title, items.dateAdded
FROM items
JOIN itemTypes ON items.itemTypeID = itemTypes.itemTypeID
JOIN itemData ON items.itemID = itemData.itemID
JOIN fields ON itemData.fieldID = fields.fieldID
JOIN itemDataValues ON itemData.valueID = itemDataValues.valueID
WHERE fields.fieldName = 'title'
ORDER BY items.dateAdded DESC LIMIT 20
```

## Storage Structure

PDFs are stored in `E:\Refer.Hub\storage\{storageHash}/` (one folder per attachment).
Folder name = `storageHash` value from `itemAttachments` table.

```
E:\Refer.Hub\
├── zotero.sqlite          ← main database
└── storage\
    ├── ZL42EGES\          ← folder named by storageHash
    │   ├── .zotero-ft-cache
    │   ├── .zotero-reader-state
    │   └── Full Paper Title.pdf
    ├── M6BCAS9M\
    └── ...
```

To resolve the actual PDF path:
1. Query `itemAttachments` with attachment key → get `storageHash`
2. The folder `E:\Refer.Hub\storage\{storageHash}\` contains the PDF
3. List folder, pick the `.pdf` file

## Python Quick Reference

```python
import sqlite3, fitz, os

DB = r"E:\Refer.Hub\zotero.sqlite"
STORAGE = r"E:\Refer.Hub\storage"

conn = sqlite3.connect(DB, timeout=30)
conn.execute("PRAGMA read_only=ON")
cur = conn.cursor()

# Search
cur.execute("""
    SELECT items.key, itemTypes.typeName, itemDataValues.value
    FROM items JOIN itemTypes ON items.itemTypeID = itemTypes.itemTypeID
    JOIN itemData ON items.itemID = itemData.itemID
    JOIN fields ON itemData.fieldID = fields.fieldID
    JOIN itemDataValues ON itemData.valueID = itemDataValues.valueID
    WHERE fields.fieldName = 'title' AND itemDataValues.value LIKE ?
""", (f"%{term}%",))

# Read PDF
import fitz
doc = fitz.open(pdf_path)
text = "\n".join(page.get_text() for page in doc)
```

## Limitations

- Database is locked by Zotero when it is running → use read-only mode
- PDF text extraction via PyMuPDF works for text-based PDFs
- Scanned/image PDFs require OCR (not covered here)
- Writing to database requires closing Zotero and using mode=OFF
