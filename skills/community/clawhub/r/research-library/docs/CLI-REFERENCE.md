# Research Library CLI Reference

`reslib` is a command-line tool for managing research materials and references with full-text search, cross-project linking, and confidence scoring.

## Installation

```bash
# Install dependencies
pip install click

# Run from the package directory
python -m reslib [command]

# Or add to PATH and use directly
alias reslib="python -m reslib"
```

## Global Options

These options apply to all commands:

| Option | Environment Variable | Description |
|--------|---------------------|-------------|
| `--data-dir PATH` | `RESLIB_DATA_DIR` | Data directory for database and attachments |
| `--db PATH` | `RESLIB_DB` | Database file path (overrides data-dir) |
| `-q, --quiet` | | Suppress non-essential output |
| `--json-output` | | Output results as JSON |
| `--version` | | Show version and exit |

---

## Commands

### `reslib add` — Add a Document

Add a research document (file or URL) to the library.

```bash
reslib add <path> --project <id> --material-type <reference|research> [options]
```

**Arguments:**
- `path` — File path or URL to add

**Required Options:**
- `-p, --project TEXT` — Project ID
- `-m, --material-type [reference|research]` — Material type
  - `reference` — Vetted, authoritative materials
  - `research` — Working materials, notes, experiments

**Optional:**
- `-u, --url TEXT` — Source URL if file was downloaded
- `-c, --confidence FLOAT` — Confidence score (0.0-1.0, auto-detected if omitted)
- `-t, --title TEXT` — Document title (auto-generated from filename if omitted)
- `--tags TEXT` — Comma-separated tags
- `--extract / --no-extract` — Extract text content (default: yes)

**Examples:**

```bash
# Add a PDF paper
reslib add paper.pdf -p ml-papers -m reference

# Add with custom confidence
reslib add screenshot.png -p debug-notes -m research -c 0.3

# Add from URL
reslib add https://arxiv.org/pdf/1234.5678.pdf -p ai-papers -m reference

# Add code with tags
reslib add implementation.py -p ml-code -m research --tags "pytorch,cnn,training"

# Add with custom title
reslib add data.csv -p analysis -m research -t "Q4 Sales Data"
```

**Output:**
```
ℹ️  Extracting text content...
✅ Saved as research #42
   Title: Paper
   Project: ml-papers
   Type: reference
   Confidence: 0.85
   Size: 2.3 MB
```

---

### `reslib search` — Search Documents

Full-text search across documents.

```bash
reslib search <query> [options]
```

**Arguments:**
- `query` — Search query (supports FTS5 syntax)

**Options:**
- `-p, --project TEXT` — Limit to specific project
- `-a, --all-projects` — Search all projects (default)
- `-m, --material [reference|research]` — Filter by material type
- `--confidence-min FLOAT` — Minimum confidence score
- `-n, --limit INT` — Max results (default: 20)
- `--include-archived` — Include archived documents

**Examples:**

```bash
# Basic search
reslib search "neural networks"

# Search with filters
reslib search "python" -p code-snippets -m research

# High-confidence results only
reslib search "API documentation" --confidence-min 0.8

# Search specific project
reslib search "training" -p ml-experiments

# FTS5 syntax: OR, AND, NOT
reslib search "python OR javascript"
reslib search "machine AND learning"
reslib search "deep learning NOT reinforcement"
```

**Output:**
```
ID     │ Title                              │ Material   │ Conf   │ Project
────────────────────────────────────────────────────────────────────────────
#42    │ Neural Network Architecture        │ reference  │ 0.95   │ ml-papers
#38    │ Training Notes                     │ research   │ 0.72   │ ml-papers
#25    │ PyTorch CNN Implementation         │ research   │ 0.85   │ (other)

3 results found in 12.3ms
```

---

### `reslib get` — Get Document Details

Show detailed information about a document.

```bash
reslib get <research_id> [options]
```

**Arguments:**
- `research_id` — Document ID number

**Options:**
- `--show-content / --no-content` — Show extracted text (default: no)
- `--show-links / --no-links` — Show related documents (default: yes)

