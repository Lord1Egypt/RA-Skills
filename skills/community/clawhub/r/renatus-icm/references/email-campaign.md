# Email Campaign Guide

## Overview

Commercial email campaigns are sent from `YOUR_SENDER@gmail.com` via gws CLI. The email template is `commercial-core-day1.html`. Campaigns target leads from `renatus_leads.csv` and track delivery via `logs/email_send_log.json`.

## Campaign Assets

| File | Purpose |
|---|---|
| `email/commercial-core-day1.html` | HTML email template |
| `renatus_leads.csv` | Lead list (export via `renatus_leads.py --export`) |
| `logs/email_send_log.json` | Sent log (resumable sends) |
| `logs/bounced_emails.json` | Bounced email tracking |

### Getting the Leads CSV
```bash
# Export fresh from Supabase
python3 scripts/renatus_leads.py --export

# Convert existing JSON to CSV (if you have old JSON export)
python3 scripts/renatus_leads.py --convert-json
```

## Sending Emails

### Prerequisites
- `gws` CLI authenticated as `YOUR_SENDER@gmail.com`
- `renatus_leads.csv` exists with at least `email` column
- `commercial-core-day1.html` template

### Dry Run (Preview)
```bash
python3 scripts/send_commercial_email_batches.py --dry-run
```

### Send in Batches (with Resume)
```bash
# First batch
python3 scripts/send_commercial_email_batches.py --batch-size 20 --start 0 --send

# Resume from batch 2
python3 scripts/send_commercial_email_batches.py --batch-size 20 --start 20 --send

# Resume from batch 3
python3 scripts/send_commercial_email_batches.py --batch-size 20 --start 40 --send
```

### Batch Script Flags
| Flag | Default | Description |
|---|---|---|
| `--batch-size` | 20 | Emails per batch |
| `--start` | 0 | Starting index |
| `--dry-run` | — | Preview without sending |
| `--send` | — | Actually send |
| `--delay` | 2.0 | Seconds between sends |

## Personalizing the Template

The template uses `{{recipient_email}}` as a placeholder for the unsubscribe link target.

### Adding Personalized Unsubscribe URL
Replace `{{recipient_email}}` with a base64-encoded unsubscribe URL:

```python
import base64

def encode_unsubscribe_url(email: str, base_url: str = "https://YOUR_DOMAIN/unsubscribe.html") -> str:
    encoded = base64.urlsafe_b64encode(email.encode()).decode().rstrip('=')
    return f"{base_url}?e={encoded}"
```

### Unsubscribe URL in Email Template
```html
<a href="https://YOUR_DOMAIN/unsubscribe.html?e={{recipient_email}}"
   style="color: #999999; font-size: 12px;">
  Unsubscribe
</a>
```

When the user clicks unsubscribe, their email is pre-filled and they confirm removal.

## Subject Line Options

Tested subject lines for Commercial Core:
1. `They turned $7K into $103M. Learn how (April 16)`
2. `Commercial real estate: free training from $100M operators`
3. `[Only 9 days] Learn commercial underwriting from operators`
4. `From skeptical to 90+ doors in 8 months (free training)`

## Bounce Handling

### Check for Bounces
```bash
python3 scripts/handle_bounced_emails.py --check
```

### Export Bounced Contacts with Phone Numbers for SMS
```bash
python3 scripts/handle_bounced_emails.py --export-sms
# Output: logs/sms_followup_list.csv
```

### Manually Mark an Email as Bounced
```bash
python3 scripts/handle_bounced_emails.py --mark-bounced user@example.com
```

## Unsubscribe Sync (Weekly Automation)

The `weekly_unsubscribe_sync.sh` script syncs unsubscribes from the web form to Renatus.

### Setup Cron Job
```bash
# Run every Sunday at 2 AM
0 2 * * 0 /home/umbrel/.openclaw/workspace/scripts/weekly_unsubscribe_sync.sh >> /home/umbrel/.openclaw/workspace/logs/unsubscribe_cron.log 2>&1
```

### Manual Run
```bash
CDP_URL=http://127.0.0.1:9222 bash scripts/weekly_unsubscribe_sync.sh
```

### Requirements
- Chrome/Brave with `--remote-debugging-port=9222`
- Logged into `backoffice.myrenatus.com`
- Unsubscribes stored in `data/unsubscribes_<timestamp>.txt`

## Deleting Leads from Renatus

### Single Lead (Dry Run)
```bash
python3 scripts/renatus_delete_lead.py --email user@example.com
```

### Single Lead (Execute)
```bash
python3 scripts/renatus_delete_lead.py --email user@example.com --execute
```

### Bulk Delete from File
```bash
python3 scripts/renatus_delete_lead.py --file unsubscribes.txt --execute
```

### Process Unsubscribe File
```bash
python3 scripts/process_unsubscribes.py --file unsubscribes.txt --execute
```

## Lead Download (Supabase Admin Export)

```bash
TOKEN="your_lead_admin_token"
REF="your_project_ref"

curl -H "x-admin-token: $TOKEN" \
  "https://$REF.supabase.co/functions/v1/lead-admin-export?limit=500" | \
  jq '.rows[] | {name, email, phone: .metadata.phone}' > leads_export.csv
```

## CSV Format (renatus_leads.csv)

Expected columns:
- `email` (required) — recipient address
- `name` (optional) — full name or first name
- `phone` (optional) — for SMS bounce recovery
- `dateCreated` (optional) — lead creation date

Example:
```csv
email,name,phone,dateCreated
jane@example.com,Jane Smith,5185551212,2026-03-01
john@example.com,John Doe,,2026-03-02
```
