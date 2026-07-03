# Marketing copy (for skill marketplace listing)

---

## Short tagline

Local client onboarding tracker. Store records, track steps, generate reminder text. No Gmail, no CRM, no Slack — just local tracking.

## Long description

A local client onboarding tracker. Store client info, track onboarding steps, and generate reminder text via LLM — all stored on your machine.

**What's actually in v1.0:**
- Client onboarding record storage (name, contact, package, contract value, start date)
- Step tracking (NDA, brief, kickoff, etc.)
- Reminder schedule configuration
- LLM-generated reminder text for stuck steps (optional, MINIMAX_API_KEY required)

**What's NOT in v1.0 (coming in v1.1):**
- Automated welcome emails (Gmail/Outlook/SendGrid)
- WhatsApp onboarding messages
- Stripe payment setup
- CRM integration (HubSpot, Pipedrive)
- Project board creation (Trello, Asana, Linear)
- Slack team notifications
- Calendly calendar booking
- Telegram digest

## Privacy

- All data stored locally at `~/.openclaw/smb-client-onboarding/`
- No data sent to third parties except api.minimax.chat (when MINIMAX_API_KEY is set)
- No email, CRM, payment, or messaging integrations in v1.0

## License

MIT
