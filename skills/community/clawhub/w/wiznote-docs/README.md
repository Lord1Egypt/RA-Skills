# wiznote

Use WizNote as your doc source of truth in Claude-driven development.

English | [简体中文](./README.zh-CN.md)

`wiznote` is a public, privacy-safe Claude skill and Python helper set for developers who want a lightweight documentation workflow: private WizNote deployment, repo-local mirrors, and Claude-friendly operations in one package.

It is built for personal developers and small teams doing vibe coding, where plans, notes, specs, and implementation context need to stay close to the code without introducing a heavy documentation platform.

## Why developers may want this

- **Private by default** — connect to your own WizNote deployment instead of moving docs into a public SaaS workspace
- **Claude-friendly workflow** — pair the same doc system with Claude Code and adjacent desktop, web, or IDE-centered repo workflows
- **Cross-end continuity** — write or sync on one surface, continue from another, and keep the same documentation source of truth
- **Built for personal or small-team vibe coding** — keep docs, plans, and implementation notes tightly coupled to the codebase
- **Repo mirrors included** — keep WizNote as canonical while preserving code-adjacent Markdown copies in `docs/wiznote-mirror/...`

This package is derived from a private internal workflow, but all user-specific paths, hosts, credentials, and organization-specific folder mappings have been removed.

## What it includes

- `SKILL.md` — the Claude Code skill definition
- `wiznote_cli.py` — login, list, download, create, and update note helpers
- `wiznote_helper.py` — category validation, mirror-path generation, and HTML body extraction helpers
- `tests/` — pytest coverage for the publicized helper and CLI behavior

## Features

- Log in to a WizNote server with explicit credentials or environment variables
- List notes under a configurable category root
- Download note HTML
- Create new notes from generated HTML
- Update existing notes
- Mirror notes into `docs/wiznote-mirror/...` safely
- Validate category paths so sync stays inside your chosen root
- Support Unicode note titles for mirror filenames

## Requirements

- Python 3.11+ recommended
- A reachable WizNote server
- Optional Python packages depending on your workflow:
  - `markdown` for Markdown → HTML conversion
  - `pytest` for running the included tests

## Installation

### Option 1: Use as a Claude Code skill

Copy this directory to your Claude skills directory:

```bash
mkdir -p ~/.claude/skills
cp -R ./wiznote ~/.claude/skills/wiznote
```

### Option 2: Keep it in your repository

You can also keep `wiznote/` inside your repo and import the Python files directly in your own scripts.

## Configuration

Set these environment variables:

```bash
export WIZNOTE_BASE_URL="https://notes.example.com"
export WIZNOTE_USER="you@example.com"
export WIZNOTE_PASSWORD="your-password"
```

You also need two runtime values in your scripts:

- `category_root` — the top-level WizNote category you want to sync under, for example `/team/docs/`
- `repo_root` — the local repository root used for mirror output

## Quick start

### 1. Import the helpers

```python
from pathlib import Path
import sys

SKILL_DIR = Path("/path/to/wiznote")
sys.path.insert(0, str(SKILL_DIR))

import wiznote_cli as cli
import wiznote_helper as helper
```

### 2. Load credentials and log in

```python
creds = cli.load_credentials()
login = cli.login(creds)
```

Or pass credentials explicitly:

```python
creds = cli.load_credentials(
    base_url="https://notes.example.com",
    user="you@example.com",
    password="your-password",
)
login = cli.login(creds)
```

### 3. Choose a category root and target category

```python
category_root = helper.normalize_category_root("/team/docs/")
category = helper.resolve_category(category_root, "plans/")
```

### 4. List notes

```python
payload = cli.fetch_note_list(
    base_url=login.kb_server,
    kb_guid=login.kb_guid,
    token=login.token,
    category=category,
)
```

### 5. Create a note

```python
html = "<h1>Project Design</h1><p>...</p>"

result = cli.create_note(
    base_url=login.kb_server,
    kb_guid=login.kb_guid,
    token=login.token,
    title="Project Design",
    category=category,
    html=html,
)
```

### 6. Build a safe local mirror path

```python
mirror_path = helper.mirror_output_path(
    repo_root=Path("/path/to/repo"),
    category_root=category_root,
    category=category,
    title="Project Design",
)
```

## Recommended sync flow

1. Configure credentials
2. Normalize the category root
3. Log in once and reuse the session
4. Resolve the exact target category
5. List notes before writing
6. Convert Markdown to HTML
7. Create or update the note in WizNote first
8. Refresh the local mirror second
9. Re-list the category to verify the write

## Markdown to HTML

`create_note(...)` and `save_note(...)` expect HTML, not raw Markdown.

Example:

```bash
python3 -m pip install markdown
```

```python
import markdown

html = markdown.markdown(text, extensions=["extra", "fenced_code", "tables", "sane_lists"])
```

## Running tests

```bash
python3 -m pip install pytest
pytest wiznote/tests
```

## Privacy and publishing notes

This public version intentionally avoids:

- hardcoded home directories
- private server addresses
- usernames or passwords
- organization-specific project folder mappings

If you fork or modify it, keep your published copy free of private infrastructure details.

## File layout

```text
wiznote/
├── README.md
├── README.zh-CN.md
├── SKILL.md
├── wiznote_cli.py
├── wiznote_helper.py
└── tests/
    ├── conftest.py
    ├── test_cli.py
    └── test_helper.py
```

## License

MIT. See [`LICENSE`](./LICENSE).
