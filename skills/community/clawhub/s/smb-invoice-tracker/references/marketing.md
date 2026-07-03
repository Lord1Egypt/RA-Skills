# Marketing copy (for skill marketplace listing)

---

## Short tagline

Local invoice tracking ledger with optional LLM reminder generation. No Gmail, no WhatsApp, no Stripe — just you and your data.

## Long description

A simple invoice tracker for freelancers and small businesses. Add invoices, track who owes you, and generate polite reminder text via LLM — all stored locally on your machine.

**What's actually in v1.0:**
- Manual invoice entry (payer, amount, due date, note)
- Outstanding / paid status tracking
- Cash flow report
- LLM-generated reminder text (optional, requires MINIMAX_API_KEY)

**What's NOT in v1.0 (coming in v1.1):**
- Gmail invoice scanning
- Automated WhatsApp or email reminders
- Stripe payment detection
- Telegram digest

## Privacy

- All data stored locally at `~/.openclaw/smb-invoice-tracker/`
- No data sent to third parties except api.minimax.chat (when MINIMAX_API_KEY is set for reminder generation)
- No Gmail access, no WhatsApp, no Stripe in v1.0

## License

MIT
