# Renatus ICM Workflows

## Table of Contents
1. [New Event Setup](#1-new-event-setup)
2. [Launch Email Campaign](#2-launch-email-campaign)
3. [Bounce Recovery via SMS](#3-bounce-recovery-via-sms)
4. [Weekly Unsubscribe Sync](#4-weekly-unsubscribe-sync)
5. [Lead Download and Analysis](#5-lead-download-and-analysis)
6. [Direct Browser Registration (CDP)](#6-direct-browser-registration-cdp)

---

## 1. New Event Setup

### Step 1: Get Event GUID from Renatus
1. Log into `backoffice.myrenatus.com`
2. Go to Events → find the event
3. Copy the event GUID from the URL or API

### Step 2: Update Supabase Edge Function Secret
```bash
supabase secrets set RENATUS_EVENT_ID="<new_event_guid>" --project-ref <PROJECT_REF>
```

### Step 3: Update Landing Page
1. Copy `site/commercial/index.html` to new event directory
2. Update event details (date, time, location, speakers)
3. Update `EDGE_URL` in the script if using a different Supabase project
4. Deploy via FTP or `deploy_hostinger.py`

### Step 4: Update Email Template
Copy `email/commercial-core-day1.html` and update:
- Event date and time
- Event name
- Instructor names
- Subject line options

### Step 5: Test Registration
Submit a test registration and verify:
- [ ] `funnel_leads` row created in Supabase
- [ ] Lead appears in Renatus Back Office
- [ ] Email confirmation received

---

## 2. Launch Email Campaign

### Day 0: Prepare
```
1. Update email template with correct event details
2. Prepare renatus_leads.csv (export from Supabase or existing list)
3. Verify gws CLI: gws gmail list --account YOUR_SENDER@gmail.com
4. Send test email to self: python3 scripts/send_commercial_email_batches.py --limit 1 --send
```

### Day 1: Send First Batch
```
python3 scripts/send_commercial_email_batches.py --batch-size 20 --start 0 --send
```

### Ongoing: Monitor and Resume
```
# After batch 1, check for bounces
python3 scripts/handle_bounced_emails.py --check

# Send next batch
python3 scripts/send_commercial_email_batches.py --batch-size 20 --start 20 --send

# Repeat until complete
```

### Post-Campaign: Sync Unsubscribes
```
# Run after campaign has been live for a few days
bash scripts/weekly_unsubscribe_sync.sh
```

---

## 3. Bounce Recovery via SMS

When emails bounce, recover by SMS if phone number is available.

### Step 1: Detect Bounces
```bash
python3 scripts/handle_bounced_emails.py --check
```

### Step 2: Export SMS List
```bash
python3 scripts/handle_bounced_emails.py --export-sms
# Output: logs/sms_followup_list.csv
```

### Step 3: Send SMS
Review `logs/sms_followup_list.csv` and send SMS manually or via WhatsApp:

```
Hi {name}, your email bounced. Please reply with your updated email to receive info about our free Commercial Real Estate Training on April 16. -Renatus
```

---

## 4. Weekly Unsubscribe Sync

Automates removal of unsubscribed leads from Renatus.

### Setup
```bash
# Add to crontab
crontab -e
# Add: 0 2 * * 0 /home/umbrel/.openclaw/workspace/scripts/weekly_unsubscribe_sync.sh
```

### Manual Run
```bash
CDP_URL=http://127.0.0.1:9222 bash scripts/weekly_unsubscribe_sync.sh
```

### Prerequisites
- Chrome/Brave with `--remote-debugging-port=9222`
- Active login session at `backoffice.myrenatus.com`

---

## 5. Lead Download and Analysis

### Export from Supabase
```bash
# Set credentials
export SUPABASE_URL="https://<REF>.supabase.co"
export LEAD_ADMIN_TOKEN="<your_token>"

# Download all leads
python3 scripts/renatus_leads.py --export

# Or inline
python3 scripts/renatus_leads.py --ref <REF> --token <TOKEN> --export

# Convert existing JSON to CSV
python3 scripts/renatus_leads.py --convert-json
```

### Supabase Admin Export (cURL)
```bash
TOKEN="..."
REF="..."
curl -H "x-admin-token: $TOKEN" \
  "https://$REF.supabase.co/functions/v1/lead-admin-export?limit=500" \
  | jq '.rows[] | {name, email, phone: .metadata.phone, sessions: .metadata.registered_sessions}'
```

### Export from Supabase
```bash
TOKEN="..."
REF="..."
curl -H "x-admin-token: $TOKEN" \
  "https://$REF.supabase.co/functions/v1/lead-admin-export?limit=500" \
  | jq '.rows[] | {name, email, phone: .metadata.phone, sessions: .metadata.registered_sessions}'
```

### Convert to CSV
```bash
curl -s -H "x-admin-token: $TOKEN" \
  "https://$REF.supabase.co/functions/v1/lead-admin-export?limit=500" \
  | jq -r '.rows[] | [.name, .email, (.metadata.phone // ""), (.metadata.registered_sessions | join("; "))] | @csv' \
  > leads.csv
```

### Registration Rate
```python
# Count total vs registered
total_leads = len(leads)
registered = sum(1 for l in leads if l.get('metadata', {}).get('lead_id'))
print(f"Registration rate: {registered}/{total_leads} ({100*registered/total_leads:.1f}%)")
```

---

## 6. Direct Browser Registration (CDP)

Use `renatus_register_guest.py` for direct registration via a live authenticated browser session. Useful when:
- The Supabase edge function is down
- Registering a lead not from the web form
- Registering for a specific session (not just public-eligible)

### Prerequisites
- Chrome/Brave with `--remote-debugging-port=9222`
- Active Renatus session in the browser

### Usage
```bash
# Dry run (test registration)
python3 scripts/renatus_register_guest.py \
  --first-name Jane --last-name Smith \
  --email jane@example.com --phone "(518) 555-1212" \
  --event-id 0817966f-b9bb-448e-bbb8-b4160115bcc8

# Execute (actually register)
python3 scripts/renatus_register_guest.py \
  --first-name Jane --last-name Smith \
  --email jane@example.com --phone "(518) 555-1212" \
  --event-id 0817966f-b9bb-448e-bbb8-b4160115bcc8 \
  --execute

# Register for all sessions (not just first)
python3 scripts/renatus_register_guest.py \
  --first-name Jane --last-name Smith \
  --email jane@example.com --phone "(518) 555-1212" \
  --event-id 0817966f-b9bb-448e-bbb8-b4160115bcc8 \
  --all-sessions --execute

# Register for specific session(s)
python3 scripts/renatus_register_guest.py \
  --first-name Jane --last-name Smith \
  --email jane@example.com --phone "(518) 555-1212" \
  --event-id 0817966f-b9bb-448e-bbb8-b4160115bcc8 \
  --session-guid <SESSION_GUID_1> \
  --session-guid <SESSION_GUID_2> \
  --execute
```

### CDP URL
```bash
--cdp-url http://127.0.0.1:9222  # Default
--cdp-url http://<remote_ip>:9222  # Remote browser
```

### Output
- Dry run: shows which sessions would be registered, event details
- Execute: shows `leadId`, `guestUserId`, `registrationId`, session IDs

---

## Quick Reference: Renatus API Flow

The edge function and CDP scripts both perform the same API flow:

```
1. POST /Token                    → get access_token + cookies
2. GET  /Home/index               → extract __RequestVerificationToken (CSRF)
3. GET  /api/queryproxy/execute?url=/api/userprofile/current?  → ownerUserId
4. GET  /api/queryproxy/execute?url=/api/event/getsavedevent?  → event + sessions
5. POST /api/commandproxy/execute?url=/api/guestRegistration/addcustomer?  → leadId, guestUserId
6. POST /api/commandproxy/execute?url=/api/registration/fees?  → session costs
7. POST /api/commandproxy/execute?url=/api/eventRegistration/registerForEvent?  → final registration
```

### Public-Eligible Sessions
Sessions are "public-eligible" if they have NO requirements:
- `RequireActiveIMA`
- `RequireXtreamEducation`
- `RequireNoEducation`
- `RequireOneStarQualify` / `RequireThreeStarQualify` / `RequireFiveStarQualify`
- `RequireEssentialEducation` / `RequireProfitEducation` / `RequireAdvancedEducation`
- `RequireGeniusIn21DaysEducation`
- `IsLeadOnly` / `IsNonLeadOnly`

If an event has no public-eligible sessions, contact Renatus to create one.