**Examples:**

```bash
# Get document details
reslib get 42

# Include extracted content
reslib get 42 --show-content

# JSON output
reslib --json-output get 42
```

**Output:**
```
Document #42: Neural Network Architecture
============================================================
  Project:       ml-papers
  Material Type: reference
  Confidence:    0.95
  MIME Type:     application/pdf
  Created:       2026-02-05 14:30
  Tags:          neural-networks, architecture, deep-learning

Attachments:
  • paper.pdf (2.3 MB)

Links (outgoing):
  → #45 Implementation Code
    (applies_to, relevance: 0.90)

Links (incoming):
  ← #48 Follow-up Research
    (supersedes, relevance: 0.75)
```

---

### `reslib archive` — Archive a Document

Soft-delete a document. It will be hidden from search but can be restored.

```bash
reslib archive <research_id> [options]
```

**Options:**
- `-f, --force` — Archive without confirmation

**Examples:**

```bash
reslib archive 42
reslib archive 42 --force
```

---

### `reslib unarchive` — Restore Archived Document

Restore a previously archived document.

```bash
reslib unarchive <research_id>
```

**Examples:**

```bash
reslib unarchive 42
```

---

### `reslib export` — Export a Document

Export document data in JSON or Markdown format.

```bash
reslib export <research_id> --format <json|markdown> [options]
```

**Options:**
- `-f, --format [json|markdown]` — Output format (default: json)
- `-o, --output PATH` — Output file (stdout if omitted)
- `--include-attachments / --no-attachments` — Copy attachment files

**Examples:**

```bash
# Export as JSON to stdout
reslib export 42 --format json

# Export as Markdown to file
reslib export 42 --format markdown -o doc.md

# Export with attachments to directory
reslib export 42 --format json --include-attachments -o ./export/
```

---

### `reslib link` — Link Documents

Create a relationship between two documents.

```bash
reslib link <source_id> <target_id> --type <link_type> [options]
```

**Arguments:**
- `source_id` — Source document ID
- `target_id` — Target document ID

**Required Options:**
- `-t, --type [applies_to|contradicts|supersedes|related]` — Relationship type

**Optional:**
- `-r, --relevance FLOAT` — Relevance score (0.0-1.0, default: 0.5)
- `--notes TEXT` — Notes about the relationship
- `-b, --bidirectional` — Create link in both directions

**Link Types:**
- `applies_to` — Source applies to or supports target
- `contradicts` — Source contradicts or refutes target
- `supersedes` — Source replaces or updates target
- `related` — General relationship

**Examples:**

```bash
# Basic link
reslib link 42 43 --type applies_to

# Link with relevance
reslib link 42 43 --type supersedes --relevance 0.9

# Bidirectional relationship
reslib link 42 43 --type related --bidirectional

# Link with notes
reslib link 42 43 --type contradicts --notes "Different methodology"
```

---

### `reslib status` — System Status

Show library statistics and system status.

```bash
reslib status
```

**Output:**
```
📚 Research Library Status
========================================

Documents:
  Total:      156
  References: 42
  Research:   114
  Archived:   8

Organization:
  Projects:    12
  Links:       89
  Attachments: 203

Storage:
  Database:    4.2 MB
  Attachments: 1.2 GB
  Total:       1.2 GB

Extraction Queue:
  ⏳ pending: 3
  ⚙️ processing: 1
  ✅ completed: 198
  ❌ failed: 2

Backups:
  Location: /home/user/.reslib/backups
  Last:     2026-02-07 09:00 (research_2026-02-07.db)
```

---

### `reslib backup` — Create Backup

Create a database backup.

```bash
reslib backup [options]
```

**Options:**
- `-n, --name TEXT` — Custom backup name (default: date-based)

**Examples:**

```bash
# Create daily backup
reslib backup

# Create named backup
reslib backup --name before-major-import
```

---

### `reslib restore` — Restore from Backup

Restore database from a backup file.

```bash
reslib restore <date> [options]
```

