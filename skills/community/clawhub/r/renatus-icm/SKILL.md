---
name: renatus-icm
description: Manage Renatus event marketing campaigns as an ICM. Use when running event registration campaigns, sending commercial email blasts, setting up event landing pages, exporting leads from Supabase, syncing unsubscribes to Renatus, or performing browser-based guest registration via CDP. Requires: Renatus credentials, Supabase project, SMTP sender account. Trigger phrases: "run a Renatus event campaign", "send Renatus email campaign", "register a guest for Renatus", "download Renatus leads", "set up event landing page".
---

## ⚠️ Credentials & Security

**Required environment variables** (declare these before running any script):

| Variable | Purpose | Minimum Scope |
|---|---|---|
| `RENATUS_USERNAME` | Renatus back office login | ICM-level account |
| `RENATUS_PASSWORD` | Renatus back office login | ICM-level account |
| `SUPABASE_URL` | Supabase project URL | Read leads |
| `LEAD_ADMIN_TOKEN` | Supabase admin export | `anon` key or limited service role |
| `SENDER_EMAIL` | From address for campaigns | Send-only SMTP account |
| `SENDER_PASSWORD` | SMTP auth for email | Send-only |
| `SUPABASE_SERVICE_ROLE_KEY` | Supabase admin actions (destructive) | Service role — do not use for read-only ops |

**Security recommendations:**
- Use a dedicated Supabase project for testing — do not supply your production `service_role_key`
- Create a least-privilege Supabase anon key scoped to `funnel_leads` table reads only
- Use a separate Chrome/Brave **profile** for CDP access (not your main browser session)
- `renatus_delete_lead.py` performs deletions — always run with `--dry-run` first
- Rotate credentials after use; revoke tokens that were shared or exposed
- Do not commit real credentials to `config.json` — use the `.example` file and environment variables

**CDP access:** Scripts connect to `http://127.0.0.1:9222` to inspect your browser's localStorage/cookies for Renatus auth tokens. This requires Chrome/Brave launched with `--remote-debugging-port=9222`. The skill does not extract your master Renatus password from CDP — it reads existing session tokens only.

---
name: renatus-icm
description: Run a Renatus event marketing campaign as an ICM (Independent Campaign Manager). Use when managing Renatus event registrations, sending commercial email campaigns, setting up event landing pages, downloading/exporting leads, syncing unsubscribes to Renatus, or performing browser-based guest registration via CDP. Handles: Supabase Edge Function registration (submit-renatus-registration), gws/gog email sending (commercial-core-day1), bounce detection and SMS recovery, CDP browser registration/delete scripts, weekly unsubscribe cron, and lead export via lead-admin-export. Trigger phrases: "run a Renatus event campaign", "send Renatus email campaign", "register a guest for Renatus", "download Renatus leads", "set up event landing page", "handle Renatus unsubscribes".
---
# Renatus ICM Skill

Complete toolkit for running a Renatus event marketing campaign: event page setup, email campaigns, lead management, and unsubscribe sync.

## Workflows Quick Reference

See [references/workflows.md](references/workflows.md) for detailed step-by-step:
- **New Event Setup** → [event-page-setup.md](references/event-page-setup.md)
- **Email Campaign** → [email-campaign.md](references/email-campaign.md)
- **CDP Registration** → scripts `renatus_register_guest.py`, `renatus_delete_lead.py`
- **Lead Export** → Supabase lead-admin-export edge function
- **Unsubscribe Sync** → `weekly_unsubscribe_sync.sh`

## Architecture Overview
## Generate a New Event Landing Page

```bash
python3 scripts/generate_event_page.py   --event-url "https://backoffice.myrenatus.com/Events/EventDetails?eventId=..."   --output site/my-event/index.html
```

Requirements: Chrome/Brave CDP + active Renatus session. The script extracts event name, date(s), location, speakers, and session details from the backoffice page — then renders a complete ready-to-deploy HTML file. Preview before saving with `--dry-run`.



```
Event Landing Page (HTML)
  ↓ form submit
Supabase Edge Function: submit-renatus-registration
  ↓ server-side Renatus API (no CORS)
Renatus Back Office (lead created + registered)
  ↓ insert
Supabase: funnel_leads table
  ↓
lead-admin-export edge function ← ICM exports here
```

