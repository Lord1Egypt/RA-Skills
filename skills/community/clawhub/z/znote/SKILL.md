---
name: znote
description: Create, manage, and operate a Zettelkasten slip-box note system using the zk.py CLI script. Use this skill whenever a user wants to build or use a Zettelkasten note system, manage atomic notes, create fleeting/literature/permanent notes, link notes together, find orphaned notes, generate Maps of Content, or search/browse a note vault. Trigger on phrases like "zettelkasten", "slip box notes", "atomic notes", "permanent notes", "znote", "zk notes", "note vault", "create a note", "link my notes", "find orphaned notes", "map of content", or "manage my notes with zk".
---

# znote: Zettelkasten CLI Note Manager

A single-file Python CLI tool (`zk.py`) implementing the full Zettelkasten method as described in the Desktop Commander / Obsidian Practical Setup Guide. No dependencies beyond Python 3.8+ stdlib. Creates and manages a local markdown vault compatible with Obsidian.

## Inputs

- Python 3.8+ (no pip installs needed)
- Optional: `ZK_VAULT` environment variable to set vault location (default: `~/Zettelkasten`)
- Optional: `EDITOR` environment variable for note editing (default: `nano`)

## Vault Structure

```
~/Zettelkasten/
  00-Inbox/        ← fleeting notes (quick captures)
  10-Literature/   ← one note per source, in your own words
  20-Permanent/    ← atomic notes, one idea, fully linked
  30-MOC/          ← Maps of Content (navigation layers)
  40-Templates/    ← markdown templates for each type
```

## Workflow

### Step 1: Deliver the script

Copy `zk.py` to `/mnt/user-data/outputs/zk.py` and present it to the user via `present_files`. Also deliver `README.md`.

### Step 2: User installs

```bash
chmod +x zk.py
cp zk.py ~/.local/bin/zk        # optional: make globally available
export ZK_VAULT=~/Zettelkasten  # add to ~/.bashrc or ~/.zshrc
```

### Step 3: Initialise vault

```bash
python3 zk.py init
# Creates all 5 folders + 4 markdown templates
```

### Step 4: Daily workflow

**Capture** (fleeting note, no friction):
```bash
zk new fleeting
```

**Process inbox weekly** (flags notes older than 7 days):
```bash
zk inbox
```

**Write permanent notes** (one atomic idea per note):
```bash
zk new permanent "Claim written as a full sentence"
```

**Link notes** — edit the `## Connections` section and add `[[note-stem]]` links.

**Promote fleeting → permanent**:
```bash
zk promote "fragment of title"
```

**Generate Map of Content** when a topic has 8+ notes:
```bash
zk moc "Topic Name"
```

### Step 5: Maintenance commands

```bash
zk links                    # find orphaned notes (no links in/out)
zk links "note title"       # show forward + backlinks for one note
zk graph                    # ASCII link graph of entire vault
zk stats                    # counts, top tags, orphan count
zk search "query"           # full-text search with highlights
zk list --folder permanent  # list notes in a specific folder
zk list --tag psychology    # filter by tag
```

## Output

- `zk.py` — single-file Python CLI, ~400 lines, no dependencies
- `README.md` — full usage guide with workflow and tips
- A local markdown vault fully compatible with Obsidian

## Note Types & Templates

| Type | Folder | Filename pattern | Template fields |
|---|---|---|---|
| Fleeting | `00-Inbox/` | `{timestamp}.md` | created, status |
| Literature | `10-Literature/` | `{date}-{slug}.md` | created, status, source, author, tags |
| Permanent | `20-Permanent/` | `{date}-{slug}.md` | created, status, tags, source, Connections, Source |
| MOC | `30-MOC/` | `MOC-{slug}.md` | created, status, tags, linked notes |

## Key Method Rules (from the guide)

- **One idea per permanent note** — if a second idea appears, create a new note and link
- **Titles are claims**, not topics: `"Attention is a finite resource"` not `"Attention"`
- **Link from day one** — every permanent note needs at least one `[[link]]`
- **Tags supplement links** — use broad tags (`#psychology`), not fine-grained ones
- **MOCs emerge late** — only create when navigation actually becomes difficult
- **Inbox rule** — fleeting notes must be processed within 7 days

## Notes / Edge Cases

- The script uses `[[double-bracket]]` wiki-link syntax identical to Obsidian — vaults are fully interoperable
- Link targets are matched by filename stem (case-insensitive)
- `zk graph` marks missing link targets with `⇢?` in red
- `--no-edit` flag on `new`, `promote`, `moc` skips opening the editor (useful for scripting)
- `ZK_VAULT` env var overrides `--vault` flag and default path
- The `zk promote` command fuzzy-matches on filename and note body content
- Templates folder is excluded from stats/orphan counts automatically
