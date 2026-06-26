# WhatsApp Business AI Assistant 🤖💬

**Market-ready AI assistant that runs your WhatsApp business conversations on autopilot.**

## What It Does

Stop losing customers to slow replies. The WhatsApp Business AI Assistant automatically handles incoming messages on WhatsApp — understanding intent, replying in seconds, capturing leads, and booking appointments. It works across gyms, restaurants, salons, clinics, and any local service business.

## Why Buy This

- **Never miss a lead** — responds within 5 seconds, 24/7, including weekends and holidays
- **Cuts headcount** — one assistant handles what 3+ admin staff do
- **Proven templates** — pre-built for 10 business categories, optimised for SA small businesses
- **Lead machine** — every conversation is scored, logged, and followed up automatically
- **Dead simple** — point it at your WhatsApp Business number, fill in your business profile, go live

## Key Features

| Feature | Details |
|---|---|
| 🧠 **Smart Intent Recognition** | Detects booking, pricing, hours, complaints, leads — even SA slang |
| 📅 **Auto-Booking** | Checks Google Calendar, proposes slots, confirms appointments |
| 📋 **Lead Capture** | Logs name, number, interest, follow-up date to built-in CRM |
| 🔁 **Smart Follow-ups** | Abandoned booking? No reply in 24h? Auto-sends nudge templates |
| 🏪 **Multi-Business Ready** | Run separate assistants for gym, salon, restaurant — all from one install |
| 🇿🇦 **SA-Tuned** | Hours, pricing, greetings, and tone adapted for South African audiences |
| 🔌 **Plugs Into Anything** | Square, PayFast, HubSpot, Slack, Google Calendar — webhooks out of the box |
| 📊 **Dashboard** | Check reply rate, lead volume, conversion stats via `/analytics` |

## What's Included

- 20+ ready-to-use reply templates across 10 business types
- Intent classifier pre-trained on SA WhatsApp conversations
- SQLite lead database with export to CSV/JSON
- Google Calendar booking integration
- Escalation workflow — hands off to a human when needed
- One-command deployment (`openclaw skill run whatsapp-business-ai`)

## Use Cases

**💪 Gym** — Book trial sessions, answer membership pricing, capture fitness goals
**🍽️ Restaurant** — Handle reservations, dietary questions, special event inquiries
**💇 Salon** — Book appointments, list services, accept cancellations and reschedules
**🏥 Clinic** — Schedule appointments, send reminders, handle prescription refill requests
**🔧 Service Business** — Quote requests, scheduling, job status updates

## Requirements

- OpenClaw v2.4+
- Meta WhatsApp Business API account (free to set up)
- 15 minutes to configure

## Quick Start

```bash
# Install
openclaw skill install whatsapp-business-ai

# Configure business profile
nano config/business.yaml

# Launch
openclaw skill run whatsapp-business-ai --dry-run   # test first
openclaw skill run whatsapp-business-ai              # go live
```

## License

Commercial license included. Deploy on unlimited business numbers.

---

**Made for South African businesses that want to grow without burning out their staff.** 🇿🇦
