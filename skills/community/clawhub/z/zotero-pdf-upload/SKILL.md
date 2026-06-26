---
name: zotero-pdf-upload
description: Upload PDFs and manage items in a Zotero Web Library. Supports both personal and group libraries. Use when a user wants to add papers/PDFs to Zotero, organize collections, or manage their Zotero library through the API.
primaryEnv: ZOTERO_API_KEY
requiredConfig: config.json
---
# zotero-pdf-upload

Use this skill for direct Zotero workflows that must stay safe, explicit, and reusable.

## First-time setup check (do this BEFORE any Zotero operation)

Before running any command, check if `config.json` exists in the skill root directory.

**If `config.json` does NOT exist**, stop and inform the user:

> This skill is not configured yet. You need to set it up first.
>
> **What you need to prepare:**
>
> 1. **Zotero API Key** — Create one at [zotero.org/settings/keys](https://www.zotero.org/settings/keys)
>    - Go to Settings → Security → Create new private key
>    - Enable: Allow library access, Allow notes access, Allow write access
>    - If using group libraries, set Default Group Permissions to Read/Write
>    - Click "Save Key" and copy the generated key
>
> 2. **Zotero Library URL** — Open your library in a browser and copy the URL:
>    - Personal: `https://www.zotero.org/<your-username>/library`
>    - Group: `https://www.zotero.org/groups/<group-id>/<group-name>/library`
>
> **Run this one-line setup command** from the skill directory:
> ```bash
> python scripts/setup.py "<YOUR_LIBRARY_URL>" "<YOUR_API_KEY>"
> ```

Do NOT proceed with any Zotero operations until `config.json` has been created.

## Included resources

- `scripts/zotero_workflow.py`: CLI entrypoint for parse/inspect/match/create operations.
- `scripts/zotero_client.py`: Zotero API client, URL parser, secret loading, collection matching, item creation, PDF upload.
- `tests/smoke_test_zotero_pdf_upload.py`: no-network smoke tests.
- `references/config.example.json`: runtime config template (uses unified `url` field for both group and personal URLs).
- `references/item.example.json`: item metadata sample.
- `references/approval-flow.md`: approval checkpoints and write safety policy.

## Required operating policy

1. Start with read-only steps (`parse-url`, `list-collections`, `choose-collection`).
2. If collection matching is weak or missing, return `pending-new-collection-approval`.
3. Create collections only via explicit action (`create-collection --approve-create`).
4. Create items only via explicit action (`create-item --approve-write`).
5. Only upload PDF if explicitly requested and config allows it.

## Secret handling

Load Zotero API key in this order (safe default):

1. Environment variable: `zotero.apiKeyEnv` (default `ZOTERO_API_KEY`)
2. Secret file path: `zotero.apiKeyPath`
3. Inline config value: `zotero.apiKey` (least preferred)

Never print full API keys in output.

Security note: when resolving a personal library URL (username-based, no numeric ID),
the skill calls `GET https://api.zotero.org/keys/{apiKey}` to look up the userID.
This is the standard Zotero API pattern — the key appears in the URL and may be
visible in server access logs. Use a least-privilege key and prefer env/file loading
over inline config.

## Core commands

Run from skill directory.

### 1) Parse a Zotero URL

```bash
python scripts/zotero_workflow.py parse-url --url "https://www.zotero.org/groups/6320165/my-group/library"
```

Personal library URL:

```bash
python scripts/zotero_workflow.py parse-url --url "https://www.zotero.org/myusername/library"
```

### 2) List collections (read-only)

```bash
python scripts/zotero_workflow.py list-collections --config ./tmp.config.json
```

Optional matching context:

```bash
python scripts/zotero_workflow.py list-collections \
  --config ./tmp.config.json \
  --title "Practical Alignment Evaluation for LLM Agents" \
  --tags alignment llm
```

### 3) Choose collection (read-only, no auto-create)

```bash
python scripts/zotero_workflow.py choose-collection \
  --config ./tmp.config.json \
  --item-json references/item.example.json
```

- If matched: status `matched-existing-collection`.
- If not matched: status `pending-new-collection-approval` + suggested name.

### 4) Explicitly create collection (write)

```bash
python scripts/zotero_workflow.py create-collection \
  --config ./tmp.config.json \
  --name "LLM Safety" \
  --approve-create
```

### 5) Explicitly create item metadata (write)

```bash
python scripts/zotero_workflow.py create-item \
  --config ./tmp.config.json \
  --item-json references/item.example.json \
  --auto-match-collection \
  --approve-write
```

Optional PDF attachment:

```bash
python scripts/zotero_workflow.py create-item \
  --config ./tmp.config.json \
  --item-json references/item.example.json \
  --collection-key ABCD1234 \
  --attach-pdf /path/to/paper.pdf \
  --approve-write
```

## Approval points to enforce

- Never call write subcommands without explicit human confirmation.
- Do not auto-create missing collections during matching.
- If matching confidence is weak, stop and ask whether to create/select a collection.
- Treat attachment upload failure as reportable; do not silently ignore.

## Smoke test

```bash
python tests/smoke_test_zotero_pdf_upload.py
```
