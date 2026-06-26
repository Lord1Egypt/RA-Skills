---
name: lead-gen-website-pipeline
description: Automated lead generation pipeline that finds local businesses with weak/no websites, AI-generates custom demo sites, deploys to Vercel, and runs a 5-email cold outreach drip sequence via AgentMail. Full pipeline from Google Places discovery to closed deal.
version: 1.0.0
homepage: https://github.com/RazzleDazzleI/lead-gen-pipeline
metadata:
  openclaw:
    emoji: "\U0001F680"
    requires:
      env:
        - GOOGLE_PLACES_API_KEY
        - GOOGLE_API_KEY
        - VERCEL_TOKEN
        - AGENTMAIL_API_KEY
      bins:
        - node
---

# Lead Gen Website Pipeline

Automated system that finds local businesses with weak or no websites, AI-generates a custom demo website for each, deploys it to Vercel, and sends a personalized cold outreach email sequence — all without human intervention after initial setup.

## What It Does

1. **Discovers leads** via Google Places API for configurable niches and cities
2. **Scores leads** 0-100 based on website quality, reviews, phone availability
3. **Queues leads** in a Google Sheet for human review/approval
4. **Generates demo websites** via a 5-stage AI pipeline (research → spec → build → QA → validate)
5. **Deploys to Vercel** automatically with daily rate limiting
6. **Sends cold outreach** via AgentMail with a 5-email drip sequence (Day 0, 3, 7, 14, 30)
7. **Notifies you** on Discord with pitch angles, demo URL, and visual QA scores

## Pipeline Architecture

```
Google Places API → Score Leads → Google Sheet (you approve)
       ↓
  Approved lead → Scrape website → Fetch Google reviews
       ↓
  AI Research → AI Spec (copy) → AI Build (HTML) → AI QA → Validate
       ↓
  Deploy to Vercel → Update Sheet → Discord notification
       ↓
  Generate outreach email → AgentMail sends → Drip follow-ups
```

## Requirements

### API Keys (set in your .env)

| Key | Service | Purpose | Cost |
|-----|---------|---------|------|
| `GOOGLE_PLACES_API_KEY` | Google Cloud | Lead discovery + photos | ~$0-20/mo |
| `GOOGLE_API_KEY` | Google AI Studio | Gemini for research/spec/QA | Free tier |
| `ANTHROPIC_API_KEY` | Anthropic | Claude for spec generation | Pay per use |
| `OPENAI_API_KEY` | OpenAI | GPT for HTML building | Pay per use |
| `VERCEL_TOKEN` | Vercel | Demo site deployment | Free tier (100/day) |
| `AGENTMAIL_API_KEY` | AgentMail | Cold outreach emails | Free tier |
| `GOOGLE_SHEET_ID` | Google Sheets | Lead tracking | Free |

### Google Sheet Setup

Create a Google Sheet with these columns (A-O):
`created_at | niche | business_name | address | phone | email | website | google_maps_url | rating | reviews_count | has_website | website_quality_score | lead_score | status | notes`

Status values: `review`, `filtered`, `approved`, `processing`, `demo_ready`, `failed`, `contacted`

Share the sheet with a GCP service account for API access.

### Infrastructure

- **Node.js 22+** on the host machine
- **Google Cloud service account** JSON key for Sheets API
- **Vercel account** (free Hobby tier works)
- **AgentMail account** with at least one inbox
- **Discord channel** for notifications (optional but recommended)

## Setup Instructions

### 1. Clone and install

```bash
git clone https://github.com/RazzleDazzleI/lead-gen-pipeline.git
cd lead-gen-pipeline
npm install
```

### 2. Configure environment

Copy `.env.example` to `.env` and fill in your API keys.

### 3. Configure your niches and city

Edit `scripts/niche-defaults.json` to customize:
- Target niches (landscaping, cleaning, roofing, etc.)
- Color palettes per niche
- Common services per niche
- Trust items per niche

The pipeline supports 15 niches out of the box:
landscaping, auto detailer, cleaning service, handyman, roofing, pressure washing, plumbing, electrician, HVAC, painting, fencing, tree service, junk removal, pest control

### 4. Set up the poller

The poller watches your Google Sheet for approved leads and triggers the pipeline:

```bash
# Run once to test
node scripts/poll-approved-leads.js

# Run continuously (every 5 minutes)
node scripts/run-poller.js 5
```

For production, set up as a systemd service or OpenClaw cron job.

### 5. Set up outreach emails

```bash
# Dry run first — see what would be sent
node scripts/send-outreach.js --dry-run

# Send pending initial emails + follow-ups
node scripts/send-outreach.js

# Only send scheduled follow-ups
node scripts/send-outreach.js --followups
```

