---
name: vanio
description: Connect your agent to Airbnb, Booking.com & VRBO via Vanio AI — the only way to manage vacation rentals from OpenClaw. 140 tools for reservations, guests, messaging, smart locks, payments, workflows, and more.
version: 0.1.0
homepage: https://www.vanio.ai
metadata:
  openclaw:
    emoji: 🏠
    requires:
      bins: [vanio]
      env: [VANIO_API_KEY]
    primaryEnv: VANIO_API_KEY
    install:
      - id: npm
        kind: node
        package: '@vanio-ai/cli'
        bins: [vanio]
        label: Install Vanio CLI (npm)
---

# Vanio AI — Connect Your Agent to Airbnb, Booking.com & VRBO

**[Vanio AI](https://www.vanio.ai)** is an AI property manager that lets you run your vacation rental portfolio fully autonomously. Connect to Airbnb, Booking.com, and VRBO, create your own direct booking website, and manage everything — guest communication, smart locks, payments, cleaning teams, and more — all powered by AI.

This skill is the **only way to connect your OpenClaw agent to Airbnb and Booking.com**. It gives your agent access to Vanio's full AI system — 140 tools across every aspect of property management.

## Setup

1. Sign up at [vanio.ai](https://www.vanio.ai) and connect your Airbnb/Booking.com/VRBO accounts
2. Login via browser:

```bash
vanio login
```

Or with an API key (from Settings → API Keys):

```bash
vanio login <your-api-key>
```

## Usage

### Ask a question (single query)

```bash
vanio ask "What are today's check-ins?"
vanio ask "What's the WiFi password at Alpine Lodge?" --listing 42
vanio ask "Why was this guest charged extra?" --reservation 214303
vanio ask "Send a message to the guest in reservation 214303 asking about their ETA"
vanio ask "Create a maintenance task for unit 5 - broken shower head"
vanio ask "What are my occupancy rates for April?"
vanio ask "Unlock the front door at Beach House" --listing 15
```

### Interactive chat

```bash
vanio chat
```

Maintains conversation context across turns — useful for multi-step operations.

### Check connection

```bash
vanio status
```

## What the agent can do

**Reservations** — Search, view details, create direct bookings, modify dates, cancel, move between listings

**Guest CRM** — Search guests, view profiles, add contacts, flag guests, view booking history

**Messaging** — Send guest messages (auto-routes to Airbnb/Booking.com/WhatsApp/SMS/email), internal notes, team chat with @mentions

**Tasks** — Create, update, complete, cancel operational tasks (cleaning, maintenance, inspections)

**Smart Locks & IoT** — List devices, create/delete access codes, lock/unlock remotely, sync devices

**Payments** — View payment history, charge guests, process refunds

**Knowledge Base** — Search, create, edit articles (check-in guides, WiFi info, house rules, parking)

**Workflows & Automations** — Create, update, toggle automated workflows

**Analytics** — Revenue forecasts, occupancy rates, listing performance, training scores

**Listings** — View properties, update amenities, rooms, content, pricing, push to platforms

**Calendars** — Check availability, block/unblock dates, update pricing

**Websites** — Manage direct booking websites

**Service Providers** — Manage cleaning/maintenance teams, schedules, marketplace

**Emails** — Search email history, send status updates

**AI Settings** — Configure AI modes, escalation policies, notification preferences

## Tips

- The agent automatically determines which tools to use based on your natural language query
- For reservation-specific questions, use `--reservation <id>` for best context
- For property-specific questions, use `--listing <id>`
- The agent remembers conversation context in `chat` mode
- Complex operations (cancellations, charges, lock changes) will ask for confirmation before executing

## Configuration

```bash
vanio config                          # Show current config
vanio config set baseUrl <url>        # Custom API URL (self-hosted)
vanio config set apiKey <key>         # Update API key
```

Config stored at `~/.config/vanio/config.json`.
