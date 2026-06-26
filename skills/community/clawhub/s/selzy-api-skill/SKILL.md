---
name: selzy
description: >
  Create and send email marketing campaigns via Selzy API.
  Manage contacts, segments, templates. Schedule campaigns,
  run A/B tests, and analyze performance (opens, clicks, bounces).
  Turn natural language requests into full email campaigns.
  
  **v2.1 — Fixed critical bug:** Campaigns now require explicit list_id verification.
  Without list_id, Selzy sends to 1 contact only. Always call getLists first.
metadata:
  openclaw:
    emoji: "✉️"
    requires:
      env:
        - SELZY_API_KEY
    primaryEnv: SELZY_API_KEY
  version: "2.3"
  lastUpdated: "2026-02-26"
  changelog:
    - "2.3: HARD LIMIT changed to 1 campaign per HOUR (was 1/min) after 35-campaign ban incident"
    - "2.2: Added RATE LIMIT WARNING — max 1 campaign per minute, batch sends forbidden"
    - "2.2: Documented account ban risk: 35 campaigns in few minutes triggered block"
    - "2.1: Added CRITICAL WARNING section about list_id requirement"
    - "2.1: Added SAFETY CHECKLIST for all campaign sends"
    - "2.1: Added real-world bug fix example (1 vs 4 recipients)"
    - "2.1: Updated all workflows to verify contact count before sending"
---

# Selzy Email Marketing API — Complete Guide

Selzy is an email marketing platform with a REST API for managing contacts, creating campaigns, and analyzing performance. This skill lets you run your entire email marketing from an AI assistant.

---

## 🚨 CRITICAL WARNING — Read Before Using

### ⚠️ Common Pitfall: Campaigns Sent to Wrong Recipients

**Problem:** If you create a campaign without explicitly specifying `list_id`, Selzy will send to **ONLY 1 contact** (default behavior), not your entire list.

**Solution:** ALWAYS follow this workflow:
1. Call `getLists` → get the correct `list_id` AND verify contact count
2. Pass `list_id` to `createEmailMessage` (REQUIRED parameter)
3. Verify recipient count matches expectations BEFORE calling `createCampaign`
4. Get explicit user confirmation before sending

**This affects ALL users.** The fix is in the workflow, not the API.

---

### 🚫 RATE LIMIT WARNING — Account Ban Risk

**REAL INCIDENT (2026-02-25):** User sent **35 email campaigns in a few minutes** using `createCampaign`. Selzy blocked the account for suspicious bulk activity.

