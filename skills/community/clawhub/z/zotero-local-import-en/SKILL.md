---
name: zotero-local-import-en
description: Import local PDF files into Zotero from the command line on Windows/macOS/Linux via the Zotero local connector (127.0.0.1). Use for single-PDF import, folder batch import, importing into an existing collection, listing collections, and verifying recent imported attachments. Requires Zotero desktop setting to allow local app communication and a user-provided connector port.
---

# Zotero Local Import Skill (Windows / macOS / Linux)

Before using this skill, make sure Zotero Desktop is open and configured:

1. Open **Zotero → Settings → Advanced**
2. Enable: **Allow other applications on this computer to communicate with Zotero**
3. Note the connector port (commonly `23119`) and provide it to the agent via `--port`

> This skill only imports into **existing collections**. It does **not** create collections.
> If `--collection` is not provided, imports default to **My Library**.

## Script location

- `scripts/zotero_tool.py`

## Features

1. Import a single PDF
2. Import all PDFs in a folder (optional recursive mode)
3. Import into an existing collection
4. List local Zotero collections
5. Check recently imported attachments (read-only from `zotero.sqlite`)

## Agent pre-execution contract (foolproof mode)

The agent must support all of the following user input forms and complete import automatically:

1. A folder path
2. A single PDF path
3. Multiple PDF paths
4. A few PDFs inside a folder (user can provide file names such as `x.pdf, y.pdf, z.pdf`)

The agent must also collect:

- Zotero local connector port
- Optional collection name (if omitted, default to My Library)

Required execution flow:

1. Run `doctor --auto-install-deps`
2. If successful, run `import`

Natural-language parsing (paths, file names, port, collection) must be handled by the **agent**, not by the script. The script accepts structured arguments only.

## Command usage

Run from repository root (or use absolute script path):

```bash
python skills/zotero-local-import-en/scripts/zotero_tool.py --help
```

### 0) Environment check (mandatory)

```bash
python skills/zotero-local-import-en/scripts/zotero_tool.py doctor \
  --port <USER_ZOTERO_PORT> \
  --auto-install-deps
```

This checks and auto-handles:

- Python runtime availability
- `requests` dependency (auto-installs if missing)
- `http://127.0.0.1:<port>/connector/ping` connectivity
- Platform URL opener availability (Windows: `os.startfile`, macOS: `open`, Linux: `xdg-open`)

If auto-install fails, the agent should surface the error and suggest:

```bash
python -m pip install requests>=2.31.0
```

### NL) Natural-language input policy (agent-side parsing only)

Users may say things like:

- “Import `x.pdf, y.pdf, z.pdf` from `<folder>`, port `xxxx`, collection `xxxx`”
- “Import this PDF: `<absolute path>`, port `xxxx`”

The agent must convert NL input into structured CLI args, then call `import`:

- Folder mode: `--dir` + optional `--pick`
- Single/multiple PDF mode: repeated `--pdf`
- Port: `--port`
- Collection: optional `--collection` (defaults to My Library)

### A) Import a single PDF

```bash
python skills/zotero-local-import-en/scripts/zotero_tool.py import \
  --pdf "<ABSOLUTE_PDF_PATH>" \
  --port <USER_ZOTERO_PORT>
```

### A2) Import multiple PDFs (repeat `--pdf`)

```bash
python skills/zotero-local-import-en/scripts/zotero_tool.py import \
  --pdf "<PDF_PATH_1>" \
  --pdf "<PDF_PATH_2>" \
  --pdf "<PDF_PATH_3>" \
  --port <USER_ZOTERO_PORT>
```

### B) Batch import a folder (non-recursive)

```bash
python skills/zotero-local-import-en/scripts/zotero_tool.py import \
  --dir "<ABSOLUTE_FOLDER_PATH>" \
  --port <USER_ZOTERO_PORT>
```

### C) Batch import a folder (recursive)

```bash
python skills/zotero-local-import-en/scripts/zotero_tool.py import \
  --dir "<ABSOLUTE_FOLDER_PATH>" \
  --recursive \
  --port <USER_ZOTERO_PORT>
```

### D) Import into a specific existing collection

```bash
python skills/zotero-local-import-en/scripts/zotero_tool.py import \
  --dir "<ABSOLUTE_FOLDER_PATH>" \
  --recursive \
  --collection "<EXISTING_COLLECTION_NAME>" \
  --port <USER_ZOTERO_PORT>
```

### D2) Import selected PDFs from a folder (CSV file names)

```bash
python skills/zotero-local-import-en/scripts/zotero_tool.py import \
  --dir "<ABSOLUTE_FOLDER_PATH>" \
  --pick "x.pdf,y.pdf,z.pdf" \
  --collection "<EXISTING_COLLECTION_NAME>" \
  --port <USER_ZOTERO_PORT>
```

Or repeat `--pick`:

```bash
python skills/zotero-local-import-en/scripts/zotero_tool.py import \
  --dir "<ABSOLUTE_FOLDER_PATH>" \
  --pick "x.pdf" \
  --pick "y.pdf" \
  --pick "z.pdf" \
  --port <USER_ZOTERO_PORT>
```

### E) List local collections

```bash
python skills/zotero-local-import-en/scripts/zotero_tool.py list-collections --port <USER_ZOTERO_PORT>
```

### F) Check recently imported attachments

```bash
python skills/zotero-local-import-en/scripts/zotero_tool.py check --limit 10
```

## Key parameters

- `--port`: Zotero connector port (provided by user; defaults to `ZOTERO_PORT` env var, fallback `23119`)
- `--timeout`: HTTP timeout in seconds (default `90`)
- `--collection`: target existing collection name
- `--db`: `zotero.sqlite` path (override for `check`)

## Platform notes

- Windows: supported by default
- macOS: requires `open`
- Linux: requires `xdg-open`

## Failure handling

- `error=collection not found`: create the collection manually in Zotero first
- Connection failures: verify Zotero is running, local-app communication is enabled, and port is correct
- Import failures: retry with one PDF first, then run batch import
