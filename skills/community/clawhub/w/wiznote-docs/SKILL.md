---
name: wiznote
description: Use when documents must be read from or maintained in a WizNote or 为知笔记 server, mirrored into a local repository, or organized under a configurable note category root.
---

# WizNote

## Overview
Use WizNote as the canonical document store and keep local repository copies as mirrors. This public version is generic: you supply your own server URL, credentials, category root, and repository paths.

## When to Use
- The user mentions WizNote, 为知笔记, internal note servers, or doc sync.
- The user wants docs read from WizNote and mirrored locally.
- The user wants local project docs uploaded into WizNote.
- The user needs a reusable pattern for note sync without hardcoded organization folders.

Do not use this skill for unrelated documentation systems.

## What This Public Copy Removes
- No hardcoded user home directory.
- No hardcoded server address.
- No hardcoded account or password.
- No fixed organization-specific project mapping.

## Required Configuration
New users must provide these values themselves:

- `WIZNOTE_BASE_URL` — base URL of the WizNote server, for example `https://notes.example.com`
- `WIZNOTE_USER` — WizNote login user ID or email
- `WIZNOTE_PASSWORD` — WizNote password
- `category_root` — the top-level WizNote category path to sync under, for example `/team/docs/`
- `repo_root` — local repository root used for mirror output

You can pass credentials explicitly or set environment variables.

## Available Helpers
Support files live in the same directory:
- `wiznote_cli.py`
- `wiznote_helper.py`

Key functions:
- `load_credentials(...)`
- `login(...)`
- `fetch_note_list(...)`
- `fetch_note_html(...)`
- `create_note(...)`
- `save_note(...)`
- `normalize_category_root(...)`
- `resolve_category(...)`
- `mirror_output_path(...)`
- `extract_html_body(...)`

## Quick Reference

### 1. Import the helpers
```python
from pathlib import Path
import sys

SKILL_DIR = Path("/path/to/wiznote")
sys.path.insert(0, str(SKILL_DIR))

import wiznote_cli as cli
import wiznote_helper as helper
```

### 2. Configure credentials
Environment variables:
```bash
export WIZNOTE_BASE_URL="https://notes.example.com"
export WIZNOTE_USER="you@example.com"
export WIZNOTE_PASSWORD="your-password"
```

Or pass them directly:
```python
creds = cli.load_credentials(
    base_url="https://notes.example.com",
    user="you@example.com",
    password="your-password",
)
```

### 3. Login once and reuse the session
```python
creds = cli.load_credentials()
login = cli.login(creds)
```

### 4. Resolve the category root and target category
```python
category_root = helper.normalize_category_root("/team/docs/")
category = helper.resolve_category(category_root, "plans/")
```

### 5. List notes in a category
```python
payload = cli.fetch_note_list(
    base_url=login.kb_server,
    kb_guid=login.kb_guid,
    token=login.token,
    category=category,
)
```

### 6. Download note HTML
```python
html = cli.fetch_note_html(
    base_url=login.kb_server,
    kb_guid=login.kb_guid,
    doc_guid="<doc-guid>",
    token=login.token,
)
body = helper.extract_html_body(html)
```

### 7. Create or update a note
`create_note(...)` and `save_note(...)` expect HTML, not Markdown. Convert local Markdown before upload.

```python
result = cli.create_note(
    base_url=login.kb_server,
    kb_guid=login.kb_guid,
    token=login.token,
    title="Project Design",
    category=category,
    html="<h1>Project Design</h1><p>...</p>",
)
```

### 8. Build the mirror path safely
```python
mirror_path = helper.mirror_output_path(
    repo_root=Path("/path/to/repo"),
    category_root=category_root,
    category=category,
    title="Project Design",
)
```

## Operating Pattern
1. Set `WIZNOTE_BASE_URL`, `WIZNOTE_USER`, and `WIZNOTE_PASSWORD`, or pass them explicitly.
2. Normalize your chosen category root with `normalize_category_root(category_root)`.
3. Log in once and reuse `login.token`, `login.kb_server`, and `login.kb_guid`.
4. For reads: resolve the target category, list notes, choose the target note, download HTML, then mirror locally if needed.
5. For writes: prepare HTML, create or update the note in WizNote first, then refresh the local mirror.
6. Re-list the category after each write to verify the note exists.

## Setup Steps For New Users
1. Copy this `wiznote/` directory into your repo or your Claude skills directory.
2. Install Python 3.
3. If you need Markdown-to-HTML conversion, install a Markdown library such as `markdown`:
   ```bash
   python3 -m pip install markdown
   ```
4. Confirm your WizNote server is reachable from the Python runtime you plan to use.
5. Set the three required environment variables or pass credentials explicitly.
6. Choose a category root like `/team/docs/` and keep all synced notes under it.
7. Test login and note listing before doing bulk writes.

## Mirror Rules
- Canonical source: WizNote.
- Local repo copy: mirror.
- Mirror destination must be produced by `mirror_output_path(repo_root, category_root, category, title)`.
- Reject paths outside the configured category root.

## Common Mistakes
- **Leaving private values in the published skill.** Keep server URLs, usernames, passwords, and local home paths out of the shared copy.
- **Writing only to the repo mirror.** Update WizNote first when the user wants centralized maintenance.
- **Uploading raw Markdown to `create_note(...)`.** Convert to HTML first.
- **Building target categories manually without validation.** Use `normalize_category_root(...)` and `resolve_category(...)`.
- **Building local paths from raw titles.** Use `mirror_output_path(...)` to avoid path escape issues.
- **Logging in for every note.** Reuse one authenticated session for the batch.