**Arguments:**
- `date` — Backup date in YYYY-MM-DD format

**Options:**
- `--list` — List available backups instead of restoring
- `-f, --force` — Restore without confirmation

**Examples:**

```bash
# List available backups
reslib restore --list

# Restore from specific date
reslib restore 2026-02-01

# Force restore
reslib restore 2026-02-01 --force
```

---

### `reslib projects` — Manage Projects

List or create projects.

```bash
reslib projects [options]
```

**Options:**
- `-c, --create TEXT` — Create a new project with this ID
- `-n, --name TEXT` — Name for new project
- `-d, --description TEXT` — Description for new project

**Examples:**

```bash
# List all projects
reslib projects

# Create a project
reslib projects --create ml-papers --name "Machine Learning Papers"

# Create with description
reslib projects -c experiments -n "Experiments" -d "Various experimental work"
```

---

### `reslib tags` — Manage Tags

View or modify tags on a document.

```bash
reslib tags <research_id> [options]
```

**Options:**
- `-a, --add TEXT` — Add tag (repeatable)
- `-r, --remove TEXT` — Remove tag (repeatable)
- `--set TEXT` — Replace all tags (comma-separated)

**Examples:**

```bash
# View tags
reslib tags 42

# Add tags
reslib tags 42 --add important --add review

# Remove tag
reslib tags 42 --remove obsolete

# Replace all tags
reslib tags 42 --set "ml,python,tutorial"
```

---

## Example Workflows

### Import a Research Project

```bash
# Create the project
reslib projects --create phd-thesis --name "PhD Thesis Research"

# Add reference papers
for pdf in papers/*.pdf; do
    reslib add "$pdf" -p phd-thesis -m reference
done

# Add working notes
reslib add notes/ -p phd-thesis -m research

# Check status
reslib status
```

### Research Discovery Workflow

```bash
# Search for relevant materials
reslib search "transformer attention mechanism" --confidence-min 0.7

# Get details on interesting result
reslib get 42 --show-content

# Link related documents
reslib link 42 45 --type applies_to --relevance 0.9

# Export for reference
reslib export 42 --format markdown -o references/transformer.md
```

### Maintain Your Library

```bash
# Create regular backup
reslib backup

# Check system status
reslib status

# Archive outdated documents
reslib archive 15 --force
reslib archive 23 --force

# Tag documents for review
reslib tags 42 --add needs-review
reslib tags 43 --add needs-review

# Search for review items
reslib search "needs-review"
```

---

## Tips & Tricks

### Use JSON Output for Scripting

```bash
# Get document ID from add
DOC_ID=$(reslib --json-output add file.pdf -p test -m research | jq -r '.id')

# Search and process results
reslib --json-output search "query" | jq '.results[].id'
```

### Organize with Consistent Naming

```bash
# Use consistent project IDs
reslib add paper.pdf -p papers-2026-q1 -m reference
reslib add notes.md -p papers-2026-q1 -m research

# Use meaningful tags
reslib tags 42 --set "topic:ml,status:active,priority:high"
```

### Bulk Operations

```bash
# Add all PDFs in a directory
for f in *.pdf; do
    reslib add "$f" -p my-project -m reference --quiet
done

# Archive all research items in a project
reslib --json-output search "" -p old-project -m research | \
    jq -r '.results[].id' | \
    xargs -I{} reslib archive {} --force
```

### Environment Variables

```bash
# Set default data directory
export RESLIB_DATA_DIR="$HOME/research-library"

# Use custom database
export RESLIB_DB="/path/to/custom.db"
```

---

## Troubleshooting

### "Search index not found"

Run any add command to initialize the database:
```bash
reslib add dummy.txt -p init -m research
```

### "No such file or directory"

Check file path and ensure it exists:
```bash
ls -la path/to/file
```

### "Duplicate detected"

The file hash already exists. You can:
- Skip (press n)
- Add anyway (press y) — creates duplicate entry

### Low Confidence Scores

Documents with low confidence are queued for async extraction. Run the worker pool to process them (see worker documentation).
