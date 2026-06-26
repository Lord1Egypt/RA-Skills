---
name: smartlead
description: "Manage Smartlead campaigns, leads, and webhooks from the command line via the smartlead CLI."
metadata:
  {
    "openclaw":
      {
        "emoji": "📬",
        "requires": { "bins": ["smartlead"], "env": ["SMARTLEAD_API_KEY"] },
        "primaryEnv": "SMARTLEAD_API_KEY"
      }
  }
---

# Smartlead — CLI Usage Guide

Smartlead is the email outreach platform used by this workspace. Use `smartlead` CLI commands
to manage campaigns, leads, webhooks, and message history.

## Configuration

Credentials are resolved in order: `~/.config/smartlead-cli/config.toml` → env vars → CLI flags.

Required:
- `SMARTLEAD_API_KEY` — Smartlead API key

Optional:
- `SMARTLEAD_BASE_URL` — base URL (default `https://server.smartlead.ai/api/v1`)
- `SMARTLEAD_PRETTY` — set to `1` for rich table output

All commands output JSON by default. Add `--pretty` for human-readable tables (avoid in scripts).

## Command Discovery (Use This Instead of Memorizing Commands)

Do not guess command names or options. Use `--help` and follow the CLI surface:

```bash
smartlead --help
smartlead campaigns --help
smartlead campaigns leads --help
smartlead webhooks --help
smartlead <group> <command> --help
```

Prefer curated commands (`campaigns`, `leads`, `webhooks`) over `raw`. Use `raw` only when the
CLI does not expose the endpoint you need yet.

For `openclaw-smartlead` plugin setup, keep plugin config minimal unless there is a clear reason not to:
- usually set only `webhookSecret` (plugin ingress auth)
- plugin forwards normalized Smartlead payloads to OpenClaw `/hooks/smartlead` by default
- prompt text / delivery channel / branching logic should live in OpenClaw `hooks.mappings` (or a hook transform), not plugin config
- `openclawHookUrl` / `openclawHookToken` are typically auto-derived from OpenClaw hooks config

## Common Workflows

### Find campaign IDs
```bash
smartlead campaigns list
```

### Get full email thread for a lead (most important for reply alerts)
```bash
# When you have campaign_id and lead_id directly:
smartlead campaigns leads message-history <campaign_id> <lead_id>

# When you only have an email address:
smartlead leads get-by-email --email person@example.com   # → get id field
smartlead campaigns leads message-history <campaign_id> <resolved_lead_id>
```

### Inspect / patch a lead safely (preferred over full update)

`smartlead campaigns leads update` is a full update endpoint and Smartlead requires `email` in the
body. For partial edits, prefer `patch` because it auto-fetches the current lead, merges your
changes, and sends a valid full payload.

```bash
smartlead campaigns leads get <campaign_id> <lead_id>
smartlead campaigns leads patch <campaign_id> <lead_id> --first-name "Updated"
```

### Reply Alert Workflow (EMAIL_REPLY webhook event)

When an EMAIL_REPLY webhook fires through `openclaw-smartlead`, your OpenClaw hook mapping/transform
should construct the prompt. The forwarded payload includes flat fields like `campaign_id`,
`lead_id`, `lead_email`, `reply_category`, `preview_text`, `message_id`, `sequence_number`,
plus `payload` (sanitized raw Smartlead payload).

When responding to the hook prompt, always follow this sequence:

1. Extract `campaign_id` and `lead_id` from the prompt context.
   - `lead_id` comes from `sl_email_lead_id` (not `sl_email_lead_map_id`).
2. If `lead_id` is present: `smartlead campaigns leads message-history <campaign_id> <lead_id>`
3. If `lead_id` is missing but `lead_email` is present:
   `smartlead leads get-by-email --email <lead_email>` → then message-history.
4. Summarize the conversation (bullets or short paragraph).
5. Send a channel message starting with exactly **"New lead answer"**, including:
   - Lead email, campaign ID
   - One-line reply preview (from `preview_text`)
   - The conversation summary

### Set up a campaign webhook pointing at openclaw

```bash
# List current webhooks first
smartlead webhooks list <campaign_id>

# Create/update (id: null = create new)
smartlead webhooks upsert <campaign_id> --body-file webhook.json
```

Example `webhook.json`:

```json
{
  "id": null,
  "name": "OpenClaw Reply Alerts",
  "webhook_url": "https://<your-openclaw-host>/smartlead/webhook",
  "event_types": ["EMAIL_REPLY"],
  "categories": ["Interested"]
}
```

Use `smartlead webhooks upsert --help` for the current allowed `event_types`.
`categories` are Smartlead workspace lead-category labels (for example `Interested`), not webhook event types.

For OpenClaw side setup, prefer:
- plugin route `/smartlead/webhook` for Smartlead ingress/auth/dedupe
- OpenClaw `hooks.mappings` on `/hooks/smartlead` for prompt templates and branching
- optional hook transform for deterministic routing like positive/negative/OOO handling

## Webhook Payload Fields (EMAIL_REPLY)

Key fields available when an EMAIL_REPLY event arrives:

| Field | Description |
|---|---|
| `campaign_id` | Smartlead campaign ID |
| `sl_email_lead_id` | Lead ID (use this for message-history) |
| `sl_email_lead_map_id` | Lead-map ID (different from lead_id — do not confuse) |
| `sl_lead_email` | Original target lead email |
| `leadCorrespondence.targetLeadEmail` | More reliable target email field |
| `leadCorrespondence.replyReceivedFrom` | Actual email that replied (may differ from target) |
| `subject` | Email subject |
| `preview_text` | Reply preview snippet |
| `event_timestamp` | ISO timestamp of the reply |
| `secret_key` | Webhook validation secret (set in Smartlead) |

## Important Edge Cases / Pitfalls

| Mistake | Fix |
|---|---|
| Guessing CLI options | Use `smartlead ... --help` for the exact command shape |
| Using `smartlead campaigns list --limit ...` | `/campaigns` does not support `limit`; use `--offset`, `--client-id`, `--include-tags` |
| Using `sl_email_lead_map_id` as `lead_id` | Use `sl_email_lead_id` for `message-history` |
| Treating `replyReceivedFrom` as the target | `targetLeadEmail` is who was originally emailed |
| Using `campaigns leads update` without `email` | Smartlead rejects it; prefer `campaigns leads patch`, or include `email` in the full update body |
| Email lookups failing due to case mismatch | Normalize emails to lowercase before `get-by-email` / updates |
| Sending webhook `categories: []` | `categories` must be a non-empty list of Smartlead lead category labels |
| Assuming webhook `categories` is a global enum | Categories are workspace-specific labels (e.g. `Interested`); inspect Smartlead UI / Test Webhook |
| Running `--pretty` in automated scripts | Drop `--pretty`, parse JSON output |
| Starting alert without "New lead answer" | First line must be exactly `New lead answer` |
| Forgetting auth | Ensure `SMARTLEAD_API_KEY` is set in env or config |

## Deletion Behavior

Delete commands prompt for confirmation in interactive shells. In scripts/automation, pass `--yes`
to skip prompts.

Examples:

```bash
smartlead campaigns delete <campaign_id>
smartlead campaigns leads delete <campaign_id> <lead_id>
smartlead webhooks delete <campaign_id> --webhook-id <id>
```
