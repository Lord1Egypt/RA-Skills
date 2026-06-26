---
name: whatsapp-business-ai
description: Automates WhatsApp conversations for local businesses — replies, bookings, lead capture, and follow-ups. Designed for gyms, restaurants, salons, clinics, and service-based businesses.
version: 1.0.0
license: MIT-0
metadata:
  openclaw:
    requires:
      env:
        - WHATSAPP_PHONE_NUMBER_ID
        - WHATSAPP_ACCESS_TOKEN
        - WHATSAPP_VERIFY_TOKEN
        - BUSINESS_HOURS_TIMEZONE
      bins:
        - node
        - npm
        - python3
    category: Automation
---

# WhatsApp Business AI Assistant

## Name & Purpose
Automates WhatsApp conversations for local businesses — handling replies, booking inquiries, lead capture, and intelligent follow-ups without requiring 24/7 human attention. Designed for gyms, restaurants, salons, clinics, and service-based businesses in South Africa.

## Prerequisites

| Requirement | Version/Detail |
|---|---|
| OpenClaw | v2.4+ |
| Node.js | v18+ |
| WhatsApp Business API (Meta) | Approved business account |
| Meta Developer App | With WhatsApp product configured |
| Python 3 | v3.10+ (for NLP pipeline) |
| `wacli` CLI | Installed on host |
| ngrok or static IP | For webhook callback |

## Installation

### 1. Copy skill files

```bash
cp -r streams/01_ClawHub_Skills/01_WhatsApp_Business_AI_Assistant/* ~/.openclaw/skills/
```

### 2. Install dependencies

```bash
cd ~/.openclaw/skills/whatsapp-business-ai
npm install
pip install -r requirements.txt
```

### 3. Configure environment

Create `~/.openclaw/skills/whatsapp-business-ai/.env`:

```env
WHATSAPP_PHONE_NUMBER_ID=your_phone_number_id
WHATSAPP_ACCESS_TOKEN=your_permanent_token
WHATSAPP_VERIFY_TOKEN=your_webhook_verify_token
WHATSAPP_BUSINESS_ACCOUNT_ID=your_business_account_id
BUSINESS_HOURS_TIMEZONE=Africa/Johannesburg
DEFAULT_LANGUAGE=en
NLP_MODEL_PATH=./models/za_intent_classifier
LEAD_DB_PATH=./data/leads.db
BOOKING_CALENDAR_ID=your_google_calendar_id
```

### 4. Link to wacli

```bash
# Verify wacli is available
which wacli || brew install wacli
wacli --configure
```

### 5. Set up webhooks

```bash
# Start webhook receiver (uses ngrok for dev)
./scripts/start-webhook.sh

# Register webhook with Meta
curl -X POST "https://graph.facebook.com/v18.0/$WHATSAPP_PHONE_NUMBER_ID/subscriptions" \
  -H "Authorization: Bearer $WHATSAPP_ACCESS_TOKEN" \
  -d "object=whatsapp_business_account&callback_url=https://your-ngrok-url.ngrok.io/webhook&verify_token=$WHATSAPP_VERIFY_TOKEN"
```

## Usage

### Start the assistant

```bash
# Production mode
openclaw skill run whatsapp-business-ai

# Development / dry-run
openclaw skill run whatsapp-business-ai --dry-run
```

The assistant runs as a persistent OpenClaw process that:
1. Listens for incoming WhatsApp messages via webhook
2. Classifies intent (booking, inquiry, complaint, lead)
3. Generates context-aware replies
4. Logs leads to the local database
5. Schedules follow-ups based on business rules

### Workflow Overview

```
Incoming Message → Intent Classifier → Response Generator → Send Reply
                                       ↓
                                  Booking Detected?
                                  ├── Yes → Check Calendar → Confirm Slot → Add Booking
                                  └── No  → Lead? → Log Lead → Schedule Follow-up
```

### Available Commands

| Command | Description |
|---|---|
| `/status` | Show assistant health, queue depth, message count today |
| `/leads` | Export leads as CSV or JSON |
| `/analytics` | Last 24h: sent/replied/followed-up counts |
| `/blacklist <phone>` | Block a number |
| `/broadcast` | Send bulk message to all leads (ask first) |
| `/pause` | Stop accepting new messages (resume with `/resume`) |

### Workflow Templates

**Auto-reply templates** are in `./templates/`. Customise per business type:

