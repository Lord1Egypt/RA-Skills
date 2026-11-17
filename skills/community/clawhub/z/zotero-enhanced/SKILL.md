---
name: zotero-enhanced
description: Zotero library management with PDF metadata auto-fetch (Crossref/arXiv), item search, file read, and note management. Supports cloud and WebDAV storage.
metadata:
  {
    "openclaw":
      {
        "emoji": "📚",
        "homepage": "https://www.zotero.org",
        "requires": {
          "bins": ["curl", "jq", "pdftotext", "zip", "unzip"],
          "env": ["ZOTERO_USER_ID", "ZOTERO_API_KEY"],
          "anyBins": ["md5sum", "md5"]
        },
        "primaryEnv": "ZOTERO_API_KEY",
        "externalServices": {
          "Crossref API": "https://api.crossref.org/",
          "arXiv API": "https://export.arxiv.org/api/",
          "Zotero API": "https://api.zotero.org/",
          "WebDAV server": "user-supplied URL"
        }
      },
  }
---

# Zotero Enhanced Library Manager

This skill provides a suite of scripts to interact with a Zotero library, covering the full document lifecycle: adding, searching, and reading. Includes **enhanced metadata fetching** for PDFs with DOI or arXiv IDs.

## Safety & Security Notes

- **Network**: scripts talk only to the Zotero API (`api.zotero.org`), Crossref, and arXiv; WebDAV scripts additionally talk to your configured WebDAV server. `read_universal.sh` sends the API key only to `https://*.zotero.org` download URLs.
- **Credentials**: passed exclusively via environment variables. `ZOTERO_WEBDAV_URL` must be `https://` — plaintext `http://` is refused so credentials never travel unencrypted.
- **Temporary files**: created in unpredictable per‑run `mktemp -d` directories (mode 0700) and removed on exit; downloaded archives are checked for path‑traversal entries before extraction.
- **Deletion is irreversible**: `delete_note.sh --no-confirm` deletes without asking — intended for non‑interactive automation that has already obtained user consent; verify with `--dry-run` first. `--backup` saves note content to `~/.zotero-backup/` (directory 0700, files 0600) at the user's explicit request.

## Storage Modes

The skill supports two storage configurations:

### 1. Zotero Cloud Storage (Default)
- Uses Zotero's built-in cloud storage (300MB free)
- No WebDAV configuration needed
- File size limit: ~100MB per file
- **Required variables:** `ZOTERO_USER_ID`, `ZOTERO_API_KEY`

