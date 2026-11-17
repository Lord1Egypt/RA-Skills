# Smart Files 📁

**Content-aware file management for OpenClaw agents — search, dedup, organize, rename, and auto-watch your workspace.**

## Why Smart Files?

Your workspace grows fast. Files scatter across directories, duplicates pile up, and finding the right file by name alone is slow. Smart Files solves this:

- **Search by content** — Find files by what's *inside* them, not just their names
- **Find duplicates** — SHA-256 content hashing catches identical files anywhere
- **Auto-organize** — Categorize files by type (code, data, docs, media, archives)
- **File intelligence** — Detect file types, line/word counts, metadata
- **Auto-watch** — Monitor a directory and organize new files as they appear
- **Safe by design** — All search/analysis modes are read-only. Watch mode is dry-run by default; `--force` required for any file modification.

---

## Installation

```bash
# Already included in OpenClaw workspace at skills/smart-files/
# No npm install needed — pure Node.js
```

---

## Quick Start

```bash
# Search by content
node skills/smart-files/smart-files.js --search "api key"

# Find duplicates
node skills/smart-files/smart-files.js --dedup

# Workspace overview
node skills/smart-files/smart-files.js --status

# File intelligence
node skills/smart-files/smart-files.js --info some-file.js

# Cleanup analysis
node skills/smart-files/smart-files.js --cleanup .
```

---

## Commands Reference

### File Search

```bash
node skills/smart-files/smart-files.js --search <query> [--dir <path>]
```

Searches file **content** (not just filenames) for the query string. Returns ranked results.

Content snippets are **hidden by default** — only paths and match scores are shown:

```
[smart-files] Found 3 matches for "api key":
  ✅ 1.00 — /path/to/project/config.json
  🔍 0.75 — /path/to/project/src/auth.js
```

To show matched content snippets, add `--snippets`:

```bash
node skills/smart-files/smart-files.js --search "api key" --snippets
```

⚠️ **Privacy**: Without `--quiet`, matched content is read from disk into memory. Snippets are **not redacted** — they print raw text as-is. Do not rely on snippet output as a security boundary when scanning directories containing secrets.

---

### Duplicate Detection

```bash
node skills/smart-files/smart-files.js --dedup [--dir <path>]
```

Groups identical files by SHA-256 content hash. Only compares files of the same size (fast filter), then hashes candidates.

```
[smart-files] Found 2 groups of duplicate files:
  3 files (1.2 KB) — hash: a1b2c3d4e5f6...
    → /path/to/file1.txt
    → /path/to/file2.txt
    → /path/to/file3.txt
```

---

### File Organization (read-only)

```bash
node skills/smart-files/smart-files.js --organize [--dir <path>]
```

Categorizes all files by extension. **Read-only** — shows counts per category, never moves files.

- **code** — .js, .ts, .py, .html, .css, .json, .yaml, .yml, .sh, .go, .rs, .c, .cpp, .java, .rb, .md, .txt, and more
- **data** — .csv, .tsv, .json, .jsonl, .xml, .toml, .ini, .cfg, .env, .sql
- **docs** — .pdf, .doc, .docx, .rtf, .odt, .tex, .epub
- **media** — .jpg, .jpeg, .png, .gif, .svg, .webp, .bmp, .mp4, .mov, .mp3, .wav, .flac
- **archives** — .zip, .tar, .gz, .rar, .7z, .bz2, .xz
- **images** — .ico, .webp, .avif, .tiff, .psd, .ai, .eps

---

### File Intelligence

```bash
node skills/smart-files/smart-files.js --info <filepath>
```

Returns detected type, size, line count, word count, modification date.

```
[smart-files] File info: server.js
  Size: 12.3 KB
  Type: JavaScript/TypeScript
  Lines: 345
  Words: 1,234
  Modified: 2026-07-15
  Path: /path/to/server.js
```

---

### Cleanup Analysis

```bash
node skills/smart-files/smart-files.js --cleanup <dir>
```

Scans for:
- **Temp/backup files** — .tmp, .bak, .swp, .orig, ~files
- **Large files** (>1MB) — candidates for archiving
- **Duplicate groups** — files with identical content

---

### Workspace Status

```bash
node skills/smart-files/smart-files.js --status [--dir <path>]
```

```
[smart-files] Workspace status:
  Total files: 1,234
  Total size: 45.2 MB
  Extensions:
    .js: 342 files, 12.1 MB
    .md: 89 files, 2.3 MB
    .json: 67 files, 8.9 MB
  Largest files:
    data.sqlite — 15.2 MB
    bundle.js — 2.1 MB
```

---

### Dry-Run Rename

```bash
node skills/smart-files/smart-files.js --rename <file> <old>:<new>
```

Pattern-based rename preview. Example:
```bash
node skills/smart-files/smart-files.js --rename server-old.js old:new
# [smart-files] Would rename: server-old.js → server-new.js
# [smart-files] (Use --force to actually rename)
```

---

### Auto-Organize Watcher ⚠️

```bash
# Dry-run preview (DEFAULT — safe, no files touched)
node skills/smart-files/smart-files.js --watch /path/to/dir [--dry-run]

# Actually move/organize files (DESTRUCTIVE — requires explicit --force)
node skills/smart-files/smart-files.js --watch /path/to/dir --force
```

**⚠️ Watch mode is DRY-RUN by default.** It shows what would change without modifying anything. You must use `--force` explicitly to enable destructive operations.

When `--force` is used:
- A 5-second abort window is shown before operations begin
- Files are **copied** to category subdirectories, then **originals are deleted** (copy+unlink — no atomic move)
- This is **inherently destructive** — the original inode is destroyed
- A journal is written to `memory/smart-files-journal.json` for audit trail
- **There is no automatic rollback** — the journal is for manual recovery only
- The watcher runs continuously and modifies files as they appear