```
templates/
├── auto_replies/
│   ├── booking_gym.yaml
│   ├── booking_restaurant.yaml
│   ├── booking_salon.yaml
│   ├── greeting_day.yaml
│   ├── greeting_night.yaml
│   ├── hours_inquiry.yaml
│   ├── pricing_inquiry.yaml
│   ├── complaint_acknowledgement.yaml
│   └── out_of_hours.yaml
├── follow_ups/
│   ├── no_reply_24h.yaml
│   ├── abandoned_booking.yaml
│   ├── post_service_feedback.yaml
│   └── promotion_blast.yaml
└── intents.yaml
```

**Example: booking_gym.yaml**

```yaml
name: gym_booking
trigger:
  intents: [booking, tour_inquiry, membership_inquiry]
  confidence_threshold: 0.75
response:
  template: |
    Hi {{customer_name}}! 👋

    Thanks for reaching out to {{business_name}}.

    I can help you book:
    🏋️ A free trial session
    📋 A membership consultation
    🎯 A personal training intro

    What time works for you? Our hours are:
    Mon–Fri: 5:00 AM – 9:00 PM
    Sat: 6:00 AM – 6:00 PM
    Sun: 7:00 AM – 2:00 PM

    Just tell me your preferred day and time!
  buttons:
    - "Book Trial"
    - "See Pricing"
    - "Ask a Human"
```

### Prompt Configuration

Edit `./config/prompts.yaml`:

```yaml
classifier_prompt: |
  Classify the incoming WhatsApp message into exactly one intent.
  Intents: [booking, pricing_inquiry, hours, complaint, lead, general, spam]
  Context: {business_type} in {location}
  Message: {text}
  Respond with only the intent name and confidence score.

response_prompt: |
  You are {assistant_name}, the friendly AI assistant for {business_name}.
  Location: {location}
  Business type: {business_type}
  Business hours: {hours}

  Customer message: {text}
  Detected intent: {intent}

  Reply in a warm, professional tone. Be concise. If it's a booking,
  ask for time and contact info. Never give away pricing you're unsure of.
  Use South African English.
```

## Example Prompts for Human Operators

> "Hey Marvis, can you check on the gym assistant? How many unqualified leads are waiting?"
> "Set up a new WhatsApp assistant for 'Jozi Cuts Barbershop' in Randburg."
> "What's the reply rate on the restaurant assistant this week?"
> "Add a 'Student Discount' promotion template to the gym assistant's broadcast queue."

## Directory Structure

```
whatsapp-business-ai/
├── SKILL.md
├── README.md
├── config/
│   ├── business.yaml          # Business profile (name, hours, location, type)
│   ├── prompts.yaml           # LLM prompts for classification & reply
│   └── webhooks.yaml          # Webhook routing rules
├── templates/
│   ├── auto_replies/          # Pre-written reply templates
│   ├── follow_ups/            # Scheduled follow-up templates
│   └── intents.yaml           # Intent definitions & training data
├── scripts/
│   ├── start-webhook.sh       # Start webhook listener with ngrok
│   ├── register-webhook.sh    # Register with Meta APIs
│   └── export-leads.py        # Export leads to CSV
├── workflows/
│   ├── booking.yaml           # Booking: detect → confirm → create
│   ├── lead.yaml              # Lead: capture → enrich → follow-up
│   └── complaint.yaml         # Complaint: acknowledge → escalate → resolve
├── data/
│   ├── leads.db               # SQLite lead database
│   └── conversation_logs/     # Raw conversation transcripts (rotated)
├── requirements.txt
└── package.json
```

## Integration Options

- **Google Calendar** — auto-check and book appointment slots
- **Square / PayFast** — send payment links for deposits
- **CRM webhooks** — POST leads to HubSpot, Pipedrive, or custom API
- **Slack** — notify human agent when escalation needed
- **Twillio** — fallback SMS for low-signal areas

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---|---|---|
| Assistant not replying | Webhook not registered | Run `register-webhook.sh` |
| Replies go to wrong chat | Wrong phone_number_id in env | Check `.env` values |
| "Message not allowed" | Sender hasn't opted in | Send template message first |
| Low confidence on intent | Trained on wrong business type | Update `config/business.yaml` |
| Calendar sync fails | Missing Google Calendar scope | Re-auth with `https://www.googleapis.com/auth/calendar` scope |
| Leads not saving | SQLite path not writable | `chmod 755 ./data/` |
| ngrok URL changed | Free ngrok rotates on restart | Use paid plan or static IP |