**Key URLs:**
- Landing page: `https://YOUR_REGISTRATION_PAGE/` (example)
- Supabase edge: `https://<REF>.supabase.co/submit-renatus-registration`
- Lead export: `https://<REF>.supabase.co/lead-admin-export`
- Renatus back office: `https://backoffice.myrenatus.com`

## Email Campaign

### Send Batch
```bash
python3 scripts/send_commercial_email_batches.py --batch-size 20 --start 0 --send
```
Resume from next batch: change `--start N`. Skip already-sent via `--skip-sent` (default on). See [email-campaign.md](references/email-campaign.md) for bounce handling, unsubscribe sync, and template customization.

### Prerequisites
- `gws` CLI authenticated as sender account
- `renatus_leads.csv` with `email` column
- `commercial-core-day1.html` template

## Browser-Based Registration (CDP)

Requires Chrome/Brave with `--remote-debugging-port=9222` and active Renatus session.

### Register Guest (dry run)
```bash
python3 scripts/renatus_register_guest.py \
  --first-name Jane --last-name Smith \
  --email jane@example.com --phone "(555) 555-5555" \
  --event-id 0817966f-b9bb-448e-bbb8-b4160115bcc8
```

### Execute Registration
Add `--execute` to perform writes.

### Delete Lead (unsubscribe)
```bash
python3 scripts/renatus_delete_lead.py --email jane@example.com --execute
```


### Generate Events Calendar
```bash
python3 scripts/generate_calendar.py --output site/calendar.html
python3 scripts/generate_calendar.py --dry-run
```
Reads `events[]` from `config.json`, generates a calendar page listing all active events with registration links.

### Add Event (One-Command Setup)
```bash
python3 scripts/add_event.py   --event-url "https://backoffice.myrenatus.com/Events/EventDetails?eventId=..."   --output site/my-event/index.html
```
Scrapes event from Renatus → adds to `config.json` → generates landing page in one step. Requires Chrome/Brave CDP + active Renatus session.

### Download Leads from Supabase
```bash
python3 scripts/renatus_leads.py --export
# Or: SUPABASE_URL=... LEAD_ADMIN_TOKEN=... python3 scripts/renatus_leads.py --export
```
Exports to `workspace/renatus_leads.csv` + `renatus_leads.json`. Set `SUPABASE_URL` and `LEAD_ADMIN_TOKEN` env vars, or pass `--ref` + `--token` flags. Use `--convert-json` to convert an existing JSON export to CSV format.

## Lead Export

### Supabase Admin Export
```bash
curl -H "x-admin-token: $TOKEN" \
  "https://<REF>.supabase.co/functions/v1/lead-admin-export?limit=500"
```

Token = `LEAD_ADMIN_TOKEN` secret in Supabase. See [supabase-setup.md](references/supabase-setup.md) for setup.

### Download via Agent
If running as an OpenClaw agent:
```bash
# From workspace: logs/email_send_log.json tracks sent emails
# Download leads to: workspace/renatus_leads.csv
```

## Configuration (config.json)

Copy `config.json.example` to `config.json` and fill in your values. Scripts auto-load it:

## Configuration (config.json)

Copy `config.json.example` to `config.json` and fill in your values. Scripts auto-load it:

```bash
cp config.json.example config.json
# edit config.json with your Supabase URL, Renatus credentials, sender account, etc.
```

Alternatively, set `RENATUS_*` environment variables. Scripts check (in order): `config.json` → env vars → defaults.

Environment variables: `RENATUS_SUPABASE_REF`, `RENATUS_SUPABASE_URL`, `RENATUS_LEAD_TOKEN`, `RENATUS_USERNAME`, `RENATUS_PASSWORD`, `RENATUS_EVENT_ID`, `RENATUS_SENDER`, `RENATUS_PROVIDER`, `RENATUS_TEMPLATE`, `RENATUS_UNSUB_URL`, `RENATUS_SITE_URL`, `RENATUS_REGISTRATION_URL`.

**Important:** `config.json` is gitignored. Your personal config stays private; `config.json.example` is what other ICMs receive.


