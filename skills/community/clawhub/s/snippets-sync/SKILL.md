---
name: snippets-sync
version: 1.0.0
description: Sync code snippets and notes between machines via file sync. Organized by language, rendered in any Markdown viewer (Obsidian, VS Code, etc.).
env:
  SNIPPETS_VAULT_PATH:
    description: Absolute path to the shared vault directory. Falls back to ~/snippets-vault if unset.
    required: false
---

# Obsidian Skill

## How This Works

The vault is a directory of `.md` files synced between machines (typically via Syncthing, but any file sync works). Anything written to the vault appears on all synced devices.

**Primary use case:** Sharing code snippets, notes, and structured content through Obsidian — persists across sessions, renders nicely in Obsidian, and is searchable.

## Vault Location

Set `SNIPPETS_VAULT_PATH` to your vault directory. Defaults to `~/snippets-vault` if unset. Point this at a dedicated directory — not your home dir or any folder containing secrets.

| | Path |
|---|---|
| Vault | `$SNIPPETS_VAULT_PATH` |
| Synced to | Your other machines via Syncthing/rsync/etc. |

## Reading & Writing Notes

### Direct File I/O (preferred)

Just read/write `.md` files in the vault directory. Obsidian picks up changes automatically via file sync.

### Markdown Format

Notes are plain Markdown with optional YAML frontmatter:

```markdown
---
created: 2026-04-05
tags: [snippet, python]
---

# Note Title

Content here. Use standard Markdown formatting.
```

## Sharing Code Snippets

### Naming Convention

```
code_snippets/
├── python/
│   └── http-server.md
├── bash/
│   └── find-large-files.md
├── typescript/
│   └── debounce.md
├── docker/
│   └── healthcheck.md
└── _uncategorized/
    └── random-thing.md
```

**Rules:**
- **Folder = language/tech** (`python/`, `bash/`, `typescript/`, `docker/`, `sql/`, `lua/`, `gdscript/`, etc.)
- **Filename = what it does** (kebab-case): `json-parser.md`, not `snippet-001.md`
- **No date prefixes** — sort by modified time in Obsidian
- **One snippet per file** — keeps things searchable and linkable
- **`_uncategorized/`** for anything that doesn't fit a clear bucket

### Snippet Template

```markdown
---
created: YYYY-MM-DD
language: <lang>
tags: [snippet, <lang>, <topic>]
---

# Descriptive Title

Description or context here.

\```<lang>
# code here
\```

Usage: `command to run if applicable`
```

### When to Share via Obsidian vs Chat

**Use Obsidian vault when:**
- Code snippets the user might reference later
- Anything with syntax highlighting that benefits from persistence
- Reference material or reusable code

**Use chat directly when:**
- Quick one-off code blocks in active discussion
- Transient stuff that doesn't need to persist

### Notification Convention

When dropping a snippet, send a brief heads-up in chat:
> "Dropped snippet: `code_snippets/python/http-server.md`"

## Markdown Rules

These files render in **Obsidian**, not Discord/chat. Write standard CommonMark Markdown:

- **Headers:** Use `#` / `##` / `###` — never `**bold text**` as a fake header
- **Code blocks:** Always use fenced code blocks with language tag (` ```python `) — never inline backticks for multi-line code
- **No chat-isms:** No `> ` blockquotes for emphasis, no `~~strikethrough~~` abuse, no platform-specific formatting
- **Links:** Wikilinks (`[[other-note]]`) for internal references, standard `[text](url)` for external
- **Lists:** Use `- ` or `1. ` with proper indentation
- **Emphasis:** `*italic*` and `**bold**` are fine — use sparingly, for actual emphasis
- **Tables:** Standard Markdown tables

The goal: clean, readable notes that render well in Obsidian's reading view.

## obsidian-cli (optional)

If `obsidian-cli` is installed and the vault is registered with Obsidian desktop:

```bash
obsidian-cli search "query"              # search note names
obsidian-cli search-content "query"      # search inside notes
obsidian-cli list                         # list files
```

Direct file I/O is the reliable path on headless Linux.

## Safety

- Only read/write `.md` files in the vault directory
- Never touch `.obsidian/` or other app config directories
- Only point `SNIPPETS_VAULT_PATH` at a dedicated snippet/note directory — never at home, `~/.ssh`, password stores, or credential-containing repos
- Files written to the vault propagate to all synced machines

## Tips

- Don't touch `.obsidian/` — that's Obsidian's config
- File sync picks up changes automatically (typically within seconds)
- Wikilinks work: `[[other-note]]` links between notes
- Frontmatter is searchable in Obsidian
- Use folders for organization — Obsidian handles them natively
- Create language subfolders as needed — the vault grows with usage
