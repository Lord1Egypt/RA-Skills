---
name: raindrop-io-bookmark-manager
description: Raindrop.io bookmark and collection manager for a local OpenClaw workspace. Use when the user wants to validate Raindrop auth, inspect their account, list or search bookmark collections, create/update/delete collections, save or edit bookmarks, bulk import/export bookmark links, or run local Raindrop.io OAuth flows without exposing secrets inside the published skill.
---

# Raindrop.io Bookmark Manager

Use the official Raindrop.io API through a local CLI that prefers user environment variables and can optionally read a local `.env` file outside the skill folder.

## Secret storage

Store real credentials outside the skill folder.

Preferred approach:
- store `RAINDROP_CLIENT_ID`, `RAINDROP_CLIENT_SECRET`, `RAINDROP_ACCESS_TOKEN`, and optional `RAINDROP_REFRESH_TOKEN` as user environment variables

Optional fallback:
- set `RAINDROP_ENV_FILE` to point at a local env file if you explicitly want file-based storage

Rules:
- never hardcode real client ids, secrets, access tokens, or refresh tokens into the skill
- never publish real credential values in `SKILL.md`, `references/`, or `scripts/`
- prefer environment variables over passing secrets on the command line, because shell history may retain CLI arguments

The skill does **not** need secrets embedded inside the published skill folder.

Example env file shape is documented in:
- `references/env-example.md`

## Quick start

Validate auth:

```powershell
python .\skills\raindrop-io-bookmark-manager\scripts\raindrop_manager.py whoami
```

Start OAuth without auto-opening the browser:

```powershell
python .\skills\raindrop-io-bookmark-manager\scripts\raindrop_manager.py auth-start --no-browser
```

Finish OAuth with the returned code:

```powershell
python .\skills\raindrop-io-bookmark-manager\scripts\raindrop_manager.py auth-finish --code "PASTE_CODE_HERE"
```

Refresh an OAuth token:

```powershell
python .\skills\raindrop-io-bookmark-manager\scripts\raindrop_manager.py refresh-token
```

List top-level collections:

```powershell
python .\skills\raindrop-io-bookmark-manager\scripts\raindrop_manager.py collections
```

List nested collections:

```powershell
python .\skills\raindrop-io-bookmark-manager\scripts\raindrop_manager.py collections --children
```

List bookmarks in a collection:

```powershell
python .\skills\raindrop-io-bookmark-manager\scripts\raindrop_manager.py bookmarks 0 --perpage 20
```

Search bookmarks inside a collection:

```powershell
python .\skills\raindrop-io-bookmark-manager\scripts\raindrop_manager.py bookmarks 0 --search "etsy" --perpage 20
```

Create a collection:

```powershell
python .\skills\raindrop-io-bookmark-manager\scripts\raindrop_manager.py create-collection --title "Research" --view list
```

Save one bookmark:

```powershell
python .\skills\raindrop-io-bookmark-manager\scripts\raindrop_manager.py add-bookmark --collection-id 123456 --link "https://example.com" --title "Example"
```

Export bookmark links:

```powershell
python .\skills\raindrop-io-bookmark-manager\scripts\raindrop_manager.py export-bookmarks 123456 --format csv --output ".\output\raindrop-export.csv"
```

Import bookmarks from a txt list:

```powershell
python .\skills\raindrop-io-bookmark-manager\scripts\raindrop_manager.py import-bookmarks --input ".\input\urls.txt" --collection-id 123456 --output ".\output\results.json"
```

## Workflow

1. Put Raindrop credentials in environment variables or a local env file.
2. Use either a test token or the built-in OAuth flow.
3. Run `whoami` first when verifying a new setup.
4. Use `collections` to discover target collection ids.
5. Use `bookmarks` and `--search` to inspect existing saved links.
6. Use `create-collection`, `update-collection`, and `delete-collection` for organization.
7. Use `add-bookmark`, `update-bookmark`, and `delete-bookmark` for individual saved links.
8. Use `import-bookmarks` and `export-bookmarks` for batch workflows.

## Commands

- `whoami` — verify auth and inspect account info
- `auth-start [--no-browser]` — generate the OAuth authorize URL
- `auth-finish --code CODE` — exchange an OAuth code for tokens and save them locally
- `refresh-token` — refresh OAuth tokens and save them locally
- `collections [--children]` — list root or nested collections
- `collection-get <id>` — inspect one collection
- `create-collection --title NAME` — create a collection
- `update-collection <id> ...` — update a collection
- `delete-collection <id>` — delete a collection
- `bookmarks <collectionId> [--search TEXT]` — list/search bookmarks in a collection
- `bookmark-get <id>` — inspect one bookmark
- `add-bookmark --collection-id ID --link URL` — save a bookmark
- `update-bookmark <id> ...` — edit a bookmark
- `delete-bookmark <id>` — delete a bookmark
- `export-bookmarks <collectionId> --format json|txt|csv --output file` — export bookmarks
- `import-bookmarks --input file --collection-id ID` — import bookmarks from txt or json
- `env-template` — print or write a local env template

List/export commands support extra filters like:
- `--tag`
- `--domain`
- `--contains`

Many commands also support `--csv` for flatter stdout output.

## OAuth / callback note

For a local desktop-style setup, use:
- `http://127.0.0.1:8765/callback`

Optionally also add:
- `http://localhost:8765/callback`

For local-only automation, a Raindrop **test token** is often enough and simpler than interactive OAuth.

## Resources

### scripts/
- `raindrop_manager.py` — local Raindrop.io CLI for auth, collections, bookmarks, import, and export

### references/
- `api-notes.md` — endpoint notes and field reminders
- `env-example.md` — non-secret example of the local env file shape
