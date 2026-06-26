# ✉️ Selzy Email Marketing Skill for OpenClaw

Full-featured email marketing skill for managing campaigns via Selzy API. Create campaigns, manage contacts, and analyze results directly from chat.

## 🚀 Quick Start

### 1. Get Selzy API Key

1. Register at [selzy.com](https://selzy.com/en/registration/)
2. Go to Account Settings → API
3. Copy your API key

### 2. Install Skill (already installed globally)

The skill is already installed in the system. You only need to add the API key.

### 3. Add API Key to Configuration

```bash
# Open OpenClaw config
nano ~/.openclaw/openclaw.json

# Add to env section:
{
  "env": {
    "SELZY_API_KEY": "your_64_character_api_key"
  }
}

# Restart Gateway
openclaw gateway restart
```

### 4. Test It

Ask your agent:
```
Show my contact lists in Selzy
```

Or:
```
What's the stats on my last campaign?
```

---

## 📋 Features

### Contact Management
- ✅ View all contact lists
- ✅ Create new lists
- ✅ Bulk import contacts
- ✅ Add individual subscribers
- ✅ Unsubscribe contacts
- ✅ Custom fields (Company, Phone, etc.)

### Campaigns
- ✅ Create email templates
- ✅ Instant sending
- ✅ Scheduled sends
- ✅ Cancel scheduled campaigns
- ✅ A/B testing (by creating multiple campaigns)

### Analytics
- ✅ Campaign statistics (opens, clicks, unsubscribes)
- ✅ Calculate metrics (Open Rate, Click Rate, Bounce Rate)
- ✅ Compare with previous campaigns
- ✅ Real-time monitoring

### Security
- ⚠️ **Never sends campaigns without explicit confirmation**
- ⚠️ Verifies sender domains before sending
- ⚠️ Does not expose API key in logs

---

## 💡 Usage Examples

### Create a Campaign

```
Create a campaign for VIP customers with subject "Exclusive Offer"
Text: Hello! Just for you — 30% off all services until end of week.
Send now.
```

**Agent will:**
1. Find "VIP Customers" list
2. Create email message
3. Create campaign
4. **Ask for confirmation** before sending
5. Send after your "yes" or "confirm"

### Schedule a Webinar

```
Schedule webinar invitation "How to Get Rich in the Galaxy"
Date: tomorrow, 19:00 Belgrade time
Link: https://t.me/abcandy
Subject: You're invited!
```

**Agent will:**
1. Create email template
2. Create campaign with scheduled time
3. Ask for confirmation
4. Send at specified time

### Check Statistics

```
Show stats for my last campaign
```

**Agent will:**
1. Get last campaign
2. Fetch statistics
3. Calculate Open Rate, Click Rate
4. Show comparison with industry benchmarks

---

## ⚠️ CRITICAL: Read Before Using

### Bug Fixed in v2.1: Campaigns Sent to Wrong Recipients

**Problem:** If you create a campaign without explicitly specifying `list_id`, Selzy sends to **ONLY 1 contact** (default behavior), not your entire list.

**Solution:** ALWAYS follow this workflow:
1. Call `getLists` → get correct `list_id` AND verify contact count
2. Pass `list_id` to `createEmailMessage` (REQUIRED parameter)
3. Verify recipient count matches expectations BEFORE calling `createCampaign`
4. Get explicit user confirmation before sending

**This affects ALL users.** The fix is in the workflow, not the API.

### Rate Limit Warning (v2.3)

**REAL INCIDENT (2026-02-25):** User sent **35 campaigns in a few minutes**. Selzy blocked the account.

**Current Limit:** **MAX 1 campaign creation per HOUR**

- General API: 1200 requests/minute (read operations)
- Campaign creation: 1 per HOUR (fraud detection)
- Burst of 35 campaigns in <5 min = instant block

**Prevention:**
- Wait 1 HOUR between `createCampaign` calls
- Never automate bulk campaign creation without rate limiting
- Monitor API responses: `count=0` = RED FLAG

---

## 🔧 Supported Selzy API Methods

| Method | Description |
|--------|-------------|
| `getLists` | Get all contact lists |
| `createList` | Create new contact list |
| `getList` | Get list details + contact count |
| `importContacts` | Bulk import contacts |
| `subscribe` | Add single contact |
| `unsubscribe` | Unsubscribe contact |
| `createEmailMessage` | Create email template |
| `createCampaign` | Create campaign |
| `sendCampaign` | Send campaign immediately |
| `scheduleCampaign` | Schedule for later |
| `getCampaigns` | Get campaigns list |
| `getCampaignCommonStats` | Campaign statistics |
| `getSenderEmails` | Get verified sender emails |
| `cancelCampaign` | Cancel scheduled campaign |
| `deleteCampaign` | Delete campaign |

---

## 📁 Project Structure

```
~/.openclaw/skills/selzy/
├── SKILL.md           # Main skill file (loaded by OpenClaw)
├── README.md          # This documentation
├── TEST_CHECKLIST.md  # Pre-use testing guide
└── PUBLISH.md         # Publication instructions
```

---

## 🆘 Troubleshooting

### API Key Not Working
```bash
# Test API connection
curl "https://api.selzy.com/en/api/getLists?format=json&api_key=YOUR_KEY"
```

Expected: `{"result": [...]}`  
If error: Check API key in Selzy dashboard

### Campaign Not Sending
1. Verify sender email is confirmed: `getSenderEmails`
2. Check list has contacts: `getList(list_id=X)`
3. Verify campaign status: `getCampaigns`

### Rate Limited
- Wait 1 hour before creating next campaign
- Contact Selzy support if account blocked

---

## 📊 Metrics

- **Version:** 2.3
- **Tested methods:** 15+
- **Campaigns sent:** 2+
- **Deliverability:** 100%
- **Languages:** EN

---

## 📝 License

MIT License — see [LICENSE](LICENSE)

---

## 🔗 Links

- Selzy API Docs: https://selzy.com/en/support/api/
- Selzy Registration: https://selzy.com/en/registration/
