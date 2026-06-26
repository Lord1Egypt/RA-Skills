---
name: risha-content-generator
description: Discover, prepare, and execute any Risha.ai capability available to the authenticated account. Use when Codex needs to authenticate to a Risha workspace, load a ready-to-use catalog of accessible capabilities, inspect manual field definitions, inspect creator, dialect, or voice choices, submit capability requests, poll async jobs, or fetch generated text, audio, image, video, or multimodal outputs from Risha.
---

# Risha Content Generator

Use this skill to drive Risha's capability workflow from discovery through final output retrieval. Prefer the bundled helper script for repeated API work so the request flow stays consistent and the payload shape remains inspectable.

## Workflow

1. Gather credentials and decide the auth mode.
2. Load the bundled capability catalog or refresh it from the live account.
3. Inspect the chosen capability's manual fields to build valid `prompt_data`.
4. Optionally inspect creator choices for creator-backed text workflows.
5. Estimate credits before submitting.
6. Submit a generation request and poll until it finishes.
7. Return the final generated content or explain the failure clearly.

## Choose Auth Mode

Prefer one of these auth approaches:

- `RISHA_AUTH_HEADER` when the caller already has a working header such as `Bearer ...` or `Basic ...`.
- `RISHA_EMAIL` and `RISHA_PASSWORD` when the skill can log in directly through `/api/auth/login/`.

Set `RISHA_API_BASE_URL` only if the host changes. The default is `https://adminxcore-api.risha.ai/api`.

Before doing generation work, validate auth with the helper:

```bash
python3 scripts/risha_api.py me
```

If login succeeds but the script cannot derive a reusable auth token/header from the response, stop guessing and ask the user for the exact header format that works in their environment.

## Load The Capability Catalog First

Never hardcode `prompt_data` blindly. The valid keys come from each capability's linked manual definition.

This skill now ships with a current account snapshot:

- [references/current-capabilities.md](references/current-capabilities.md)
- [references/current-capabilities.json](references/current-capabilities.json)

Refresh that snapshot in one step when needed:

```bash
python3 scripts/risha_api.py catalog \
  --quiet \
  --write-json references/current-capabilities.json \
  --write-markdown references/current-capabilities.md
```

Use the catalog for:

- capability IDs
- category and output type
- async vs sync behavior
- required inputs
- field choice sources
- current input and output schemas

When you need one capability in full detail, inspect it directly:

```bash
python3 scripts/risha_api.py capability 123
```

Use the capability manual to inspect:

- `manual.fields`
- each field's `field_path`
- `json_type`
- `is_required`
- `choice_model`
- `enum_values`
- credit rules when present

Build `prompt_data` from those manual fields. Use the field path exactly as Risha expects. For nested paths such as `input.text`, create nested JSON objects.

The current account snapshot includes 17 accessible capabilities across:

- `multimodal`
- `text_generation`
- `tts`

Treat the snapshot as the fast path and the live `catalog` command as the refresh path.

## Inspect Creator Choices When Needed

For creator-backed writing flows, inspect available creators before choosing one:

```bash
python3 scripts/risha_api.py creators
```

If the relevant manual field uses `choice_model: creators`, pass the creator's `field_value`, not just its label.

Use the same pattern for dialects and voices when the manual points to those choice models.

## Generate Content

The helper now includes credit preview by default. Before every `generate` request, it fetches:

- current available credits
- estimated cost for the selected capability and `prompt_data`
- projected remaining credits after submission

If you want the preview without creating anything, use:

```bash
python3 scripts/risha_api.py estimate \
  --capability-id 123 \
  --prompt-data-file /absolute/path/prompt-data.json
```

Pass either inline JSON or a JSON file:

```bash
python3 scripts/risha_api.py generate \
  --capability-id 123 \
  --title "LinkedIn post draft" \
  --prompt-data '{"input":{"topic":"AI adoption","tone":"confident"}}'
```

Or:

```bash
python3 scripts/risha_api.py generate \
  --capability-id 123 \
  --prompt-data-file /absolute/path/prompt-data.json \
  --wait
```

Use `--wait` to poll until the request reaches a terminal state. Terminal states are:

- `completed`
- `failed`
- `cancelled`

When completed, prefer returning:

- `generated_content.content` for text
- `generated_content.asset` or `thumbnail` URLs for media
- `generated_content.content_metadata` when it contains useful structured extras

The `generate` response now includes a `credit_preview` block alongside the request or final generation result.

## Chat Endpoint

Risha also exposes `/api/chat/` and `/api/chat/stream/`, but the schema does not currently describe their request bodies. Treat those endpoints as exploratory only unless the user provides working payload examples. Prefer the capability plus generation-request flow for reliable automation.

## Troubleshooting

- If `/auth/login/` returns `400` with `Invalid email or password`, confirm credentials before retrying.
- If a generation request fails, inspect `error_message` on the request record.
- If a capability detail lacks enough manual information, read [references/risha-api.md](references/risha-api.md) and inspect the live capability JSON with the helper before constructing payloads.
- If the API host returns intermittent `502 Bad Gateway`, retry with backoff instead of rewriting the workflow.

## Resources

- Use [scripts/risha_api.py](scripts/risha_api.py) for authenticated API calls, capability inspection, catalog refresh, and generation polling.
- Use [references/risha-api.md](references/risha-api.md) for the endpoint map, auth notes, and payload-building rules derived from the published schema at `https://adminxcore-api.risha.ai/api/docs/?format=openapi`.
- Use [references/current-capabilities.md](references/current-capabilities.md) as the ready-to-browse capability inventory.
- Use [references/current-capabilities.json](references/current-capabilities.json) when exact field names and schemas are needed without another API round-trip.
