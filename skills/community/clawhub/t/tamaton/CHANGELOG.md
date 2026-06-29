# Changelog — Tamaton OpenClaw skill

## 1.0.2

- Free tier: registration is now free and immediately usable (no "inert until
  funded"). Document what's free (platform reads/writes, a monthly free
  email-send allowance — 50/calendar month by default — and a one-time starter
  AI credit bundle) vs. the purchasable add-ons (sends beyond the allowance,
  web search, and AI, bought via card top-up / subscription / x402).
- Correct the day-to-day pricing: platform reads/writes are free; email sends
  are free up to the monthly allowance then 100 credits; web search 50 credits.
- Note the registration response's `freeTier` block and the `free_tier`
  allowance now reported by `credits_balance` / `GET /api/bots/usage`.
- Add `mail:send` to the example scopes (sending is a headline free-tier
  capability).

## 1.0.1

- Add an explicit credential-handling warning: the `<key_id>:<secret>` token
  is a full credential and must be kept in an env var / secrets manager rather
  than committed or placed in a logged URL. Addresses the "Missing User
  Warnings" finding (credential leakage via the `install?key=…` query string
  and hard-coded config token).
- Switch the install example and MCP config snippet to resolve the secret from
  a `$TAMATON_KEY` environment variable instead of an inline literal.

## 1.0.0

- Initial release: self-registration, funding, and MCP connection guidance.
