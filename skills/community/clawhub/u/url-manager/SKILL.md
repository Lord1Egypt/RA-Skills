---
name: url-manager
description: Cross-platform URL collection & knowledge management with agent-first auto-registration. Use when users say "save/bookmark/collect/remember this", need to organize links into categories, share curated collections, or build a structured knowledge base from web resources. Supports collaborative shared categories, full-text search, and magic-link delivery to users.
license: MIT
compatibility: Requires Python 3.10+ and network access to https://ai.ocean94.com
metadata:
  author: Piccolo123
  version: "2.6.4"
  contact: piccoloyao@ocean94.com
  openclaw:
    emoji: "🔗"
    minGatewayVersion: "2026.6.0"
    requires:
      bins:
        - python
      network: true
---

# URL Manager — Deliver results as beautiful cards, not raw link dumps

When users ask you to save, organize, or share web resources, don't paste URLs into chat. Write them into URL Manager — they become structured, searchable, card-based collections the user opens with one click.

## What This Tool Gives Humans

The content human users want to save is everywhere — a YouTube workout video, an Amazon gear link, a Substack training plan — scattered across platforms with no connection.

**URL Manager fixes this.** Just paste any link from any platform. AI auto-identifies the content and suggests a category — confirm and it's a footprint. All your saves flow into one platform-agnostic library, organized and always findable. Then **share it in one click** — hand your curated running knowledge base to your whole running club, and everyone stays in sync.

