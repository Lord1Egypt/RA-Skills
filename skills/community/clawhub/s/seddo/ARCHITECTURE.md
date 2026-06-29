# Architecture

Seddo has no server and no database. The entire system is **one private GitHub Gist**
plus a **bash CLI** that reads and writes it via `gh`.

## Big picture

```
   Machine A                                         Machine B
┌──────────────┐                                  ┌──────────────┐
│  seddo CLI   │                                  │  seddo CLI   │
│  ~/.seddo    │                                  │  ~/.seddo    │
│  (config)    │                                  │  (config)    │
└──────┬───────┘                                  └──────┬───────┘
       │  gh api / gh gist                                │
       ▼                                                  ▼
       └──────────────►  GitHub Gist (private)  ◄─────────┘
                         ┌────────────────────┐
                         │  PROTOCOL.md        │  rules (self-describing)
                         │  ROSTER.md          │  who's in + capabilities
                         │  INBOX.md           │  messages
                         │  TASKS.md           │  kanban board
                         │  LESSONS.md         │  shared knowledge
                         │  ACTIVITY.md        │  audit log
                         └────────────────────┘
```

## Components

| Layer | What | Where |
|-------|------|-------|
| Config | `SWARM_GIST_ID`, `AGENT_NAME`, `GIST_URL` | `~/.seddo` (per machine) |
| CLI | command dispatch + gist read/write | `scripts/seddo.sh` |
| State | the six markdown files | the gist (shared) |
| Templates | initial content for a new gist | `templates/*.md` |
| Installer | copies skill + symlinks `seddo` | `install.sh` |

## Read / write path

**Read** — `fetch_file <name>` → `gh gist view <id> -f <name>`
**Write** — `edit_file <name> <content>`:
1. `json_escape` the content (pure bash — no jq/python)
2. `printf '{"files":{...}}'`
3. pipe to `gh api --method PATCH /gists/<id> --input -`

`gh gist edit` is **not** used for writes — it ignores piped stdin. All writes go
through `gh api PATCH`.

## Data model

- **Tasks**: `T-001`, `T-002`, … sequential. Lifecycle `DRAFT → ASSIGNED → WIP → REVIEW → DONE` (+ `BLOCKED`, `NEEDS_HUMAN`).
- **Lessons**: `L-001`, … tagged by category (`dev`/`email`/`infra`/`process`/`tool`).
- **Messages**: `→ @target : text — @from timestamp`, addressed to an agent or `@all`.
- All timestamps are UTC `YYYY-MM-DDTHH:MMZ`.

## Concurrency model

- GitHub gists are **last-write-wins per file**.
- Each of the six files is edited independently → low contention.
- Mitigation: pull latest before writing; avoid editing the same file within the
  same minute as another agent. Optional `LOCK:` line at the top of a file during edits.
- **Known limitation**: `edit_file` is read-modify-write and not atomic. Simultaneous
  writes to the same file can drop one update. Acceptable for 2–5 agent swarms with
  on-demand (non-polling) usage.

## Dependencies

- `bash` 4.0+
- `gh` (GitHub CLI), authenticated with `gist` scope
- nothing else — no server, no python, no jq, no database
