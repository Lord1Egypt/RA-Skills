# Action Catalog Format

This document describes how MCP Action knowledge is stored in this skill. The same layout is used by the other Zoho MCP skills, so an agent learns the structure once and can then answer "which Actions do I need for this task".

## Problem

A Zoho MCP app exposes a set of Actions. Zoho Social currently documents 31 tools as the complete MCP surface. Written as prose Markdown, that catalog still has three defects:

1. An agent must load long descriptions into context to answer a small question.
2. Hand-written profile lists drift away from the real catalog.
3. Zoho adds, renames, and removes Actions, and a prose file makes that invisible in review.

## Design

JSON is the only source of truth. There is no generated or hand-maintained Markdown catalog.

| File | Purpose |
|---|---|
| `references/actions.jsonl` | Every known Action, one JSON object per line |
| `references/profiles.json` | Role profiles and task recipes, referencing Action keys |
| `scripts/import_actions.py` | Rebuilds `actions.jsonl` from a Zoho MCP setup UI dump |
| `scripts/lookup_actions.py` | Answers profile, task, and search questions without loading the full catalog |

### Why JSONL for the catalog

One Action per line keeps Git diffs readable. When Zoho changes the catalog, review shows exactly which lines were added, changed, or marked removed.

### Action record

```json
{"key":"getSocialPortals","name":"getSocialPortals","summary":"Fetches social portals...","description":"Full text as delivered by the live MCP tool.","added":"2026-09-21"}
```

- `key`: unique identifier used by profiles and tasks. Equal to `name` except for grouped Actions.
- `name`: the Action name shown in the Zoho MCP setup UI and, without the `ZohoSocial_` prefix, on the live server.
- `summary`: shortened first line for fast scanning.
- `description`: the untouched description text delivered by Zoho.
- `added`: date the Action first appeared in the catalog.
- `removed`: set when an Action disappears from a newer dump.

This catalog was seeded from a live `mcporter list --json` of a Zoho Social MCP server on 2026-09-21. Zoho's public Social MCP page also states 31 tools. Refresh from a setup-UI dump or a new live listing if Zoho expands the surface.

## Usage

```bash
python3 scripts/lookup_actions.py --profiles
python3 scripts/lookup_actions.py --profile social-viewer --names-only
python3 scripts/lookup_actions.py --task media-asset-management --names-only
python3 scripts/lookup_actions.py --search "draft"
python3 scripts/lookup_actions.py --action uploadSocialMedia
python3 scripts/lookup_actions.py --validate
```

## Maintaining the catalog

1. Open the Zoho MCP setup UI for Zoho Social and copy the complete Action list into a text file, or export a live `mcporter list --json`.
2. Rebuild from a UI dump:

   ```bash
   python3 scripts/import_actions.py /tmp/social_actions_dump.txt --dry-run
   python3 scripts/import_actions.py /tmp/social_actions_dump.txt
   ```

3. Validate that profiles and tasks still reference existing Actions:

   ```bash
   python3 scripts/lookup_actions.py --validate
   ```

4. Fix any profile or task entry the validation rejects, then commit.

The catalog describes Actions that can exist for the app. It does not prove that an Action is enabled on a specific MCP server. Always confirm against the live server:

```bash
mcporter list "$ZOHO_SOCIAL_MCP_URL"
```

Runtime tool names carry the `ZohoSocial_` prefix; the catalog and the setup UI use the bare Action name.
