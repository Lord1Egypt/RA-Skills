# Zoho Social MCP Action Profiles & Task Recipes

The machine-readable source of truth is [`references/profiles.json`](profiles.json), validated against [`references/actions.jsonl`](actions.jsonl). Use `scripts/lookup_actions.py` for copy-ready lists.

## The 300-Action Server Limit

A Zoho MCP server accepts at most 300 selected Actions per connection. Zoho Social currently exposes 31 tools, so every profile fits on one server. Use the smallest matching profile anyway so the session tool catalog stays small.

| Profile | Actions | Fits one MCP server |
|---|---|---|
| `social-viewer` | 16 | yes |
| `social-creator` (inherits `social-viewer`) | 23 | yes |
| `social-publisher` (inherits `social-creator`) | 30 | yes |
| `social-admin` (inherits `social-publisher`) | 31 | yes |

## Role Profiles

```bash
python3 scripts/lookup_actions.py --profiles
python3 scripts/lookup_actions.py --profile social-viewer --names-only
python3 scripts/lookup_actions.py --profile social-creator --names-only
python3 scripts/lookup_actions.py --profile social-publisher --names-only
python3 scripts/lookup_actions.py --profile social-admin --names-only
```

### 1. Social Viewer (`social-viewer`) - 16 Actions

Read-only inspection: portals, brands, channels, users, network properties, drafts, schedules, published posts, media library, mentions, geolocations, Pinterest boards, post activities, and counts. No create, upload, publish, or delete Actions.

### 2. Social Creator (`social-creator`) - 23 Actions resolved

Inherits `social-viewer` and adds draft creation and updates, post validation, media uploads, Pinterest board creation, and activity comments. No immediate publishing and no schedule create/update/delete.

### 3. Social Publisher (`social-publisher`) - 30 Actions resolved

Inherits `social-creator` and adds schedule create/update, immediate publish, approval status changes, draft/schedule listing, and draft deletion. Schedule deletion stays denied.

### 4. Social Administrator (`social-admin`) - 31 Actions resolved

Inherits `social-publisher` and adds `deleteSocialSchedule`. This is the full documented Zoho Social MCP surface.

## Task Recipes

```bash
python3 scripts/lookup_actions.py --tasks
python3 scripts/lookup_actions.py --task media-asset-management --names-only
```

- `post-drafting`: portals, brands, channels, validate, create/update/get draft
- `publishing-and-scheduling`: validate, schedule, update schedule, publish, publish status
- `media-asset-management`: upload local or URL media, list library
- `social-monitoring`: published posts, post detail, activities, counts
