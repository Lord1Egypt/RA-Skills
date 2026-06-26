---
name: todoist-orbit
description: "Operate Todoist through a Python CLI backed by the Todoist REST API. Use when the task requires deterministic Todoist automation instead of chatty natural-language parsing: listing, creating, updating, moving, completing, deleting, or resolving tasks; creating/updating/archiving/searching projects; creating/updating/archiving sections; listing/creating/updating/deleting/searching labels; uploading files and attaching them to task/project comments; or concurrent Todoist lookups. Prefer this skill when Todoist, projects, sections, labels, attachments, or task comments are involved."
metadata: { "openclaw": { "primaryEnv": "TODOIST_API_KEY", "requires": { "bins": ["python3"], "env": ["TODOIST_API_KEY"] } } }
---

# Todoist Orbit

Use the bundled Python CLI. It is async at the command layer and uses only Python stdlib HTTP primitives, so there is no SDK dependency to install.

## Prerequisites

Set `TODOIST_API_KEY` in the environment.

## Find the installed skill path first

ClawHub installs skills under an OpenClaw skills directory such as `~/.openclaw/skills/todoist-orbit/`, but do not assume the exact path blindly. Verify the installed location first if needed, then run the script from there.

```bash
SKILL_DIR="$HOME/.openclaw/skills/todoist-orbit"
[ -f "$SKILL_DIR/scripts/todoist_orbit.py" ] || echo "Verify the installed path for todoist-orbit before running commands"
```

## Primary command

```bash
python3 "$SKILL_DIR/scripts/todoist_orbit.py" --pretty <group> <action> ...
```

If you are running from a checked-out repo instead of an installed skill, adjust `SKILL_DIR` accordingly.

## Common commands

### Tasks

```bash
python3 "$SKILL_DIR/scripts/todoist_orbit.py" --pretty tasks list --filter "today"
python3 "$SKILL_DIR/scripts/todoist_orbit.py" --pretty tasks add "Ship release" --project-id <project_id> --section-id <section_id> --due "tomorrow" --priority 1
python3 "$SKILL_DIR/scripts/todoist_orbit.py" --pretty tasks update <task_id> --content "Ship release v2" --due "next monday"
python3 "$SKILL_DIR/scripts/todoist_orbit.py" --pretty tasks move <task_id> --project-id <project_id> --section-id <section_id>
python3 "$SKILL_DIR/scripts/todoist_orbit.py" --pretty tasks close <task_id>
```

Keep `tasks add ... "content"` and `--description` short. Use them for the task title and a brief summary only. If you need multi-line notes, logs, checklists, transcripts, or structured updates, put that material in comments instead of stretching task fields.

### Projects

```bash
python3 "$SKILL_DIR/scripts/todoist_orbit.py" --pretty projects list
python3 "$SKILL_DIR/scripts/todoist_orbit.py" --pretty projects search "client"
python3 "$SKILL_DIR/scripts/todoist_orbit.py" --pretty projects add "Client Ops" --view-style board --favorite
python3 "$SKILL_DIR/scripts/todoist_orbit.py" --pretty projects archive <project_id>
```

`projects search` now calls Todoist's server-side `GET /api/v1/projects/search` endpoint. Keep `--exact` when you want an exact-name match on top of the API-backed search results.

### Sections

```bash
python3 "$SKILL_DIR/scripts/todoist_orbit.py" --pretty sections list --project-id <project_id>
python3 "$SKILL_DIR/scripts/todoist_orbit.py" --pretty sections add <project_id> "Inbox"
python3 "$SKILL_DIR/scripts/todoist_orbit.py" --pretty sections move <section_id> <project_id>
```

`sections move` is preserved for CLI compatibility, but Todoist REST does not provide a section move endpoint, so the command exits with a documented error instead of attempting a move.

### Labels

```bash
python3 "$SKILL_DIR/scripts/todoist_orbit.py" --pretty labels list
python3 "$SKILL_DIR/scripts/todoist_orbit.py" --pretty labels search "waiting"
python3 "$SKILL_DIR/scripts/todoist_orbit.py" --pretty labels add "waiting-for" --color berry_red --favorite
python3 "$SKILL_DIR/scripts/todoist_orbit.py" --pretty labels update <label_id> --name "waiting-on" --color blue
python3 "$SKILL_DIR/scripts/todoist_orbit.py" --pretty labels get <label_id>
python3 "$SKILL_DIR/scripts/todoist_orbit.py" --pretty labels delete <label_id>
```

`labels search` now calls Todoist's server-side `GET /api/v1/labels/search` endpoint. Keep `--exact` when you want an exact-name match on top of the API-backed search results.

### Attachments and comments

Upload the file first or let `comments add` do it implicitly.

```bash
python3 "$SKILL_DIR/scripts/todoist_orbit.py" --pretty uploads add ./voice-note.m4a
python3 "$SKILL_DIR/scripts/todoist_orbit.py" --pretty comments add --task-id <task_id> "Voice memo attached" --attachment ./voice-note.m4a
python3 "$SKILL_DIR/scripts/todoist_orbit.py" --pretty comments add-file --task-id <task_id> ./daily-log.txt
python3 "$SKILL_DIR/scripts/todoist_orbit.py" --pretty comments add-stdin --task-id <task_id> <<'EOF'
Daily log
- investigated API regression
- deployed rollback
- monitoring error budget
EOF
```

Todoist stores attachments on comments, not directly on the task object. For task attachments, add a task comment with `--attachment`.

Formatting and safety guidance:
- Todoist comments are plain text. Treat Markdown rendering, indentation, and pasted shell snippets as best-effort rather than rich formatting.
- For anything longer than a short sentence, prefer `comments add-file` or `comments add-stdin` over inline shell arguments.
- Avoid shell interpolation for comment bodies. Commands like `comments add --task-id ... "$NOTE"` are fragile and can introduce accidental characters such as a stray leading `$`.
- Use `add-file` for saved notes and `add-stdin` for here-docs or generated output. Both routes preserve multi-line text without shell-quoting games.

### Concurrent resolution

```bash
python3 "$SKILL_DIR/scripts/todoist_orbit.py" --pretty resolve --project "Work" --section "Inbox" --task-filter "today"
```

Use `resolve` when you want project and section lookups plus a task query in one call.

## Operational notes

- Prefer IDs once resolved; names are ambiguous.
- The CLI is REST-only; there is no Sync API fallback.
- `projects search` and `labels search` use Todoist's `GET /api/v1/projects/search` and `GET /api/v1/labels/search` endpoints. `--exact` remains as a compatibility flag that narrows the API results to an exact name match.
- `sections move` is intentionally unsupported because Todoist REST does not expose a section move operation. The command remains available only to fail clearly for callers that already invoke it.
- `comments add --attachment` uploads the file and passes the returned attachment object into the comment create request.
- Prefer short task fields and long comments: task content/description are easier to scan when they stay concise, while comments work better for running logs and multi-line notes.
- Read `references/api-notes.md` only when you need endpoint-specific details or attachment behavior.
