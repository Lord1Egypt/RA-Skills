---
name: "zoho-social-mcp"
description: "Zoho Social via MCP with action catalog, least-privilege profiles, portal/brand/channel helpers, media upload, and verified draft/schedule workflows. Use whenever a task involves Zoho Social: creating, validating, scheduling, or publishing posts, uploading or listing media library assets, or resolving portals, brands, and channels."
---

# Zoho Social MCP

Use Zoho Social through an MCP endpoint from `mcp.zoho.eu`. This skill is the canonical home for Social-specific MCP action documentation and least-privilege action profiles.

Source: [sprintberlin/openclaw-zoho-social-mcp-skill](https://github.com/sprintberlin/openclaw-zoho-social-mcp-skill)

## Requirements

- A Zoho Social MCP endpoint from `mcp.zoho.eu`
- `mcporter`
- Endpoint configuration via `ZOHO_SOCIAL_MCP_URL`, `--profile`, or `--mcp-url`
- For image bytes: this skill's `scripts/upload_media.py`. Keep [zoho-attachment-bridge](https://github.com/sprintberlin/zoho-attachment-bridge) linked; Social MCP currently takes JSON/base64 rather than a dropped `format: binary` parameter. See [Media uploads](#media-uploads).

Treat the endpoint as a credential. Never print it, commit it, or copy it into tickets, prompts, or chats.

## Improve during daily use

Daily use is the discovery loop. Treat every reusable defect, missing capability, safer check, or useful simplification as a contribution.

1. Search open issues immediately with native `gh`; link a match or create one.
2. Include the need, sanitized evidence, expected behavior, and acceptance criteria. Never include MCP URLs, tokens, customer names, or live IDs.
3. If implementation is feasible now: issue → branch → code/docs/tests → PR → CI → merge.
4. If implementation is not feasible now: file the issue before finishing and return its URL.
5. Do not add a GitHub wrapper script. Use native `git` and `gh`. See [CONTRIBUTING.md](CONTRIBUTING.md).

```bash
REPO=sprintberlin/openclaw-zoho-social-mcp-skill
gh issue list --repo "$REPO" --state open --search "<terms>"
gh issue create --repo "$REPO" --title "<title>" --body "<sanitized requirement and acceptance criteria>"
python3 -m unittest discover -s tests -v
```

## First setup

1. Create or open a Zoho Social connection at `mcp.zoho.eu`.
2. Select only the required Actions. Resolve the exact list from the JSON catalog:

```bash
python3 scripts/lookup_actions.py --profiles
python3 scripts/lookup_actions.py --profile social-viewer --names-only
python3 scripts/lookup_actions.py --profile social-creator --names-only
python3 scripts/lookup_actions.py --profile social-publisher --names-only
python3 scripts/lookup_actions.py --profile social-admin --names-only
python3 scripts/lookup_actions.py --task media-asset-management --names-only
```

3. Search the catalog when a profile or task lacks a required Action:

```bash
python3 scripts/lookup_actions.py --search "draft"
python3 scripts/lookup_actions.py --action uploadSocialMedia
```

4. Configure one default endpoint with `ZOHO_SOCIAL_MCP_URL`, or create named profiles using [references/MULTI_ACCOUNT.md](references/MULTI_ACCOUNT.md).
5. Inspect the selected live server before relying on an Action:

```bash
mcporter list "$ZOHO_SOCIAL_MCP_URL"
```

The catalog describes possible Actions. It does not prove that an Action is enabled on a particular MCP server. Runtime tool names usually have the `ZohoSocial_` prefix, while the Zoho MCP setup UI uses the Action name without that prefix.

Zoho currently documents 31 Social MCP tools. The catalog in this skill was seeded from a live listing on 2026-09-21.

## Endpoint selection

For one account, set `ZOHO_SOCIAL_MCP_URL`. For multiple accounts, pass `--profile NAME` to a bundled helper. Profiles live in `~/.config/zoho-mcp/profiles.json` by default and can resolve endpoints through an environment variable, a local URL file, or a direct URL. One-off `--mcp-url URL` overrides everything, but may expose the credential in shell history or process listings.

Resolution order is `--mcp-url`, selected profile, then the environment fallback. Profile selection is `--profile`, `ZOHO_SOCIAL_MCP_PROFILE`, then `ZOHO_MCP_PROFILE`. See [references/MULTI_ACCOUNT.md](references/MULTI_ACCOUNT.md).

## Safe workflow

1. Confirm the correct Zoho account. Never reuse an endpoint from another customer.
2. List portals with `getSocialPortals`. An empty list or `USER_INACTIVE_IN_PORTAL` means the authenticated user has no Social workspace access. Stop. Do not guess portal or brand IDs.
3. Resolve brand and channels with `getSocialBrands` and `getSocialChannels`. Never invent IDs.
4. Read before writing. Inspect a draft or schedule before updating it.
5. Call `validateSocialPost` with the exact post body before create/update/publish/schedule.
6. For writes, send only intended fields and read the affected post back immediately.
7. Keep `deleteSocialSchedule` disabled unless the task explicitly requires it.

## Media uploads

Zoho Social MCP can accept image bytes as a JSON string. The live `uploadSocialMedia` schema requires `body.file` (complete `data:image/png;base64,<COMPLETE_PAYLOAD>`) and `body.file_name`, plus headers `portal_id` and `brand_id`. Supported formats: PNG, GIF, JPEG, JPG.

Do not paste base64 into chat. Truncated base64 produces a corrupt library asset while the call can still report success.

```bash
python3 scripts/upload_media.py --portal-id <portal_id> --brand-id <brand_id> --file <path>
python3 scripts/upload_media.py --portal-id <portal_id> --brand-id <brand_id> --image-url https://example.com/hero.png
python3 scripts/list_media.py --portal-id <portal_id> --brand-id <brand_id>
```

The live upload ID arrives in `file_path`, not `id`. Treat empty `file_path` as failure even when `status` is `success`. Re-list the library before attaching the ID in `media_input`. Degenerate images (for example a 1x1 PNG) can return empty fields and never appear in the library.

[zoho-attachment-bridge](https://github.com/sprintberlin/zoho-attachment-bridge) remains required for Books, CRM, Projects, and WorkDrive, where MCP upload tools drop `format: binary` bytes. Social is different: a real PNG uploaded as a complete data URI lands in the media library. Keep the bridge linked, but do not route Social images through it unless a later live upload reports success with empty `file_path` and no library asset.

## Common calls

List portals:

```bash
cat > /tmp/social_portals.json <<'JSON'
{"headers": {}}
JSON
mcporter call "$ZOHO_SOCIAL_MCP_URL.ZohoSocial_getSocialPortals" --args "$(< /tmp/social_portals.json)"
```

List brands:

```bash
cat > /tmp/social_brands.json <<'JSON'
{"headers": {"portal_id": "PORTAL_ID"}}
JSON
mcporter call "$ZOHO_SOCIAL_MCP_URL.ZohoSocial_getSocialBrands" --args "$(< /tmp/social_brands.json)"
```

Use the schema shown by the live MCP server when it differs from these examples.

## Bundled scripts

The scripts resolve the endpoint via `--mcp-url`, `--profile` (`~/.config/zoho-mcp/profiles.json`), or `ZOHO_SOCIAL_MCP_URL`, call `mcporter` without shell expansion, paginate results, and normalize common Zoho MCP response envelopes.

```bash
python3 scripts/list_portals.py
python3 scripts/list_brands.py --portal-id PORTAL_ID --json
python3 scripts/list_channels.py --portal-id PORTAL_ID --brand-id BRAND_ID
python3 scripts/list_drafts.py --portal-id PORTAL_ID --brand-id BRAND_ID --limit 20
python3 scripts/list_schedules.py --portal-id PORTAL_ID --brand-id BRAND_ID
python3 scripts/list_published.py --portal-id PORTAL_ID --brand-id BRAND_ID --network linkedin
python3 scripts/inspect_post.py POST_ID --kind draft --portal-id PORTAL_ID --brand-id BRAND_ID
python3 scripts/list_media.py --portal-id PORTAL_ID --brand-id BRAND_ID
python3 scripts/upload_media.py --portal-id PORTAL_ID --brand-id BRAND_ID --file ./hero.png
```

Every helper accepts `--mcp-url`, `--profile`, `--profiles-file`, `--json`, and `--timeout`. Run any helper with `--help` without configuring credentials. Unknown or incomplete options exit with status 2.

## Role profiles

| Profile | Actions | Fits one MCP server |
|---|---|---|
| `social-viewer` | 16 | yes |
| `social-creator` | 23 | yes |
| `social-publisher` | 30 | yes |
| `social-admin` | 31 | yes |

Start with `social-viewer` for lookup. Use `social-creator` for drafts and media. Use `social-publisher` for scheduling and live publish. Keep `social-admin` for schedule deletion.

## References

- [Action catalog](references/actions.jsonl)
- [Profiles and task recipes](references/profiles.json)
- [Catalog format](references/CATALOG_FORMAT.md)
- [Action profiles overview](references/ACTION_PROFILES.md)
- [Common workflows](references/COMMON_WORKFLOWS.md)
- [Multi-account profiles](references/MULTI_ACCOUNT.md)
- [zoho-attachment-bridge](https://github.com/sprintberlin/zoho-attachment-bridge)

Query the catalog with `scripts/lookup_actions.py` instead of loading `actions.jsonl` into context.

## Troubleshooting and safety

- **No endpoint configured**: set `ZOHO_SOCIAL_MCP_URL`, use `--profile`, or pass `--mcp-url`; never print the value.
- **Empty portals / `USER_INACTIVE_IN_PORTAL`**: the authenticated user cannot see a Social workspace. Stop and report it. Do not switch customers.
- **Unknown portal or brand ID**: resolve through lookup tools; do not guess.
- **Upload reported success but empty `file_path`**: treat as failure. Re-list the library. File a GitHub issue with sanitized evidence.
- **OAuth scope error**: reconnect the affected MCP connection; never switch to another customer's endpoint.
- Zoho Social contains customer content and publishing credentials. Load only required records and never copy post text, media, or IDs into chats, logs, or repositories.
