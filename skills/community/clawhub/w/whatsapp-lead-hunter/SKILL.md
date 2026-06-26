---
name: whatsapp-lead-hunter
description: Automated lead generation and WhatsApp outreach system. Scrape business leads from Google Maps by sector and location, generate personalized pitch messages, and send them via WAHA (WhatsApp HTTP API). Use when building sales pipelines, doing cold outreach to local businesses, or automating WhatsApp marketing campaigns. Supports any sector (salons, veterinarians, dentists, restaurants, real estate, auto repair, etc). Includes bot-safe ignore lists to prevent auto-reply conflicts.
---

# WhatsApp Lead Hunter

Automated lead generation pipeline: Google Maps → Lead Database → Personalized Pitch → WAHA WhatsApp Delivery.

## How It Works

1. **Scrape** — Use browser tool to search Google Maps for businesses by sector + location
2. **Extract** — Pull name, phone, rating, reviews, website, Instagram from each listing
3. **Store** — Save leads as JSON in organized directory structure
4. **Pitch** — Generate personalized messages based on business profile (rating, website presence, pain points)
5. **Send** — Deliver via WAHA WhatsApp API with configurable delays between messages
6. **Protect** — Add all outreach numbers to bot ignore list (prevents auto-reply conflicts)

## Prerequisites

- **WAHA** running (WhatsApp HTTP API) — Docker container with active WhatsApp session
- **Browser tool** — For Google Maps scraping
- **WhatsApp Business number** connected to WAHA

## Quick Start

### 1. Search for Leads

Use the browser tool to navigate to Google Maps:

```
https://www.google.com/maps/search/{sector}+{location}
```

Examples:
```
https://www.google.com/maps/search/veteriner+uşak
https://www.google.com/maps/search/kuaför+simav+kütahya
https://www.google.com/maps/search/diş+kliniği+istanbul
https://www.google.com/maps/search/auto+repair+london
```

Click each listing to extract: name, phone, rating, reviews, website, Instagram, hours.

### 2. Store Leads

Save as JSON:

```json
[
    {
        "name": "Business Name",
        "phone": "905551234567",
        "rating": "4.8",
        "reviews": 120,
        "website": "example.com",
        "instagram": "instagram.com/handle",
        "hours": "Open · Closes 8 pm",
        "notes": "Key observations"
    }
]
```

Directory structure:
```
leads/
├── {city}/
│   ├── {sector}.json
│   ├── veteriner.json
│   ├── dis_klinigi.json
│   └── kuafor.json
```

### 3. Craft Pitch Messages

Personalize based on business profile. See `references/pitch-templates.md` for sector-specific templates.

**Key personalization signals:**
- **No website** → "online presence" angle
- **Low rating** → "customer satisfaction improvement" angle
- **High reviews** → "you're already popular, scale it" angle
- **Has Instagram but no website** → "convert followers to customers" angle

### 4. Send via WAHA

```bash
curl -X POST "http://localhost:3000/api/sendText" \
  -H "X-Api-Key: YOUR_WAHA_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "session": "default",
    "chatId": "905551234567@c.us",
    "text": "Your personalized message here"
  }'
```

**Sending rules:**
- Minimum 2 minutes between messages (avoid WhatsApp spam detection)
- Maximum 15-20 messages per batch
- Send during business hours (09:00-18:00 local time)
- Never send the same template to the same number twice

### 5. Protect Against Bot Auto-Reply

If you have a WhatsApp bot (like a customer service bot), add all outreach numbers to an ignore list so the bot doesn't reply with irrelevant messages.

**File-based ignore list** (recommended):

Create `data/outreach_ignore_lids.txt`:
```
# Outreach targets - bot will NOT auto-reply
# Add both @lid IDs and phone numbers
905551234567
127517595824360
```

**Webhook filter** in your bot:

```python
# In your WhatsApp webhook handler, before processing:
ignore_file = "data/outreach_ignore_lids.txt"
if os.path.exists(ignore_file):
    with open(ignore_file) as f:
        ignore_ids = {line.strip() for line in f if line.strip() and not line.startswith('#')}
    clean_id = from_id.replace("@lid","").replace("@c.us","")
    if clean_id in ignore_ids:
        # Don't auto-reply, but notify admin
        notify_admin(f"Outreach reply from {from_id}: {message}")
        return
```

**Important:** WAHA uses `@lid` format internally which differs from phone numbers. Always add BOTH the lid ID and the phone number to your ignore list.

## Batch Send Script

For automated batch sending, use `scripts/batch_send.sh`:

```bash
scripts/batch_send.sh \
  --leads leads/usak/veteriner.json \
  --template references/pitch-templates.md \
  --sector veteriner \
  --waha-url http://localhost:3000 \
  --waha-key YOUR_KEY \
  --delay 120 \
  --ignore-file data/outreach_ignore_lids.txt
```

## Sector-Specific Angles

See `references/pitch-templates.md` for full templates. Quick reference:

| Sector | Pain Point | Our Solution |
|--------|-----------|-------------|
| Salon/Kuaför | Missed calls during service | WhatsApp auto-appointment |
| Veteriner | Forgotten vaccine schedules | Auto vaccine reminders |
| Diş Kliniği | No-show appointments (30%+) | Appointment reminders |
| Emlakçı | Lead tracking chaos | Auto property matching |
| Oto Servis | Missed maintenance cycles | Service interval reminders |
| Restoran | Reservation no-shows | WhatsApp reservation + reminder |
| Fotoğrafçı | Client/shoot tracking | CRM + auto follow-up |

## Security

- **No credentials in skill files** — WAHA key passed as parameter or environment variable
- **No direct config access** — Uses OpenClaw CLI for any gateway operations
- **Rate limiting built-in** — Configurable delays prevent WhatsApp spam flags
- **Ignore list is append-only** — New outreach targets are added, never removed
- **Admin notifications** — All outreach replies forwarded to admin (Telegram/SMS/etc)

## Tips

- Start with 10-15 leads per batch, scale up after testing response rates
- Personalized messages get 3-5x more replies than generic templates
- Best days: Tuesday-Thursday. Best times: 10:00-12:00, 14:00-16:00
- Follow up non-responders after 3-5 days with a shorter message
- Track conversion: lead → reply → demo → customer
