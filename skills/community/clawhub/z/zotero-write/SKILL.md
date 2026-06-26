---
name: zotero-write
description: "Write, tag, annotate, and edit a local Zotero SQLite database. Use when the user wants to: (1) Add tags or labels to papers in their Zotero library, (2) Add notes or annotations to specific papers, (3) Update paper metadata (title, authors, journal, date, DOI, etc.), (4) Create new Zotero items manually. Activates on: 'tag this paper', 'add a note to', 'update the metadata of', 'add this to my Zotero', 'create a new Zotero entry', 'edit Zotero', 'organize my Zotero with tags', any request to modify, annotate, or write to the Zotero database."
metadata:
  openclaw:
    emoji: "📝"
    requires:
      env: []
      bins: ["python3 (with sqlite3 built-in)"]
    primaryEnv: null
---

# Zotero Write Skill

Write, tag, annotate, and edit a local Zotero SQLite database.

## Database & Safety

- **Database**: `E:\Refer.Hub\zotero.sqlite`
- **⚠️ SAFETY**: Always use `--backup` before any write operation. Backups saved to `E:\Refer.Hub\backups/`
- **Required**: Close Zotero application before writing to the database
- **Rule**: Never run write operations without `--backup` — the script will refuse

## Scripts

- `scripts/write_items.py` — All write operations

## Scripts Usage

### 0. Always backup first
```bash
py -3 scripts/write_items.py --backup "E:\Refer.Hub\zotero.sqlite"
```
This saves a timestamped backup before any write. **Always do this first.**

### 1. Add tags to a paper

First find the item key from `zotero-browse` skill, then:
```bash
py -3 scripts/write_items.py --backup "E:\Refer.Hub\zotero.sqlite" \
  --add-tag ZL42EGES "NAFLD" "FGF15" "silymarin"
```

### 2. Add a note to a paper
```bash
py -3 scripts/write_items.py --backup "E:\Refer.Hub\zotero.sqlite" \
  --add-note ZL42EGES "This paper shows FGF15 is the key mediator of silibinin's anti-NAFLD effect."
```

### 3. Update a field (metadata)
```bash
# Update title
py -3 scripts/write_items.py --backup "E:\Refer.Hub\zotero.sqlite" \
  --set-field ZL42EGES title "New Title Here"

# Update date
py -3 scripts/write_items.py --backup "E:\Refer.Hub\zotero.sqlite" \
  --set-field ZL42EGES date "2024"

# Update journal
py -3 scripts/write_items.py --backup "E:\Refer.Hub\zotero.sqlite" \
  --set-field ZL42EGES publicationTitle "Journal Name"

# Update DOI
py -3 scripts/write_items.py --backup "E:\Refer.Hub\zotero.sqlite" \
  --set-field ZL42EGES DOI "10.1234/example"
```

### 4. Create a new Zotero entry
```bash
py -3 scripts/write_items.py --backup "E:\Refer.Hub\zotero.sqlite" \
  --new-item journalArticle \
  --title "Example Title" \
  --authors "John Doe" "Jane Smith" \
  --date "2024" \
  --journal "Nature Medicine" \
  --doi "10.1038/s41591-024-0001-z"
```

### 5. List available field names
```bash
py -3 scripts/write_items.py --list-fields
```

### 6. Show full item details (before editing)
```bash
py -3 scripts/write_items.py --item-info ZL42EGES
```

---

## Available Fields

Run `--list-fields` to see all. Common fields:

| fieldName | Description |
|-----------|-------------|
| title | Paper title |
| creators | Authors (use `--authors` for new items) |
| date | Publication date (YYYY or YYYY-MM-DD) |
| publicationTitle | Journal name |
| DOI | Digital Object Identifier |
| url | Web URL |
| abstractNote | Abstract |
| tags | Tags (use `--add-tag` instead) |
| volume | Volume number |
| issue | Issue number |
| pages | Page range |
| publisher | Publisher |
| ISBN | ISBN |
| ISSN | ISSN |
| journalAbbreviation | Journal abbreviation |

## Item Types

When creating new items, use one of:
- `journalArticle` (default for papers)
- `book`
- `bookSection`
- `conferencePaper`
- `thesis`
- `report`
- `webpage`
- `note`

## Workflow: Tag a paper

1. Use `zotero-browse` skill to find the paper's attachment key
2. Run with `--backup` first
3. Add tags:
   ```bash
   py -3 scripts/write_items.py --backup "E:\Refer.Hub\zotero.sqlite" \
     --add-tag ZL42EGES "NAFLD" "FGF15" "biomarker"
   ```
4. Confirm backup was created at `E:\Refer.Hub\backups/`

## Important Notes

- **Backup is automatic** with `--backup` — always use it
- Tags use exact string matching; case-sensitive
- Setting a field that already has a value will **overwrite** it
- Notes are added as child items linked to the parent paper
- New items get a random 8-char Zotero key
- After writing, Zotero will sync changes on next launch