---

## Supabase Setup (New ICM)

See [supabase-setup.md](references/supabase-setup.md) for full setup:
1. Link project: `supabase link --project-ref <REF>`
2. Push migrations: `supabase db push`
3. Deploy functions: `submit-renatus-registration`, `lead-admin-export`
4. Set secrets: `RENATUS_USERNAME`, `RENATUS_PASSWORD`, `RENATUS_EVENT_ID`, `LEAD_ADMIN_TOKEN`
5. Verify: submit test registration → check `funnel_leads` + Renatus back office

## Supabase Edge Function Reference

### submit-renatus-registration
Public POST endpoint. Registers a lead in Renatus via server-side API (bypasses CORS). Auto-detects public-eligible sessions (no IMA/education requirements). Required secrets: `RENATUS_USERNAME`, `RENATUS_PASSWORD`, `RENATUS_EVENT_ID`.

### lead-admin-export
Admin GET endpoint. Requires `x-admin-token` header. Params: `?partner=&limit=`.

### capture-lead
General-purpose public lead intake with Turnstile bot protection. Insert into `funnel_leads`.

## Key Secrets (Supabase)

| Secret | Required | Purpose |
|---|---|---|
| `RENATUS_USERNAME` | Registration | Back office login |
| `RENATUS_PASSWORD` | Registration | Back office password |
| `RENATUS_EVENT_ID` | Registration | Default event GUID |
| `LEAD_ADMIN_TOKEN` | Export | Admin export auth |
| `SUPABASE_URL` | Always | Project URL |
| `SUPABASE_SERVICE_ROLE_KEY` | Always | DB access |

## Unsubscribe Sync (Weekly Cron)

```bash
# Add to crontab
0 2 * * 0 /home/umbrel/.openclaw/workspace/scripts/weekly_unsubscribe_sync.sh

# Manual run
CDP_URL=http://127.0.0.1:9222 bash scripts/weekly_unsubscribe_sync.sh
```
Requirements: Chrome CDP at 9222 + active Renatus session. See [email-campaign.md](references/email-campaign.md).

## Bounce Recovery

```bash
# Detect bounces
python3 scripts/handle_bounced_emails.py --check

# Export SMS-ready contacts
python3 scripts/handle_bounced_emails.py --export-sms

# Manually mark bounce
python3 scripts/handle_bounced_emails.py --mark-bounced user@example.com
```

## Authentication: Two Options

### Option A — Browser Relay (Recommended for CDP scripts)
Use your existing logged-in Brave/Chrome session via Browser Relay (OpenClaw extension).

1. Open Brave → click the **OpenClaw Browser Relay** extension icon on any Renatus tab
2. Scripts connect to `http://127.0.0.1:9222` via Playwright CDP
3. No credentials needed in config — reads existing session tokens from localStorage/cookies
4. Requires the OpenClaw Browser Relay extension with an active tab

**CDP scripts affected:** `renatus_register_guest.py`, `renatus_delete_lead.py`, `generate_event_page.py`, `add_event.py`

### Option B — Env Vars (Recommended for non-CDP scripts)
Set credentials as environment variables — never in chat or config files.

```bash
export RENATUS_USERNAME="earlvanze@gmail.com"
export RENATUS_PASSWORD="YOUR_PASSWORD"
export RENATUS_EVENT_ID="0817966f-b9bb-448e-bbb8-b4160115bcc8"
export LEAD_ADMIN_TOKEN="YOUR_SUPABASE_TOKEN"
```

Or use a `.env` file loaded by your shell profile. Scripts read from env vars via `config_loader.py`.

**Non-CDP scripts:** `renatus_leads.py`, `send_commercial_email_batches.py`, `generate_calendar.py`, `generate_email_template.py`

### Security Rules
- **Never paste credentials in chat** — use env vars or `.env` files
- **Bitwarden CLI** (`bw`) for programmatic credential access: `bw get password "Renatus"`
- CDP reads do not extract your master password — only existing session tokens
- Config file (`config.json`) should use `[REDACTED — see Nextcloud/secrets]` for credential placeholders
- Rotate credentials after any shared exposure