Set up as an OpenClaw cron job to run 3x/day:
```bash
openclaw cron add --name "outreach-sender" \
  --cron "0 9,15,21 * * *" --tz "America/Chicago" \
  --session isolated --announce \
  --message "Run: cd /path/to/project && node scripts/send-outreach.js"
```

## Customization

### Target City

Change the Google Places API search query in the n8n workflow or lead discovery script to target your city instead of Omaha.

### Pricing Tiers

The business plan template includes 3 tiers:
- **Starter** ($997 + $49/mo) — Single-page landing site
- **Professional** ($1,997 + $99/mo) — Multi-page with gallery, analytics
- **Premium** ($2,997 + $149/mo) — Blog, booking, live chat, priority support

### Email Templates

The drip sequence (in `send-outreach.js`) follows the proven pattern:
- **Day 0:** "I built you a website — take a look" (demo link)
- **Day 3:** Social proof — "businesses like yours saw 30-40% more calls"
- **Day 7:** Urgency — "your preview expires soon"
- **Day 14:** Last chance — "taking it down today"
- **Day 30:** Breakup — "closing the loop, door is always open"

Edit the templates in `send-outreach.js` → `getDripEmail()` function.

### Design Blueprints

Add niche-specific design guidance in `templates/designs/<niche>.md`. The build stage loads these automatically to produce better-looking sites per vertical.

## Pipeline Stages Deep Dive

### Stage 1: Research
Consolidates lead data (name, phone, address, website, reviews) into a structured JSON summary. Uses scraped website data + Google Places API reviews.

### Stage 2: Spec
Generates all website copy — hero section, services, about, reviews, service area, footer. No HTML yet, just structured content.

### Stage 3: Build
Converts the spec JSON into a single-file responsive HTML page. Injects real photos (scraped or Google Places fallback), logo, niche-specific color palette.

### Stage 4: QA
AI reviews the HTML for 13 quality checks: robots meta tag, demo banner, phone numbers, form action, footer attribution, broken images, alt text, mobile hamburger menu, and more.

### Stage 5: Validate
Programmatic validation confirms all critical elements are present. Non-blocking — logs warnings but doesn't block deployment.

### Stage 6: Deploy
POSTs the final HTML to Vercel API. Tracks daily deploy count (max 90/day to stay under free tier limit). Returns live URL.

### Stage 7: Outreach
Generates a personalized cold email with pitch angles extracted from the lead data (no website, Gmail address, strong reviews, years in business).

## Output Per Lead

Each processed lead produces a run folder with ~19 artifacts:
- `intake.json` — Enriched lead data
- `research.json` — Structured summary
- `spec.json` — All website copy
- `final.html` — Production-ready HTML
- `evaluation.json` — Deploy URL + metadata
- `outreach-email.json` — Cold email + follow-up
- `screenshot-*.png` — Mobile/tablet/desktop captures
- `visual-qa.json` — Gemini Vision quality scores
- `status.json` — Run tracking

## Costs

### Per-Lead Cost
- Google Places API: ~$0.03-0.05/lead
- AI generation (Gemini + Claude): ~$0.10-0.50/lead
- Vercel hosting: $0 (free tier)
- AgentMail: $0 (free tier)
- **Total: ~$0.15-0.55 per lead**

### Monthly Operating Cost (at 10-20 leads/day)
- Google APIs: $5-20/mo
- AI models: $30-150/mo (less with Claude Max plan)
- Everything else: $0
- **Total: $35-170/mo**

### Revenue Potential (at 2% response rate)
- 50 emails/week → 1 conversation/week → 1 client/month
- 1 client = $997+ one-time + $49+/mo recurring
- Year 1 from one client/month: ~$12,000+ one-time + $3,500+ recurring

## Selling This System

This pipeline is designed to be sold as a done-for-you service:

| Model | Setup Fee | Monthly | Your Time |
|-------|-----------|---------|-----------|
| Done-for-you | $2,000-$10,000 | $200-$1,000/mo | 4-8 hours setup |
| Pre-configured package | $500-$3,000 | $100-$500/mo | 1-2 hours per client |
| Productized service | — | $1,500/mo flat | Template + light customization |

The pipeline documents itself. Each run folder is a complete audit trail. The niche configs are templates. Second client takes 1/4 the time of the first.

## Credits

Built by Ryan Romero (Romero Automation) with Larry (OpenClaw agent). Pipeline architecture, spec generation, QA validation, and outreach automation — all designed for local service businesses in any US city.