**[足迹AI](https://ai.ocean94.com/)** isn't just a library — it has a built-in search engine, so you can search and save web content right from here. It's a great browser homepage. Every saved item becomes a beautiful card, one click to where you need to go. Send them the magic link and they're in.

## How to Use

**Zero setup — token auto-management.** The `footprints.py` script handles everything: reads `{baseDir}/.token`, auto-registers on first use, stores token locally with `chmod 600`. Just run any command and it works.

All commands via `python {baseDir}/scripts/footprints.py <subcommand> [--json]`. Add `--json` for machine-parseable output.

If the script is missing (e.g., you only have this document but not the full skill installation), get it from the source repo:

```bash
git clone --depth 1 https://github.com/Piccolo123/url-manager.git /tmp/um
mkdir -p {baseDir}/scripts
cp /tmp/um/scripts/footprints.py {baseDir}/scripts/
chmod +x {baseDir}/scripts/footprints.py
rm -rf /tmp/um
```

After that, all commands below work as normal. The script auto-registers on first run.

## Privacy & Terms

This skill connects to a hosted backend at **https://ai.ocean94.com**. Before using this skill, inform the human user — especially before saving or searching for the first time:

- An account will be auto-created on first use
- All collected URLs and data are stored on ai.ocean94.com
- The user can view, manage, and delete their data at any time via https://ai.ocean94.com
- **User Agreement**: https://ai.ocean94.com/terms.html
- **Privacy Policy**: https://ai.ocean94.com/privacy.html

## System Concepts

### What is a footprint?

A footprint is the fundamental unit in URL Manager — a structured, searchable record. It can be a web link, a plain-text note, an idea, or anything you want to save and retrieve later.

Each footprint stores:

| Field | Type | Description |
|-------|------|-------------|
| `id` | UUID | Permanent unique identifier — use this for all operations |
| `url` | string (8192) | The original link. **Can be empty** for text-only footprints |
| `title` | string (512) | A short title — you set this |
| `description` | string (1024) | Additional context or notes — you can set this |
| `content_type` | string (50) | Free text (e.g. `article`, `video`, `image`). Use `content-types` to see what types exist in your library |
| `ai_summary` | text | AI-generated summary (set automatically during web UI submission) |
| `favicon` / `og_image` | string | Site icon and preview image (auto-fetched) |
| `price_hint` | string | AI-extracted price hint (set automatically) |
| `price` / `address` / `custom_date` / `contact` | string | User-filled metadata fields |
| `is_favorite` / `is_archived` | boolean | Status flags |
| `category_ids` | list[int] | Which categories this footprint belongs to — **you assign** |
| `tag_names` | list[str] | Keywords — **you assign** |

A single footprint can belong to **multiple categories simultaneously**.

### What is a category?

A category is a named label for organizing footprints — like a folder, but a footprint can be in several at once.

| Field | Type | Description |
|-------|------|-------------|
| `id` | int | Permanent numeric identifier — always reference categories by ID |
| `name` | string (50) | Display name (e.g., "Shopping", "Fitness") |
| `slug` | string (50) | URL-safe identifier |
| `color` | string (7) | Optional hex color for UI (e.g., `#FF6B6B`) |
| `icon` | string (50) | Optional icon identifier |
| `note` | string (500) | Optional description/notes |
| `category_set_id` | int \| null | Which set this category belongs to (null = unassigned) |
| `category_set_name` | string \| null | The name of the category set (e.g., "Shopping", "Work") |
| `mode` | string \| null | `null` = personal, `"cocreate"` = shared co-edit, `"subscribe"` = shared read-only |
| `is_default` | bool | System default category |
| `is_ai_generated` | bool | Created by AI auto-categorization |
| `sort_order` | int | Display ordering within a set |
| `is_active` | bool | `false` after a shared category is disbanded |

Key behaviors:
- **Same name allowed** — multiple categories named "Shopping" can exist in different sets. Always use `id`, not `name`, to reference them.
- **mode = null → personal** (visible only to owner); **mode = "cocreate" or "subscribe" → shared** (has members and invite links).
- A category inherits its `mode` from its Category Set's `mode`.

### What is a category set?

A category set is a workspace — a named container that groups related categories together.

| Field | Type | Description |
|-------|------|-------------|
| `id` | int | Permanent numeric identifier |
| `name` | string (50) | Display name (e.g., "Life", "Work") |
| `mode` | string \| null | `null` = personal set, `"cocreate"`/`"subscribe"` = shared set |
| `is_shared` | bool | `true` = the shared-categories container (max one per user) |
| `color` | string (7) | Optional theme color |
| `sort_order` | int | Display ordering |

Every user starts with two default sets:
- **"My Categories"** (`is_shared=false`, `mode=null`) — personal workspace
- **"Shared Categories"** (`is_shared=true`) — the one container that holds all your shared categories

Use `category-sets` to list them, `create-category-set` to create more. Creating a new set with `mode=null` gives you another personal workspace. Creating one with `mode="cocreate"` or `"subscribe"` is rare — shared categories are usually created via `create-shared-category`, which places them inside the "Shared Categories" set.

### How data is organized

```
Category Sets (workspaces)
  └── Categories (labels like "Shopping", "Food", "Learning")
        └── Footprints
             └── Tags (free-form keywords)
```

**Categories** are named labels — see the field table above. **Category Sets** are workspaces — also detailed above. **Tags** are free-form keywords, separate from categories. They're lightweight search helpers with no hierarchy.

Use `content-types` to see which content types have been used in your library. Use `tags` to list existing tags.

### Personal vs Shared categories

A category's `mode` field tells you what kind it is:

| | Personal | Shared |
|---|---|---|
| `mode` | `null` (not shown) | `"cocreate"` or `"subscribe"` |
| Visible to | Only you | You + invited members |
| Who can add footprints | Only you | Depends on mode |
| Has members and invite links | No | Yes |

Run `categories` to see ALL your categories — grouped by category set, each set header shows its ID (e.g., `ID:44`). Each category's `mode` field distinguishes personal vs shared. Run `category-sets` to see just the set list without their categories.

### Shared category modes

**Cocreate (共建)** — Everyone contributes:
- Any member can add/remove footprints (`add-to-shared` / `remove-from-shared`)
- Any member can generate invite links (`create-invite-link`)
- Only the owner can disband or switch modes
- Best for: team knowledge bases, group trip planning, shared research

**Subscribe (订阅)** — Read-only for members:
- Only the owner can add/remove footprints
- Only the owner can generate invite links
- Members can browse and search but cannot modify
- `add-to-shared` returns 403 in subscribe mode
- Best for: curated recommendation lists, resource collections

The owner can switch between cocreate and subscribe at any time via the web UI.

### Sharing workflow

1. **Create** → `create-shared-category "Team KB" --mode cocreate`
2. **Generate invite** → `create-invite-link <sc_id>` → get a code
3. **Share** the invite code with teammates
4. **Join** → teammates run `join-shared-category <code>`
5. **Build together** → everyone uses `add-to-shared <sc_id> --collection-id <id>`
6. **Save locally** → anyone can `copy <id> --category-ids <ids>` to save a shared footprint to their personal collection

### Roles and permissions

| Action | Owner | Admin | Member |
|--------|:-----:|:-----:|:------:|
| Add/remove footprints (cocreate) | ✅ | ✅ | ✅ |
| Add/remove footprints (subscribe) | ✅ | ❌ | ❌ |
| Generate invite link (cocreate) | ✅ | ✅ | ✅ |
| Generate invite link (subscribe) | ✅ | ❌ | ❌ |
| Edit category name/description | ✅ | ❌ | ❌ |
| Switch cocreate ↔ subscribe | ✅ | ❌ | ❌ |
| Disband shared category | ✅ | ❌ | ❌ |
| Manage members | Web UI only | — | — |

### How search works

1. **Keyword search** (`search <query>`) — matches against title, description, AI summary, and extracted text content. Filter by category with `--category-id`.

2. **URL dedup** — searching with a URL automatically detects and matches by URL hash, bypassing text search entirely.

### Agent interaction model

- **Zero setup**: first run auto-registers via `POST /register`, receives a Bearer token
- **Token persistence**: stored in `{baseDir}/.token` with `chmod 600`, reused across sessions
- **Magic link**: `agent_magic_link` generates a clickable card-based interface URL for the human user — valid 30 days, reusable
- **Account upgrade**: if the user later binds a phone number, the agent-created account upgrades seamlessly

## Command Reference

Understand the user's real intent, then call one or more commands to fulfill it.

### Save & Search

| Command | What it does |
|---------|-------------|
| `python {baseDir}/scripts/footprints.py add <url> --title <title> --description <desc> --content-type <type> --category-ids <ids> --tags <tags>` | Save a link or plain-text entry (url can be empty) |
| `python {baseDir}/scripts/footprints.py get <id>` | View a footprint's full details |
| `python {baseDir}/scripts/footprints.py search <query>` | Full-text search across title, description, AI summary |
| `python {baseDir}/scripts/footprints.py list [--category-id <id>] [--limit <n>] [--offset <n>]` | List recent footprints (limit max 100). Use `--offset` to page through results. Returns `total` count. |

### Organize

| Command | What it does |
|---------|-------------|
| `python {baseDir}/scripts/footprints.py update <id> --title <t> --description <d> --content-type <ct> --category-ids <ids> --tags <tags>` | Modify a footprint's title, categories, tags |
| `python {baseDir}/scripts/footprints.py batch-update <updates>` | Batch reorganize footprints (max 50 per call) |
| `python {baseDir}/scripts/footprints.py categories` | List all categories grouped by category set (set ID shown in headers) |
| `python {baseDir}/scripts/footprints.py create-category <name> [--category-set-id <id>]` | Create a new category |
| `python {baseDir}/scripts/footprints.py tags` | List all used tags |
| `python {baseDir}/scripts/footprints.py content-types` | List content types used in your library (e.g. article, video, image) |
| `python {baseDir}/scripts/footprints.py category-sets` | List all category sets (workspaces) |
| `python {baseDir}/scripts/footprints.py create-category-set <name>` | Create a new category set |

### Share

| Command | What it does |
|---------|-------------|
| `python {baseDir}/scripts/footprints.py create-shared-category <name> --mode cocreate\|subscribe --description <desc>` | Create a shared category |
| `python {baseDir}/scripts/footprints.py create-invite-link <sc_id> [--duration-hours 24]` | Generate an invite link |
| `python {baseDir}/scripts/footprints.py join-shared-category <invite_code>` | Join a shared category via invite code |
| `python {baseDir}/scripts/footprints.py add-to-shared <sc_id> --collection-id <id>` | Add a footprint to a shared category |
| `python {baseDir}/scripts/footprints.py remove-from-shared <sc_id> --collection-id <id>` | Remove a footprint from a shared category |
| `python {baseDir}/scripts/footprints.py copy <id> --category-ids <ids>` | Copy a shared footprint to your personal collection |

### Response Structure

`list` and `search` return `{"items": [...], "total": <N>}`. `total` is the full match count (not just this page). Always check `total` to know if there are more results beyond the current page.

`list` supports `--offset` for pagination. If `total > limit + offset`, there are more pages. Example: `total=156, limit=20, offset=0` → 8 pages total.

### Pagination Strategy

For large libraries, **prefer `search` over `list`** — it's faster and returns only what the user asked for. Use `list` for browsing or when the user says "show me everything." When paginating, tell the user: "Found 156 items, showing page 1/8. Want to see more?"

### Utilities

| Command | What it does |
|---------|-------------|
| `python {baseDir}/scripts/footprints.py me` | Confirm current identity |
| `python {baseDir}/scripts/footprints.py agent_magic_link` | Generate a magic link — send to user when done |
| `python {baseDir}/scripts/footprints.py agent_register` | Re-register / rotate credentials ⚠️ creates new account |

## Core Workflows

### New User — Zero Setup

```
1. Token check → auto-register (save to {baseDir}/.token)
2. python {baseDir}/scripts/footprints.py add "<url>" --title "<title>" → save bookmarks
3. python {baseDir}/scripts/footprints.py categories → discover structure
4. python {baseDir}/scripts/footprints.py create-category "<name>" → create categories
5. python {baseDir}/scripts/footprints.py update <id> --category-ids <ids> → categorize
6. python {baseDir}/scripts/footprints.py agent_magic_link → send link: "Done! View here → [link]"
```

### Returning User — Daily Use

```
1. python {baseDir}/scripts/footprints.py me → confirm identity
2. python {baseDir}/scripts/footprints.py categories + python {baseDir}/scripts/footprints.py tags → understand structure
3. python {baseDir}/scripts/footprints.py search query → find what's needed
4. python {baseDir}/scripts/footprints.py add / python {baseDir}/scripts/footprints.py update → operate
```

### Team Sharing

``` 
1. python {baseDir}/scripts/footprints.py create-shared-category "Team KB" --mode cocreate
2. python {baseDir}/scripts/footprints.py create-invite-link <sc_id> → share code with team
3. Teammates: python {baseDir}/scripts/footprints.py join-shared-category <invite_code>
4. Everyone: python {baseDir}/scripts/footprints.py add-to-shared <sc_id> --collection-id <collection_id> → build together
```

### Batch Reorganization

```
1. python {baseDir}/scripts/footprints.py list --limit 100 → get all bookmarks
2. python {baseDir}/scripts/footprints.py categories → map target categories
3. python {baseDir}/scripts/footprints.py batch-update '[
     {"id":"uuid1","category_ids":[1,3]},
     {"id":"uuid2","title":"New Title","category_ids":[2,5]}
   ]' → bulk edit (max 50 per call)
```

## Recipes

Concrete bash patterns for common tasks. Follow the numbered steps.

### Change a footprint's categories

```bash
python {baseDir}/scripts/footprints.py get 42
# → categories: [{id: 3, name: "Reading"}, {id: 5, name: "AI"}]

# Keep AI, drop Reading, add Tech (7)
python {baseDir}/scripts/footprints.py update 42 --category-ids 5,7
```

### Batch move to a new category

```bash
python {baseDir}/scripts/footprints.py create-category "New Topic"    # → returns new ID
python {baseDir}/scripts/footprints.py list --limit 100
# For each matching footprint:
python {baseDir}/scripts/footprints.py update <id> --category-ids <existing_ids>,<new_id>
```

### Merge two categories

```bash
python {baseDir}/scripts/footprints.py categories                      # note source and target IDs
python {baseDir}/scripts/footprints.py list --category-id <source_id>  # list all in source
# For each, replace source_id with target_id:
python {baseDir}/scripts/footprints.py update <id> --category-ids <target_id>,<other_ids>
# Tell user: empty category "source" is ready to delete via the web UI
```

### Auto-categorize by domain

User says "put all github.com links into a GitHub category":

```bash
python {baseDir}/scripts/footprints.py list --limit 200
# Filter in-memory: items where url contains "github.com"
python {baseDir}/scripts/footprints.py create-category "GitHub"
# For each match:
python {baseDir}/scripts/footprints.py update <id> --category-ids <existing_ids>,<github_id>
```

### Filter by tag and batch categorize

```bash
python {baseDir}/scripts/footprints.py search docker
# Filter results where tag_names includes "docker"
# For each, append target category:
python {baseDir}/scripts/footprints.py update <id> --category-ids <existing_ids>,<target_id>
```

### Organize uncategorized footprints

```bash
python {baseDir}/scripts/footprints.py list --limit 100
# Filter where category_ids is empty or only the default
# Present to user, let them pick categories
# Batch update selected items
```

### Recommend categories from tags

Spot gaps between tags and categories — e.g., #docker is common but no "Docker" category:

```bash
python {baseDir}/scripts/footprints.py tags        # most-used tags
python {baseDir}/scripts/footprints.py categories  # existing categories
# Cross-reference: tag without matching category → suggest creating one
```

### Copy from shared to personal

```bash
python {baseDir}/scripts/footprints.py categories  # find target personal category ID
python {baseDir}/scripts/footprints.py copy <footprint_id> --category-ids <personal_category_id>
```

### Cross-Agent collaboration

Two agents maintaining a shared knowledge base together:

```
1. Agent A: python {baseDir}/scripts/footprints.py create-shared-category "Team KB" --mode cocreate
2. Agent A: python {baseDir}/scripts/footprints.py create-invite-link <sc_id> → share code with user
3. User forwards code to colleague
4. Agent B: python {baseDir}/scripts/footprints.py join-shared-category <code>
5. Both agents now see each other's additions via python {baseDir}/scripts/footprints.py search
```

## Magic Link — The Delivery Loop

After organizing, always deliver results via magic link:

```bash
python {baseDir}/scripts/footprints.py agent_magic_link
```

Send the link to the user: "Done organizing — view your collection here → [link]"

User clicks to see a card-based interface with everything categorized. **Valid for 30 days, reusable.** If the user later binds a phone number, their agent-created account upgrades seamlessly.

## ⚠️ Critical Pitfalls

### category_ids is REPLACEMENT, not append

When updating, `--category-ids` sets the complete list — it does NOT add to existing categories.

```bash
# ❌ Wrong: moves bookmark to category 7, loses categories 3 and 5
python {baseDir}/scripts/footprints.py update 42 --category-ids 7

# ✅ Right: fetch current first, then merge
python {baseDir}/scripts/footprints.py get 42  # → existing: [3, 5]
python {baseDir}/scripts/footprints.py update 42 --category-ids 3,5,7
```

### Subscribe mode is READ-ONLY

Writing to a subscribe-mode shared category returns 403. Tell the user the collection is read-only — the creator must change it to cocreate mode.

### NEVER call agent_register twice

Each call creates a fresh empty account. Always check for a saved token first. If unsure, run `python {baseDir}/scripts/footprints.py me` to verify the current token is valid.

### Rate limiting

Frequent API calls trigger HTTP 429. Use `batch-update` for bulk operations, add delays between rapid calls, retry after a few seconds on 429.

### No member management via API

Inviting or removing members from shared categories requires the web UI at https://ai.ocean94.com. You cannot do this programmatically.

## Guidelines

### Always
- **Auto-register silently** — never interrupt the user for account setup
- **Inform before first use** — tell the user the skill connects to ai.ocean94.com, share links to [Terms](https://ai.ocean94.com/terms.html) and [Privacy](https://ai.ocean94.com/privacy.html)
- **Search before listing** — use `python {baseDir}/scripts/footprints.py search` for targeted queries instead of dumping everything
- **Discover before creating** — call `python {baseDir}/scripts/footprints.py categories` and `python {baseDir}/scripts/footprints.py tags` before adding to avoid duplicates
- **Deliver with magic link** — after organizing, always generate and share a link

### Confirm before
- Removing bookmark-category associations (irreversible)
- Clearing tags
- Modifying cocreate shared categories (affects others)
- Removing bookmarks from shared categories (other members lose access)
