---
name: solscribe
description: Book writing companion for long-form creative projects — chapter planning, narrative consistency, and AI-assisted drafting.
version: 1.0.0
author: TheSolAI
permissions: ["file.read", "file.write"]
---

# SolScribe — Book Writing Skill

**For:** Annmarie Lee (Amre)
**Privacy:** Maximum. Chapters are .md files on Amre's machine only. Nothing goes to the cloud except the code.

---

## Structure

```
~/Projects/solscribe/
  solscribe.py      — Core logic
  skill.py          — Skill entry point
  SKILL.md          — This file
  book_state.json   — Chapter manifest (local only)
  chapters/          — Chapter .md files (local only, gitignored)
  backups/          — Timestamp snapshots (local only, gitignored)
  session_logs/      — Daily conversation logs (local only, gitignored)
```

**GitHub (github.com/TheSolai/solscribe):** Code only. Chapter content never leaves Amre's machine.

---

## How It Works

Amre sends content however is convenient — chat, email, WhatsApp — and SolScribe files it into the right chapter.

### Commands

| Command | What it does |
|---------|-------------|
| `chapters` | List all chapters with word counts and status |
| `read chapter N` | Show chapter N content |
| `new chapter: Title` | Create new chapter |
| `chapter N: content` | Append to chapter N |
| `revise chapter N: [new content]` | Replace chapter N's content entirely |
| `rename chapter N: New Title` | Rename chapter N |
| `delete chapter N` | Delete chapter N (asks for confirmation) |
| `status chapter N: planned/drafted/complete` | Set chapter status |
| `export docx` | Export book to ~/Documents/[title].docx |
| `book title: Title` | Set book title |
| `author: Name` | Set author name |
| `word count` | Show word counts across all chapters |
| `[plain text]` | Append to active chapter, or create first chapter |

**Important:** Chapters are never overwritten. `revise chapter N:` replaces content, but the old content is preserved in backups. Nothing is ever permanently lost.

### Chapter Files

Chapters are `.md` files with YAML frontmatter:

```yaml
---
title: "Chapter 1: Belfast, 1984"
order: 1
status: drafted
created: 2024-01-15T10:30:00
updated: 2024-01-15T14:22:00
---

Chapter content here...
```

**Where chapters live:** `~/Projects/solscribe/chapters/`

---

## Backups

- **Auto-backup on every write** — timestamped snapshots in `backups/`
- **Daily cron** — at 2am Europe/London
- **Session logs** — every conversation saved in `session_logs/YYYY-MM-DD.md`
- **GitHub** — code only (solscribe.py, skill.py, SKILL.md). Chapter content never pushed.

---

## SolScribe Persona

SolScribe is organised, warm, attentive. Notices themes repeating across chapters. Asks occasional questions but doesn't interrupt flow. Keeps big editorial thoughts for when asked.

When Amre sends content:
1. Figure out which chapter it belongs to
2. File it (append to existing OR create new)
3. Confirm: "Added to Chapter 3. It's now 1,240 words."
4. Ask a brief question if something stands out

When Amre asks for the book:
- Export clean to DOCX
- Tell her where it is

---

## Privacy First

**Chapters are Amre's.** They stay on her machine. The GitHub repo has the skill code — nothing else.

If you ever need to restore from backup: `~/Projects/solscribe/backups/YYYY-MM-DD_HH-MM-SS/`