**Official Selzy API Rate Limits** (from https://selzy.com/en/support/api/common/selzy-api-limits/):

| Endpoint / Action | Limit |
|-------------------|-------|
| **General API** | 1200 requests / 60 seconds (per API key or IP) |
| **checkEmail method** | 300 requests / 60 seconds |
| **subscribe method** | Limited (exact value not published) |
| **sendEmail method** | 1,000 emails/day default for new users (auto-increases) |
| **sendSms method** | 150 numbers per call |
| **getCampaigns method** | 10,000 campaigns per response |
| **getMessages limit** | 100 records per request (default 50) |
| **importContacts timeout** | 30 seconds per call |

**⚠️ CRITICAL: Campaign Creation Rate (UNPUBLISHED but ENFORCED)**

While general API allows 1200 req/min, **creating campaigns (`createCampaign`) has additional fraud detection**:
- **MAX 1 campaign creation per HOUR** (strict limit after ban incident)
- **Burst of 35 campaigns in <5 min = instant account block** (real incident 2026-02-25)
- Selzy's fraud system flags rapid campaign creation as suspicious bulk activity

**Why the discrepancy?**
- 1200 req/min is for **read operations** (getLists, getCampaigns, stats)
- **Write operations** (createCampaign, importContacts) have stricter anti-abuse limits
- No official documentation on campaign creation rate — enforced heuristically

**Symptoms of Rate Limit Violation:**
- API returns `count=0` for all campaigns (even valid ones)
- Campaigns stuck in `scheduled` status but never send
- Account flagged for manual review

**Recovery:**
1. **STOP all campaign creation immediately**
2. Wait 24-48 hours for automatic unblock OR contact Selzy support
3. Request manual review + explain it was automation error
4. When unblocked: implement rate limiting (**1 campaign / hour MAX**)

**Prevention:**
- **Wait 1 HOUR between `createCampaign` calls** — this is now the hard limit
- For batch sends: create max 1 campaign per hour, spread across days
- Monitor API responses: `count=0` across multiple campaigns = RED FLAG
- **NEVER automate bulk campaign creation without rate limiting**
- Remember: 1200 req/min is for READ operations, not campaign creation

**If you need to send to multiple segments:**
```
1. Create all email messages first (no rate limit on createEmailMessage)
2. Schedule campaigns across multiple days (1 per hour max)
3. OR: use single campaign with segmented list (preferred)
4. Use cron jobs with hourly spacing for automated sends
```

**This is now MANDATORY:** Any automation creating >1 campaign per hour will risk permanent ban. **1 campaign per hour = HARD LIMIT.**

---

### 📊 Official Selzy API Limits Summary

| Operation | Limit | Notes |
|-----------|-------|-------|
| General API calls | 1200 / min | Per API key or IP |
| checkEmail | 300 / min | Email validation |
| sendEmail (transactional) | 1000 / day | New users, auto-increases |
| sendSms | 150 / call | Max numbers per request |
| getCampaigns | 10,000 / response | Pagination needed for more |
| getMessages | 100 / request | Default 50 |
| importContacts | 30s timeout | Per call |
| **createCampaign** | **1 / hour** | **Unpublished, HARD LIMIT after ban incident** |

**Source:** https://selzy.com/en/support/api/common/selzy-api-limits/

---

## 🔐 Authentication

All requests require the `SELZY_API_KEY` environment variable. Pass it as the `api_key` parameter.

**Base URL:** `https://api.selzy.com/en/api`

**Important:** All methods use `GET` with query parameters (Selzy API uses GET for all endpoints). URL-encode parameter values when needed.

## General Request Pattern

```bash
curl "https://api.selzy.com/en/api/{METHOD}?format=json&api_key=$SELZY_API_KEY&{params}"
```

**Response Format:**
- Success: `{"result": {...}}` or `{"result": [...]}`
- Error: `{"error": "message", "code": "error_code"}`

---

## 📋 1. Contact Lists

### 1.1 Get Lists — `getLists`

Retrieve all contact lists.

```bash
curl "https://api.selzy.com/en/api/getLists?format=json&api_key=$SELZY_API_KEY"
```

**Response:**
```json
{
  "result": [
    {"id": 1, "title": "Newsletter subscribers", "count": 15420, "active_contacts": 14800}
  ]
}
```

### 1.2 Create List — `createList`

Create a new contact list.

```bash
curl "https://api.selzy.com/en/api/createList?format=json&api_key=$SELZY_API_KEY&title=VIP%20Customers"
```

**Response:** `{"result": {"id": 12345}}`

### 1.3 Get List Details — `getList`

Get detailed info about a specific list.

```bash
curl "https://api.selzy.com/en/api/getList?format=json&api_key=$SELZY_API_KEY&list_id=12345"
```

---

## 👥 2. Contact Management

### 2.1 Import Contacts — `importContacts`

Bulk import contacts into a list.

```bash
curl "https://api.selzy.com/en/api/importContacts?format=json&api_key=$SELZY_API_KEY&field_names[]=email&field_names[]=Name&data[][]=john@example.com&data[][]=John&data[][]=jane@example.com&data[][]=Jane&list_ids=12345&overwrite=2"
```

| Parameter | Description |
|-----------|-------------|
| `field_names[]` | Column names: email (required), Name, phone, etc. |
| `data[][]` | Contact data rows (flat array, fills row by row) |
| `list_ids` | Comma-separated list IDs to add contacts to |
| `overwrite` | 0=skip existing, 1=overwrite all, 2=overwrite empty only |

### 2.2 Subscribe — `subscribe`

Add a single contact with opt-in control.

```bash
curl "https://api.selzy.com/en/api/subscribe?format=json&api_key=$SELZY_API_KEY&list_ids=12345&fields[email]=user@example.com&fields[Name]=Alice&double_optin=3"
```

**double_optin values:**
- `0` = no confirmation
- `3` = send confirmation email
- `4` = already confirmed (force subscribe)

### 2.3 Exclude Contact — `exclude`

Unsubscribe/remove a contact.

```bash
curl "https://api.selzy.com/en/api/exclude?format=json&api_key=$SELZY_API_KEY&contact_type=email&contact=user@example.com"
```

### 2.4 Get Contact — `getContact`

Get contact details by email.

```bash
curl "https://api.selzy.com/en/api/getContact?format=json&api_key=$SELZY_API_KEY&email=user@example.com"
```

### 2.5 Create Custom Field — `createField`

Add a custom field for contacts.

```bash
curl "https://api.selzy.com/en/api/createField?format=json&api_key=$SELZY_API_KEY&field_name=Company&field_type=text"
```

**field_type options:** `text`, `number`, `date`, `boolean`

---

## 📧 3. Email Messages (Templates)

### 3.1 Create Email Message — `createEmailMessage`

⚠️ **CRITICAL: `list_id` is REQUIRED** ⚠️

**Without `list_id`, Selzy will send to ONLY 1 contact (default behavior).** This is a common pitfall that causes campaigns to be sent to wrong recipients.

**ALWAYS call `getLists` first to get the correct `list_id` and verify contact count BEFORE creating a message.**

Create an email template for campaigns.

```bash
curl "https://api.selzy.com/en/api/createEmailMessage?format=json&api_key=$SELZY_API_KEY&sender_name=My%20Store&sender_email=news@yourdomain.com&subject=Summer%20Sale%20🔥&body=<h1>Hello!</h1><p>Check%20out%20our%20deals</p>&list_id=12345"
```

| Parameter | Required | Description |
|-----------|----------|-------------|
| `sender_name` | Yes | From name |
| `sender_email` | Yes | From email (must be verified domain) |
| `subject` | Yes | Email subject line |
| `body` | Yes | HTML content (URL-encoded) |
| `list_id` | **YES — CRITICAL** | **Target list ID. MUST be obtained from `getLists`. Without this, campaign sends to 1 contact only!** |
| `lang` | No | Language code (en, ru, es, etc.) |
| `text_body` | No | Plain text version for fallback |
| `tag` | No | Campaign tag for filtering/analytics |

**Response:** `{"result": {"message_id": 67890}}`

### 3.2 Update Email Message — `updateEmailMessage`

Modify an existing email template.

```bash
curl "https://api.selzy.com/en/api/updateEmailMessage?format=json&api_key=$SELZY_API_KEY&id=67890&subject=Updated%20Subject"
```

### 3.3 Get Message — `getMessage`

Get email template details.

```bash
curl "https://api.selzy.com/en/api/getMessage?format=json&api_key=$SELZY_API_KEY&id=67890"
```

### 3.4 List Messages — `listMessages`

List all email templates with date filter.

```bash
curl "https://api.selzy.com/en/api/listMessages?format=json&api_key=$SELZY_API_KEY&date_from=2026-01-01&date_to=2026-02-01"
```

### 3.5 Create Email Template — `createEmailTemplate`

Create a reusable template (separate from messages).

```bash
curl "https://api.selzy.com/en/api/createEmailTemplate?format=json&api_key=$SELZY_API_KEY&name=Welcome%20Series&subject=Welcome!&body=<h1>Welcome {{Name}}!</h1>"
```

### 3.6 Get Template — `getTemplate`

Get template details.

```bash
curl "https://api.selzy.com/en/api/getTemplate?format=json&api_key=$SELZY_API_KEY&template_id=12345"
```

---

## 🚀 4. Campaigns

### 4.1 Create Campaign — `createCampaign`

Create and schedule a campaign.

```bash
curl "https://api.selzy.com/en/api/createCampaign?format=json&api_key=$SELZY_API_KEY&message_id=67890&start_time=2026-02-10%2010:00:00&timezone=Europe/Moscow&track_read=1&track_links=1"
```

| Parameter | Required | Description |
|-----------|----------|-------------|
| `message_id` | Yes | Email message ID from createEmailMessage |
| `start_time` | No | Schedule time (YYYY-MM-DD HH:MM:SS). Omit for immediate send |
| `timezone` | No | Timezone for scheduled send (e.g., Europe/Belgrade) |
| `track_read` | No | Track opens (1=yes, 0=no) |
| `track_links` | No | Track clicks (1=yes, 0=no) |

**Response:** `{"result": {"campaign_id": 11111}}`

### 4.2 Cancel Campaign — `cancelCampaign`

Cancel a scheduled campaign before it sends.

```bash
curl "https://api.selzy.com/en/api/cancelCampaign?format=json&api_key=$SELZY_API_KEY&campaign_id=11111"
```

### 4.3 Get Campaign Status — `getCampaignStatus`

Check campaign status and progress.

```bash
curl "https://api.selzy.com/en/api/getCampaignStatus?format=json&api_key=$SELZY_API_KEY&campaign_id=11111"
```

**Status values:** `draft`, `scheduled`, `sending`, `analysed`, `canceled`

### 4.4 Get Campaigns — `getCampaigns`

List recent campaigns with optional date filter.

```bash
curl "https://api.selzy.com/en/api/getCampaigns?format=json&api_key=$SELZY_API_KEY&from=2026-01-01&to=2026-02-24"
```

**Date format:** `YYYY-MM-DD HH:MM:SS` or `YYYY-MM-DD`

---

## 📊 5. Campaign Statistics

### 5.1 Get Campaign Stats — `getCampaignCommonStats`

Get comprehensive statistics for a campaign.

```bash
curl "https://api.selzy.com/en/api/getCampaignCommonStats?format=json&api_key=$SELZY_API_KEY&campaign_id=11111"
```

**Response:**
```json
{
  "result": {
    "total": 15000,
    "sent": 14800,
    "delivered": 14500,
    "read_unique": 4200,
    "read_all": 5100,
    "clicked_unique": 890,
    "clicked_all": 1200,
    "unsubscribed": 12,
    "spam": 3
  }
}
```

**Metrics to calculate:**
- **Open Rate** = `(read_unique / delivered) × 100`
- **Click Rate** = `(clicked_unique / delivered) × 100`
- **Bounce Rate** = `((sent - delivered) / sent) × 100`
- **Unsubscribe Rate** = `(unsubscribed / delivered) × 100`
- **Spam Rate** = `(spam / delivered) × 100`

---

## 📮 6. Senders

### 6.1 Get Sender Emails — `getSenderEmails`

List all verified sender emails.

```bash
curl "https://api.selzy.com/en/api/getSenderEmails?format=json&api_key=$SELZY_API_KEY"
```

**Response:**
```json
{
  "result": [
    {
      "id": 8526648,
      "email": "news@yourdomain.com",
      "name": "Your Store",
      "isVerified": true,
      "dkimStatus": "verified",
      "isFreeDomain": false
    }
  ]
}
```

**Note:** `sender_email` in campaigns must be from this verified list.

---

## 🎯 Instructions for the Agent

### Critical Rules

#### 🚨 SAFETY CHECKLIST (Before Any Campaign Send)

**MANDATORY — verify ALL before proceeding:**
- [ ] `getLists` called → have explicit `list_id`
- [ ] Contact count verified → matches expected recipients
- [ ] If count = 0 or count != expected → **STOP and alert user**
- [ ] `createEmailMessage` includes `list_id` parameter
- [ ] User confirmed: list name, count, subject, send time
- [ ] Explicit "send" or "confirm" received from user
- [ ] **RATE LIMIT CHECK:** Last campaign created >1 HOUR ago (HARD LIMIT)
- [ ] **BATCH WARNING:** If creating >1 campaign per hour = ACCOUNT BAN RISK

**If ANY check fails → DO NOT SEND, ask user first.**

**CRITICAL: Creating 35 campaigns in a few minutes = ACCOUNT BAN. MAX 1 campaign per HOUR.**

---

1. **NEVER send a campaign without explicit user confirmation.** Always show:
   - Recipient list name and count (**VERIFY this matches expectations**)
   - Subject line
   - Body summary (first 100 chars)
   - Send time (immediate or scheduled)
   - **list_id being used**

2. **For new campaigns, follow this workflow (MANDATORY):**
   ```
   1. getLists → GET list_id AND count of contacts
   2. VERIFY: count >= expected recipients (if count=0, STOP and ask)
   3. createEmailMessage → MUST include list_id parameter + confirm subject + content
   4. RATE LIMIT CHECK: If created campaign in last 60s, WAIT before proceeding
   5. createCampaign → confirm timing + recipient count
   6. WAIT for explicit "send" or "confirm" from user
   ```

   **⚠️ BATCH SENDS:** If creating multiple campaigns (e.g., for different segments):
   - Create all `createEmailMessage` calls first (no rate limit)
   - Queue `createCampaign` calls with **1 HOUR delays** between each (HARD LIMIT)
   - **NEVER** create >1 campaign per hour — instant ban risk
   - Real incident: 35 campaigns in few minutes = account blocked
   - Use cron jobs to space campaigns across days if needed

3. **CRITICAL: list_id is REQUIRED**
   - NEVER create email message without explicit list_id
   - ALWAYS verify contact count matches expectations before sending
   - If list_id is missing or count is wrong → STOP and alert user

4. **For statistics requests:**
   - Always calculate rates as percentages
   - Compare to industry benchmarks if asked (avg: 20% open, 2.5% click)
   - Highlight trends (up/down vs previous campaigns)

4. **Handle errors gracefully:**
   - Explain what went wrong in plain language
   - Suggest specific fixes
   - Retry once for rate limiting (add 1s delay)

5. **Security reminders:**
   - Never log or display the full API key
   - Remind users that sender_email must be verified
   - Warn about GDPR/compliance for contact imports

### Common Workflows

#### "Create a campaign for my VIP customers"
```
1. getLists → find VIP list, confirm count (MUST match expected recipients)
2. If count is wrong → STOP and alert user (DO NOT proceed)
3. Ask: subject, content type (promo/newsletter/event)
4. createEmailMessage → MUST include list_id parameter, show preview
5. createCampaign (omit start_time for immediate)
6. ⚠️ WAIT for "send it" or "confirm" before considering it done
7. Report: campaign_id, status, recipient count (verify matches step 1)
```

#### "How did my last campaign perform?"
```
1. getCampaigns (last 7 days) → get latest campaign_id
2. getCampaignCommonStats → get metrics
3. Calculate: open rate, click rate, bounce rate, unsubscribe rate
4. Present as: "X% opened, Y% clicked, Z% bounced"
5. Optional: compare to industry avg or previous campaign
```

#### "Add new subscribers to my newsletter"
```
1. getLists → find newsletter list
2. Confirm: list name, number of contacts to add
3. importContacts (bulk) OR subscribe (single)
4. Report: success count, skipped count, errors
```

#### "Show my contact lists"
```
1. getLists → retrieve all
2. Present table: Name | Total | Active | Created
3. Offer: "Want to create a new list or add contacts?"
```

#### "Schedule a webinar invitation"
```
1. getLists → confirm audience (GET list_id + count)
2. VERIFY count matches expected recipients
3. Ask: webinar details (title, date, time, link)
4. createEmailMessage with storytelling approach + list_id parameter
5. createCampaign with start_time="2026-02-25 10:00:00" timezone="Europe/Belgrade"
6. Confirm: "Scheduled for Feb 25 at 10:00 AM Belgrade time to {count} recipients"
```

---

## 📖 Real-World Bug Fix Example

### ❌ WRONG — Campaign sent to 1 person instead of 4

```bash
# Missing list_id — Selzy sends to 1 contact by default!
curl "https://api.selzy.com/en/api/createEmailMessage?format=json&api_key=$KEY&sender_name=My+Store&sender_email=me@example.com&subject=Sale&body=<h1>Sale!</h1>"
```

**Result:** Campaign #327590492 sent to 1 recipient instead of 4 contacts in list.

### ✅ CORRECT — Always include list_id

```bash
# Step 1: Get lists and verify count
curl "https://api.selzy.com/en/api/getLists?format=json&api_key=$KEY"
# Response: [{"id": 12345, "title": "My first list", "count": 4}]

# Step 2: Create message WITH list_id
curl "https://api.selzy.com/en/api/createEmailMessage?format=json&api_key=$KEY&sender_name=My+Store&sender_email=me@example.com&subject=Sale&body=<h1>Sale!</h1>&list_id=12345"
# Response: {"result": {"message_id": 67890}}

# Step 3: Create campaign
curl "https://api.selzy.com/en/api/createCampaign?format=json&api_key=$KEY&message_id=67890"
# Response: {"result": {"campaign_id": 11111}}

# Result: Campaign sent to ALL 4 contacts ✅
```

---

## ⚠️ API Error Handling

| Error Response | Meaning | Fix |
|----------------|---------|-----|
| `"error": "Incorrect API key"` | Wrong/missing API key | Check SELZY_API_KEY in config |
| `"error": "Access denied"` | Insufficient permissions | Verify API key has correct scope |
| `"error": "Not found"` | Resource doesn't exist | Check ID (campaign_id, message_id, list_id) |
| `"error": "Bad date-time literal"` | Wrong date format | Use `YYYY-MM-DD HH:MM:SS` |
| HTTP 429 | Rate limited | Wait 1-2 seconds, retry once |
| `"error": "Sender not verified"` | Email not in verified list | Use getSenderEmails, pick verified one |

---

## 📚 Resources

- **API Reference:** https://selzy.com/en/support/api/
- **Getting Started:** https://selzy.com/en/support/
- **Sign Up:** https://selzy.com/en/registration/
- **Blog:** https://selzy.com/en/blog/

---

## 🧪 Quick Test Commands

Verify API access:
```bash
# Check connection
curl "https://api.selzy.com/en/api/getLists?format=json&api_key=YOUR_KEY"

# Check verified senders
curl "https://api.selzy.com/en/api/getSenderEmails?format=json&api_key=YOUR_KEY"

# Test campaign stats (replace ID)
curl "https://api.selzy.com/en/api/getCampaignCommonStats?format=json&api_key=YOUR_KEY&campaign_id=123456"
```

---

**Skill Version:** 2.0 (Complete)  
**Last Updated:** 2026-02-24  
**Tested Methods:** getLists, getSenderEmails, getCampaigns, getCampaignCommonStats, createEmailMessage, createCampaign, getTemplates
