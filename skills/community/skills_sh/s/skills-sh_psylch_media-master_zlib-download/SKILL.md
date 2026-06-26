---
name: zlib-download
description: Search and download books from Z-Library and Anna's Archive. Use when user wants to find, search, download, or look up books, papers, or ebooks. Trigger phrases include "find book", "search book", "download book", "找书", "下载书籍", "搜书", "book search", "zlibrary", "anna's archive".
---

# Book Tools

Search and download books from multiple sources through a unified CLI.

## Language
**Match user's language**: Respond in the same language the user uses.

## Backends

| Backend | Source | Auth Required | Best For |
|---------|--------|---------------|----------|
| **zlib** | Z-Library (EAPI) | Email + Password | Largest catalog, direct download |
| **annas** | Anna's Archive | API Key (donation) | Aggregated sources, multiple mirrors |

## Preflight

Before any workflow, run preflight to check environment readiness:

```bash
python3 ${SKILL_PATH}/scripts/book.py preflight
```

Returns standardized JSON:
```json
{
  "ready": true,
  "dependencies": { "python3": {"status": "ok"}, "requests": {"status": "ok"} },
  "credentials": { "zlib": {"status": "configured"}, "annas_api_key": {"status": "not_configured"} },
  "services": { "annas_binary": {"status": "ok"} }
}
```

- If `ready: true` — proceed directly to the Workflow section.
- If `ready: false` — follow the Check/Fix table below, then run the Setup flow.