### 2. WebDAV Storage
- For users with their own WebDAV server (Synology, Nextcloud, etc.)
- No file size limits (subject to server constraints)
- Supports both `imported_file` (stored directly) and `imported_url` (referenced via WebDAV URL) attachment types
- **Required variables:** `ZOTERO_USER_ID`, `ZOTERO_API_KEY`, `ZOTERO_WEBDAV_URL` (https:// enforced), `ZOTERO_WEBDAV_USER`, `ZOTERO_WEBDAV_PASS`

## Authentication

All scripts require Zotero API credentials. Get your API key from: https://www.zotero.org/settings/keys

- **ZOTERO_USER_ID**: Your Zotero user ID (found in profile URL)
- **ZOTERO_API_KEY**: Your Zotero API key
- **WEBDAV_***: Only required if using WebDAV storage

## 1. Searching for Documents

Use `scripts/search.sh` to find items in the library by keyword.

### Usage
```bash
# Ensure the script is executable
chmod +x scripts/search.sh

# Run the search
ZOTERO_USER_ID="<user_id>" \
ZOTERO_API_KEY="<api_key>" \
bash scripts/search.sh "your search query"
```
The script outputs a formatted list of matching items with their `Key`, needed for reading.

## 2. Reading a Document

### Option A: Universal Reader (Recommended)
Use `scripts/read_universal.sh` to read documents from either storage mode.

#### Usage
```bash
chmod +x scripts/read_universal.sh

# For Zotero cloud storage:
ZOTERO_USER_ID="<user_id>" \
ZOTERO_API_KEY="<api_key>" \
bash scripts/read_universal.sh "ITEM_KEY"

# For WebDAV storage (add WebDAV variables; https:// required):
ZOTERO_USER_ID="<user_id>" \
ZOTERO_API_KEY="<api_key>" \
ZOTERO_WEBDAV_URL="https://<webdav-host>" \
ZOTERO_WEBDAV_USER="<user>" \
ZOTERO_WEBDAV_PASS="<pass>" \
bash scripts/read_universal.sh "ITEM_KEY"
```

### Option B: WebDAV-only Reader
Use `scripts/read.sh` for WebDAV storage only (legacy).

## 3. Managing Notes

The skill now supports creating, reading, updating, and deleting notes in your Zotero library. Notes can be standalone or attached to parent items (documents).

### Creating a Note

Use `scripts/create_note.sh` to create a new note with plain text content.

#### Usage
```bash
chmod +x scripts/create_note.sh

# Create a standalone note:
ZOTERO_USER_ID="<user_id>" \
ZOTERO_API_KEY="<api_key>" \
bash scripts/create_note.sh "My important research notes"

# Create a note attached to a document:
bash scripts/create_note.sh --parent "ITEM_KEY" "Meeting notes about this paper"

# Create a note with tags:
bash scripts/create_note.sh --tag research --tag to-read "Follow up on this paper"
```

#### Options
- `--parent KEY`: Attach note to a parent item (document key)
- `--tag TAG`: Add a tag (can be used multiple times)
- `--dry-run`: Show steps without creating the note

The script automatically converts plain text to HTML for Zotero storage.

### Reading a Note

Use `scripts/read_note.sh` to read a note and convert HTML back to plain text.

#### Usage
```bash
chmod +x scripts/read_note.sh

# Read as plain text (default):
ZOTERO_USER_ID="<user_id>" \
ZOTERO_API_KEY="<api_key>" \
bash scripts/read_note.sh "NOTE_KEY"

# Read as HTML:
bash scripts/read_note.sh --format html "NOTE_KEY"

# Read as JSON (full item data):
bash scripts/read_note.sh --format json "NOTE_KEY"
```

#### Output Formats
- `plain` (default): Human-readable plain text
- `html`: Raw HTML content
- `json`: Full JSON item data

### Updating a Note

Use `scripts/update_note.sh` to update existing notes with new content or tags.

#### Usage
```bash
chmod +x scripts/update_note.sh

# Replace note content:
echo "New content" | \
ZOTERO_USER_ID="<user_id>" \
ZOTERO_API_KEY="<api_key>" \
bash scripts/update_note.sh --replace "NOTE_KEY"

# Append to existing content:
echo "Additional notes" | \
bash scripts/update_note.sh --append "NOTE_KEY"

# Add tags:
bash scripts/update_note.sh --tag important --tag to-read "NOTE_KEY"

# Remove tags:
bash scripts/update_note.sh --remove-tag obsolete "NOTE_KEY"
```

#### Options
- `--replace`: Replace note content (default)
- `--append`: Append new content to existing note
- `--tag TAG`: Add a tag (can be used multiple times)
- `--remove-tag TAG`: Remove a tag (can be used multiple times)
- `--dry-run`: Show steps without updating

The script includes version checking to prevent update conflicts.

### Deleting a Note

Use `scripts/delete_note.sh` to delete notes safely with confirmation and backup options.

#### Usage
```bash
chmod +x scripts/delete_note.sh

# Delete with confirmation:
ZOTERO_USER_ID="<user_id>" \
ZOTERO_API_KEY="<api_key>" \
bash scripts/delete_note.sh "NOTE_KEY"

# Delete without confirmation (use with caution):
bash scripts/delete_note.sh --no-confirm "NOTE_KEY"

# Backup before deleting:
bash scripts/delete_note.sh --backup "NOTE_KEY"

# Dry-run to see what would be deleted:
bash scripts/delete_note.sh --dry-run "NOTE_KEY"
```

#### Safety Features
- **Confirmation prompt**: Requires manual confirmation. `--no-confirm` skips the prompt for non‑interactive automation — the caller is responsible for having user consent; prefer `--dry-run` first
- **Backup option**: Saves note content to `~/.zotero-backup/` before deletion (directory 0700, backup files 0600)
- **Version checking**: Prevents deletion if note was modified by another process
- **Dry-run mode**: Preview deletion without actually deleting

## 4. Adding a New Document

### Option A: Universal Upload with Metadata Fetching (Recommended)
Use `scripts/add_to_zotero_universal.sh` for full metadata fetching and flexible storage.

#### Features
- **Automatic Metadata**: Extracts DOI/arXiv ID, fetches metadata from Crossref/arXiv API
- **Flexible Storage**: Works with both Zotero cloud and WebDAV storage
- **Smart Detection**: Falls back to title extraction if no metadata found
- **Dry-run mode**: Use `--dry-run` to see what would be uploaded without making changes

#### Usage
```bash
chmod +x scripts/add_to_zotero_universal.sh

# Zotero cloud storage (no WebDAV needed):
ZOTERO_USER_ID="<user_id>" \
ZOTERO_API_KEY="<api_key>" \
bash scripts/add_to_zotero_universal.sh "/path/to/paper.pdf"

# WebDAV storage:
ZOTERO_USER_ID="<user_id>" \
ZOTERO_API_KEY="<api_key>" \
ZOTERO_WEBDAV_URL="https://<webdav-host>" \
ZOTERO_WEBDAV_USER="<user>" \
ZOTERO_WEBDAV_PASS="<pass>" \
bash scripts/add_to_zotero_universal.sh "/path/to/paper.pdf"
```

#### Example: Adding a Paper with DOI
The universal script will:
1. Extract DOI `10.1126/science.aec8352` from PDF
2. Query Crossref API for metadata (authors, journal, date, abstract, etc.)
3. Create Zotero item with complete metadata
4. Upload PDF via Zotero API (cloud) or WebDAV (if configured)

### Option B: Enhanced Upload (WebDAV)
Use `scripts/add_to_zotero_enhanced.sh` for WebDAV storage with metadata fetching (DOI/arXiv). Requires WebDAV — for Zotero cloud storage use `add_to_zotero_universal.sh`.

### Option C: Basic Upload (WebDAV)
Use `scripts/add_to_zotero.sh` for WebDAV storage with title‑only extraction. Requires WebDAV — for Zotero cloud storage use `add_to_zotero_universal.sh`.

## 5. Requirements

### Core Dependencies
- `curl`: HTTP requests
- `jq`: JSON processing (for enhanced/universal scripts)
- `pdftotext`: PDF text extraction (from poppler-utils)
- `zip`: File compression (for WebDAV mode)

### Platform Support
All scripts are cross‑platform compatible (Linux and macOS). The universal scripts automatically detect platform‑specific commands (`md5sum`/`md5`, `stat` options).

### Installation (Debian/Ubuntu)
```bash
sudo apt-get update
sudo apt-get install -y curl jq poppler-utils zip
```

### Installation (macOS)
```bash
brew install curl jq poppler zip
```

## Quick Start

1. **Get Zotero API credentials** from your Zotero settings
2. **Install dependencies** as shown above
3. **Check dependencies** (optional but recommended):
   ```bash
   bash scripts/check_deps.sh
   ```
4. **Test search functionality**:
   ```bash
   ZOTERO_USER_ID="1234567" \
   ZOTERO_API_KEY="abc123def456" \
   bash scripts/search.sh "artificial intelligence"
   ```
5. **Add your first paper**:
   ```bash
   ZOTERO_USER_ID="1234567" \
   ZOTERO_API_KEY="abc123def456" \
   bash scripts/add_to_zotero_universal.sh "~/Downloads/paper.pdf"
   ```

## Changelog

### v1.3.14 (2026‑09‑16)
- **Bug fix** (scan finding T09 on v1.3.13, `add_to_zotero_universal.sh`):
  - **Partial WebDAV config now fails closed**: previously the mode banner read WebDAV from URL presence alone, while the actual branch required all three variables — a URL-only setup silently uploaded the PDF to Zotero cloud instead. Now: all three of `ZOTERO_WEBDAV_URL`/`ZOTERO_WEBDAV_USER`/`ZOTERO_WEBDAV_PASS` must be set, or none.
  - **https:// validation moved to startup**: the scheme check runs before any Zotero API write, so a plaintext `http://` URL can no longer leave an orphan item in the library before the script exits.
  - Mode banner now reflects the same all‑three‑variables condition the upload branch uses.
- `_meta.json` version synced to the published version.

### v1.3.13 (2026‑09‑16)
- **Security fixes** (scan findings T09/TM1/EA2 on v1.3.12):
  - `delete_note.sh --backup`: backup directory now created with mode 0700 and backup files set to 0600 (were default umask).
  - `add_to_zotero.sh` / `add_to_zotero_enhanced.sh`: no longer claim “file stored in Zotero cloud” in cloud mode — **these scripts never had a cloud upload path**. They now fail fast with a clear error when WebDAV is not fully configured, before creating any item; use `add_to_zotero_universal.sh` for Zotero cloud storage.
  - SKILL.md/SECURITY.md: `--no-confirm` documented as a risk note (unattended deletion), added a Safety & Security Notes section, corrected the false “supports Zotero cloud” claims for both legacy adder scripts, and qualified the backup exception in SECURITY.md.
- Script versions synced to v1.3.13.

### v1.3.12 (2026‑09‑16)
- **Security hardening** (scan findings T09):
  - `ZOTERO_WEBDAV_URL` must now be an **https://** URL — all five WebDAV scripts (`add_to_zotero.sh`, `add_to_zotero_enhanced.sh`, `add_to_zotero_universal.sh`, `read.sh`, `read_universal.sh`) refuse plaintext `http://` so credentials never travel unencrypted.
  - `read_universal.sh` validates the attachment download URL against an allowlist (`https://*.zotero.org`) before sending the Zotero API key.
  - Temporary files now use unpredictable per‑run directories (`mktemp -d`, 0700) instead of predictable `/tmp` paths; archives are checked for path‑traversal entries before extraction (zip‑slip guard); API‑provided filenames are stripped of path components.
- Script `--version` strings synced to v1.3.12.

### v1.3.11 (2026‑09‑16)
- **Breaking change (env rename)**: WebDAV environment variables renamed to be skill-scoped:
  - `WEBDAV_URL` → `ZOTERO_WEBDAV_URL`
  - `WEBDAV_USER` → `ZOTERO_WEBDAV_USER`
  - `WEBDAV_PASS` → `ZOTERO_WEBDAV_PASS`
- Updated all WebDAV‑touching scripts (`add_to_zotero.sh`, `add_to_zotero_enhanced.sh`, `add_to_zotero_universal.sh`, `read.sh`, `read_universal.sh`, `check_deps.sh`) and `SKILL.md`.
- Internal derived variables (`WEBDAV_BASE_URL`, `WEBDAV_TARGET_URL`, `WEBDAV_SOURCE_URL`) are unchanged.

### v1.3.10 (2026‑08‑10)
- **Bug fix**: Alnum fallback path only applied `_filter_year` + `_filter_issue`, missing `_filter_abstract`, `_filter_keywords`, and `grep -v` exclusions. Now applies the full filter set, matching the CJK branch (review #2).
- **Improvement**: WebDAV `trap` documented as known limitation (overwrites existing EXIT traps; acceptable for standalone script, review #1).
- **Note**: Issues #3 (awk byte/char), #4 (version header skip), #5 (BSD fallback CJK Extension B coverage) acknowledged as low-priority; not blocking.

### v1.3.9 (2026‑08‑10)
- **Bug fix (critical)**: CJK detection `grep '[一-龥]'` is locale-sensitive — fails in `C.UTF-8` (error) and silently matches nothing in `zh_CN.UTF-8`. Replaced with `grep -P '[\x{4E00}-\x{9FFF}]'` (codepoint-based, collation-independent) with BSD grep fallback probe.
- **Bug fix**: Filter patterns `年.*期` / `第.*期` too greedy — killed legitimate titles like "青少年时期心理健康研究". Tightened to `^[0-9０-９]{2,4}.*年` and `第[0-9０-９一二三四五六七八九十]+[期卷]`.
- **Bug fix**: Fullwidth space variants `摘　要` (U+3000) / `关 键 词` not covered. Now using `摘[[:space:]　]*要` / `关[[:space:]　]*键`.
- **Improvement**: Alnum fallback path now applies same header filters as CJK branch (was only scanning 5 lines unfiltered — another regression path to grabbing issue headers).
- **Improvement**: Added `|| true` to `title=$(...)` pipelines for explicit pipefail safety (was safe by accident due to function ending with `echo`).
- **Improvement**: WebDAV upload failure now exits non-zero instead of printing "Success!". Added `trap 'rm -f ...' EXIT` for cleanup on failure/Ctrl-C.
- **Improvement**: `TMP_DIR` now uses `${TMPDIR:-/tmp}` instead of hardcoded `/tmp`.
- **Improvement**: Header version comment updated to match `--version` output.

### v1.3.8 (2026‑08‑10)
- **Bug fix (critical)**: WebDAV upload failed with exit code 3 — `mktemp` creates an empty 0-byte file, then `zip -j` treats it as an invalid existing archive and fails. Replaced `mktemp` with `$TMP_DIR/${ATTACH_KEY}.prop` and `$TMP_DIR/${ATTACH_KEY}.zip` (with `rm -f` guard), which also fixes a secondary bug where files were uploaded with random mktemp names instead of the required `<ATTACH_KEY>.zip`/`<ATTACH_KEY>.prop` filenames.
- **Bug fix**: Chinese paper title extraction grabbed issue headers (e.g. "２０２１年第４期") instead of the actual title. Added `extract_title_from_pdf()` function with CJK-aware filtering: skips date/issue/volume markers, abstracts, keywords, author bios, and fund project notes; strips trailing footnote markers (＊).
- **Improvement**: WebDAV curl uploads now report HTTP status codes instead of failing silently with `-f`.
- **Improvement**: WebDAV upload URL uses explicit filename (`$WEBDAV_BASE_URL/${ATTACH_KEY}.prop`) instead of relying on curl's trailing-slash filename appending behavior.

### v1.3.6 (2026‑06‑11)

- **Security fixes** (CRITICAL): Fixed CRLF injection in multipart form data (`add_to_zotero_universal.sh`) — filename sanitized, all attachment JSON payloads use `jq --arg` instead of raw string interpolation
- **Security fix**: Fixed JSON injection in `update_note.sh` — NOTE_KEY now passed via `jq --arg`
- **Security fix**: Added NOTE_KEY format validation in `delete_note.sh` to prevent path traversal in backup filenames
- **Bug fix**: Fixed `update_note.sh` text-to-HTML conversion — replaced `for`/`IFS` paragraph split with robust `while read` loop
- **Bug fix**: Fixed cross-platform `stat` bug in `read_universal.sh` — now uses `get_filesize()` helper on all platforms
- **Bug fix**: `delete_note.sh` backup now saves full decoded plain-text, not just 3-line preview
- **Improvement**: Added `--help` and `--version` flags to all legacy scripts
- **Version sync**: All script versions normalized to v1.3.6

### v1.3.5 (2026‑06‑11)
- Fixed Chinese error text in `add_to_zotero_universal.sh` (`get_filesize` function)
- Enhanced `create_note.sh` HTML conversion: handles `**bold**`, bullet lists (`-`, `*`, numbered), and inline line breaks (`<br>`)
- Enhanced `read_note.sh` HTML→plaintext conversion: decodes `<br>`, `<strong>`, `<b>`, `<ul>/<li>`, and HTML entities

### v1.3.2 (2026‑03‑31)
- Updated external services metadata in SKILL.md to resolve ClawHub scan errors
- Added external API URLs (Crossref, arXiv, Zotero API, WebDAV) to metadata for better compatibility

### v1.3.1 (2026‑03‑30)
- Fixed version conflict in Clawhub publication

### v1.3.0 (2026‑03‑30)
- Added note management support with four new scripts:
  - `create_note.sh`: Create notes (plain text → HTML, optional parent, tags)
  - `read_note.sh`: Read notes (HTML → text, with format options)
  - `update_note.sh`: Update notes (append/replace, tag management, version checking)
  - `delete_note.sh`: Delete notes (with confirmation, backup option)
- Implemented HTML ↔ plain text conversion for notes
- Added safety features: dry-run mode, confirmation prompts, backup before deletion
- Updated documentation with comprehensive Note Management section

### v1.2.2 (2026‑03‑30)
- Removed library organization tools (`check_attachments.sh`, `find_duplicates.sh`, `analyze_tags.sh`) per user request.
- Reverted documentation to focus on core metadata fetching and file management.

### v1.2.1 (2026‑03‑30)
- Added `imported_url` support in `read_universal.sh` for WebDAV‑stored PDFs.
- Implemented `--dry‑run` mode for `add_to_zotero_universal.sh`.
- Improved argument parsing and help messages.
- Updated security documentation.

### v1.2.0 (2026‑03‑30)
- Cross‑platform compatibility (Linux/macOS) with automatic detection of `md5sum`/`md5` and `stat` variants.
- Added dependency checker script (`check_deps.sh`).
- Added OpenClaw metadata declaration for better integration.
- Added LICENSE and SECURITY.md files.
- Improved script safety headers and `--help`/`--version` flags.

## Troubleshooting

### "No PDF attachment found"
- Ensure the item has an attached PDF (not just a URL)
- Check that attachment has `linkMode: "imported_file"` (stored directly) or `linkMode: "imported_url"` (referenced via WebDAV)
- If using WebDAV, the `read_universal.sh` script will search for both types automatically

### "WebDAV authentication failed"
- Verify WebDAV URL, username, and password
- Test WebDAV access with: `curl -u user:pass "https://your.webdav.server/"`

### "Crossref API failed"
- Check internet connection
- Verify DOI is valid: `curl "https://api.crossref.org/works/10.1126/science.aec8352"`

### "File too large for Zotero API"
- Large files (>100MB) require WebDAV storage
- Set `ZOTERO_WEBDAV_URL` (https:// required), `ZOTERO_WEBDAV_USER`, `ZOTERO_WEBDAV_PASS` variables
