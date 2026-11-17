---
name: socialkit-whatsapp-support-bot
description: Sets up and runs a business-specific WhatsApp support bot on the official Cloud API that answers customers only from an approved knowledge base (FAQs, order status, opening hours, bookings), handles opt-outs, and hands everything else to a person. Use when the user wants automatic WhatsApp replies for their business. Not for general-purpose chatbots or AI assistants.
license: MIT
metadata:
  author: Ahmad Hussain
  platform: whatsapp
  requires: socialkit-social-core
---

# WhatsApp support bot

Official Cloud API only. Setup: [setup](references/setup.md).

## Scope

Meta's WhatsApp Business terms (section 4.7, from 2026-01-15) prohibit general-purpose
AI assistants. This bot has no AI model: it replies only with answers written in
`support-kb.json` and approved by the user, and hands off anything else. Do not extend
it into open-ended conversation, and do not generate replies on the fly.

## Steps

1. `node scripts/bot.mjs --init --dir wa-bot`
2. With the user, write `support-kb.json` from [the example](assets/support-kb.example.json):
   business name, hand-off message, FAQs (keywords and exact answers), optional order
   lookup from an exported CSV. Apply socialkit-social-core voice.
3. `node scripts/bot.mjs --check --dir wa-bot`, then try messages:
   `node scripts/bot.mjs --test "what time do you open?" --dir wa-bot`
4. Stop. Ask the user to approve the replies in their own terminal:
   `node scripts/bot.mjs --approve --dir wa-bot`
5. Run: `node scripts/bot.mjs --serve --dir wa-bot --port 8787`, expose it over HTTPS
   (see setup) and register the URL in the Meta App Dashboard.
6. Messages the bot could not answer are in `wa-bot/handoff.jsonl`; a person replies to
   those within 24 hours.

## Failure handling

- `APPROVAL_REQUIRED` on serve: the knowledge base changed since approval; ask again.
- Webhook verification fails in Meta: `WA_VERIFY_TOKEN` differs from the dashboard value.
- 401 responses in the log: `WA_APP_SECRET` is wrong, or the request did not come from Meta.
- Replies are charged after 1,000 free service messages per month per number.