| Check | Fix |
|-------|-----|
| `requests` missing | `bash ${SKILL_PATH}/scripts/setup.sh install-deps` (or manually: `pip3 install requests` / `uv pip install requests`) |
| `zlib` not configured | Guide user to edit `~/.claude/book-tools/.env` — set `ZLIB_EMAIL` and `ZLIB_PASSWORD` |
| `zlib` expired | Cached tokens expired and no email/password in `.env`. Guide user to re-add credentials to `~/.claude/book-tools/.env` |
| `annas_api_key` not configured | Guide user to donate at Anna's Archive for API key, then add `ANNAS_SECRET_KEY` to `~/.claude/book-tools/.env` |
| `annas_binary` missing | `bash ${SKILL_PATH}/scripts/setup.sh install-annas` (or manually: download from [annas-mcp releases](https://github.com/iosifache/annas-mcp/releases), extract to `~/.local/bin/annas-mcp`) |

## Setup (First-Time Only)

Only run setup when preflight reports `ready: false`. Guide the user through configuration interactively.

### Step 1: Install Dependencies

```bash
bash ${SKILL_PATH}/scripts/setup.sh install-deps
```

### Step 2: Configure Credentials

Credentials are stored in `~/.claude/book-tools/.env`. Create the file from the skill's bundled template:

```bash
mkdir -p ~/.claude/book-tools
# Only copy if .env does not already exist — never overwrite existing credentials
if [ ! -f ~/.claude/book-tools/.env ]; then
  cp ${SKILL_PATH}/scripts/.env.example ~/.claude/book-tools/.env
else
  echo "Existing .env found — skipping copy to preserve your credentials."
fi
```

The `.env` file looks like this:

```
# Z-Library credentials
ZLIB_EMAIL=your_email@example.com
ZLIB_PASSWORD=your_password_here

# Anna's Archive (optional, requires donation for API key)
# ANNAS_SECRET_KEY=your_api_key_here
```

**IMPORTANT**: Do NOT ask the user for credentials directly in chat. Instead:
1. Create the `.env` file (or `.env.example` template)
2. Tell the user to edit `~/.claude/book-tools/.env` with their credentials
3. Wait for the user to confirm they've filled it in
4. Then proceed with search

### Step 3: Verify

```bash
python3 ${SKILL_PATH}/scripts/book.py preflight
```

Confirm `ready: true` before proceeding.

### Credential Storage

**Canonical path**: `~/.claude/book-tools/.env` — this is the single place users should edit credentials.

| Variable | Purpose | Required |
|----------|---------|----------|
| `ZLIB_EMAIL` | Z-Library email | For Z-Library backend |
| `ZLIB_PASSWORD` | Z-Library password | For Z-Library backend |
| `ANNAS_SECRET_KEY` | Anna's Archive API key | For Anna's Archive backend |

On first successful Z-Library login, session tokens are automatically cached in `~/.claude/book-tools/config.json` for performance. This file is auto-managed — do not edit it manually. If login issues occur, delete `config.json` and the script will re-login using `.env` credentials.

## Workflow

The typical flow is: **search → pick → download**.

### 1. Search

```bash
# Auto-detect backend (tries zlib first, then annas)
python3 ${SKILL_PATH}/scripts/book.py search "machine learning" --limit 10

# Z-Library with filters
python3 ${SKILL_PATH}/scripts/book.py search "deep learning" --source zlib --lang english --ext pdf --limit 5

# Anna's Archive
python3 ${SKILL_PATH}/scripts/book.py search "reinforcement learning" --source annas

# Chinese books
python3 ${SKILL_PATH}/scripts/book.py search "莱姆 索拉里斯" --source zlib --lang chinese --limit 5
```

**Output** (JSON to stdout):
```json
{
  "source": "zlib",
  "count": 5,
  "books": [
    {
      "source": "zlib",
      "id": "12345",
      "hash": "abc123def",
      "title": "Deep Learning",
      "author": "Ian Goodfellow",
      "year": "2016",
      "language": "english",
      "extension": "pdf",
      "filesize": "22.5 MB"
    }
  ]
}
```

### 2. Present Results to User

After searching, present results as a **numbered table** so the user can pick:

```
| # | Title | Author | Year | Format | Size |
|---|-------|--------|------|--------|------|
| 1 | Deep Learning | Ian Goodfellow | 2016 | pdf | 22.5 MB |
| 2 | ... | ... | ... | ... | ... |
```

If results span multiple languages or editions, **group them by language or category** with sub-headings for clarity.

Ask: "Which book would you like to download? (number)"

### 3. Download

```bash
# Z-Library download (needs id + hash from search results)
python3 ${SKILL_PATH}/scripts/book.py download --source zlib --id 12345 --hash abc123def -o ~/Downloads/

# Anna's Archive download (needs MD5 hash from search results)
python3 ${SKILL_PATH}/scripts/book.py download --source annas --hash a1b2c3d4e5 --filename "deep_learning.pdf" -o ~/Downloads/
```

**Output**:
```json
{
  "source": "zlib",
  "status": "ok",
  "path": "~/Downloads/Deep Learning (Ian Goodfellow).pdf",
  "size": 23592960
}
```

### 4. Report to User

After download, present a structured completion report:

```
[Book Download] Complete!
Book: [title] by [author]
Source: [zlib/annas]
Path: [file path]
Size: [file size]
```

If using Z-Library, also mention any remaining daily download quota.

## Other Commands

### Book Info (Z-Library only)

```bash
python3 ${SKILL_PATH}/scripts/book.py info --source zlib --id 12345 --hash abc123def
```

Returns full metadata: description, ISBN, pages, table of contents, etc.

### Check Config

```bash
python3 ${SKILL_PATH}/scripts/book.py config show
```

### Check Backend Status

```bash
python3 ${SKILL_PATH}/scripts/book.py setup
```

## Error Handling

| Error | Cause | Action |
|-------|-------|--------|
| "Z-Library not configured" | No credentials | Guide user to edit `~/.claude/book-tools/.env` |
| "Z-Library login failed" | Bad credentials or service down | Ask user to verify credentials. Z-Library domains change — if persistent, the vendored `Zlibrary.py` domain may need updating. |
| "annas-mcp binary not found" | Binary not installed | Run `setup.sh install-annas` |
| "Anna's Archive API key not configured" | No API key | Guide user to donate at Anna's Archive for API access, then add key to `.env` |
| Search timeout | Network issue | Retry once. If persistent, try the other backend. |
| "No backend available" | Neither backend configured | Walk through full setup flow from Step 1 |

## Degradation

| Scenario | Behavior |
|----------|----------|
| Z-Library down | Auto-fallback to Anna's Archive (`--source auto` handles this) |
| Anna's Archive unavailable | Use Z-Library only |
| Neither configured | Halt and guide user through Setup flow |

## Tips

- Z-Library has a daily download limit (usually 10/day for free accounts). Use `info` to check a book before downloading to avoid wasting quota.
- Anna's Archive requires an API key for both search and download (obtained via donation).
- For Chinese books, use `--lang chinese` with Z-Library for best results.
- If Z-Library is unreachable, automatically fall back to Anna's Archive with `--source auto`.
- When searching for a specific author in multiple languages, run parallel searches (e.g. English name + Chinese name) and merge results into one table.