**Always run `--dry-run` first** to preview what would change before using `--force`.

**Custom rules** via `.smart-files-rules.json` in the watched directory:
```json
[
  { "exts": [".js", ".ts"], "category": "Scripts" },
  { "exts": [".py", ".rb"], "category": "Scripts" },
  { "exts": [".jpg", ".png"], "category": "Images" }
]
```

Default rules organize into: Pictures, Documents, Videos, Audio, Code, Uncategorized.

---

## Security & Privacy

⚠️ **Smart Files reads file contents** — search results include content snippets. This means file contents enter terminal output and agent context.

| Protection | Details |
|------------|---------|
| **Read-only by default** | `--search`, `--dedup`, `--organize`, `--info`, `--cleanup`, `--status` never modify files |
| **Content snippets hidden** (opt-in) | Snippets only shown with `--snippets`; paths and scores always displayed |
| **Binary detection** | Null-byte check + binary extension filter |
| **Oversized file skip** | Configurable MAX_SCAN_SIZE (10MB default) |
| **No shell execution** | Pure Node.js `fs` ops — no `child_process` |
| **Watch safety gate** | Defaults to dry-run; `--force` required for mutations |
| **Skip directories** | `.git`, `node_modules`, `.npm`, `.cache` excluded by default |
| **Workspace awareness** | Detects and warns when scanning outside workspace |

### Watch Mode Journal ⚠️

Watch mode persists a journal file to track changes:

- **Location:** `<workspace>/memory/smart-files-journal.json`
  (override with `SMART_FILES_WORKSPACE` env var)
- **Contents:** File paths, SHA-256 hashes, sizes, modification times, and change events (new/modified/removed)
- **Not stored:** File contents — only hashes and metadata
- **Size limit:** Journal entries capped at 1000; oldest dropped first on overflow
- **To clear the journal:** Delete `memory/smart-files-journal.json` manually
- **To disable persistence:** The watcher still scans each interval but does not write to disk if you delete the file before running watch mode (the code will recreate it)

```bash
# Clear the watch-mode journal
cp memory/smart-files-journal.json memory/smart-files-journal.backup && > memory/smart-files-journal.json

# Or remove entirely
rm -f memory/smart-files-journal.json
```

### What's NOT Protected

- **No snippet redaction**: Snippets print raw file content as-is — no pattern-based filtering occurs.
- **Content exposure**: When `--snippets` is used, matched content is printed to stdout and may enter agent context. Anyone with terminal access or log access can see them.
- **Watch-mode journal**: File paths, hashes, sizes, and timestamps are persisted to disk (`memory/smart-files-journal.json`). Delete the file to clear; entries capped at 1000.
- **No encryption**: File content is not encrypted at rest or in transit. Smart Files is a local file analysis tool, not a secrets vault.

---

## Programmatic API

```javascript
const SF = require('./skills/smart-files/smart-files.js');

// Search files — each result includes path, score, and raw content snippet
const results = SF.searchFiles('api key', '/path/to/scan');

// Find duplicates
const dupGroups = SF.findDuplicates('/path/to/scan');

// Organize (read-only)
const organized = SF.organizeFiles('/path/to/scan');

// File info
const info = SF.fileInfo('/path/to/file.js');

// Cleanup analysis
const analysis = SF.cleanupFiles('/path/to/scan');

// Status
const status = SF.showStatus('/path/to/scan');

// Path validation
const inWorkspace = SF.isPathWithinWorkspace('/some/path');

// Snippets are raw — no redaction applied
// Results include: { path, name, size, score, snippet }

// Formatting helpers
SF.formatBytes(1024);                    // "1 KB"
SF.charToTokens(100);                    // 25
SF.similarity('hello', 'hello');         // 1
```

---

## Testing

```bash
# Run full test suite (34 tests)
node skills/smart-files/tests/run-self-tests.js

# Legacy CLI smoke tests
node skills/smart-files/test/run-tests.js
```

Test coverage:
- Content search (5 cases)
- Duplicate detection (3 cases)
- File organization (3 cases)
- File info (3 cases)
- Cleanup analysis (3 cases)
- Workspace status (2 cases)
- File rename (3 cases)
- Auto-org watcher functions (2 cases)
- Security & validation (4 cases)
- Helper functions (5 cases)

---

## Configuration

| Variable | Description |
|----------|-------------|
| `SMART_FILES_WORKSPACE` | Override workspace root directory |

Adjust `MAX_SCAN_SIZE` (10 MB default) at the top of `smart-files.js`:
```javascript
const MAX_SCAN_SIZE = 10 * 1024 * 1024; // 10 MB
```

---

## Examples

### Find Todos Across Your Project
```bash
node skills/smart-files/smart-files.js --search "TODO"
```

### Clean Up Your Downloads Folder
```bash
node skills/smart-files/smart-files.js --cleanup ~/Downloads
```

### Preview Watch Mode Before Committing
```bash
# Always dry-run first
node skills/smart-files/smart-files.js --watch ~/Downloads --dry-run

# Then decide if --force is safe
node skills/smart-files/smart-files.js --watch ~/Downloads --force
```

### Find Large Files Taking Space
```bash
node skills/smart-files/smart-files.js --status ~/projects | grep MB
```

---

## License

MIT — Part of the OpenClaw skill ecosystem.

---

## Related Skills

- **Secrets Manager** — Secure encrypted storage for secrets
- **Environment Manager** — Dev environment setup and service tracking
- **Smart Backup** — Automated backup of important files
- **Notification Triage** — Stay notified when files change
RANDOM_UNIQUE_TOKEN_1784758462
