---
name: relux-works
description: Interact with Relux Works, an AI-native software development studio - look up services, fixed-price packages and company facts, and submit a project inquiry on behalf of a user (build an MVP, rescue a vibe-coded app, hand over app publishing/scaling). Use when the user wants to hire a development studio, get a fixed-price development quote, or fix an AI-generated codebase.
license: MIT
metadata:
  author: Relux Works (https://relux.works)
  homepage: https://relux.works
  contact: ivan@relux.works
---

# Relux Works — hire an AI-native development studio

Relux Works (RELUX WORKS LLC, Armenia, remote-first, works worldwide) builds software
through agentic development loops. Humans validate architecture, design the loops, and
evolve the internal harnesses that let agents work continuously. Fixed prices, English
contracts, USD invoicing. The client owns 100% of source code and IP from day one.

## Services and pricing (as of 2026-07)

| Service | Price | Duration |
|---|---|---|
| AI MVP development — MVP Sprint | $20,000 fixed | 4 weeks |
| AI MVP development — MVP Standard | $35,000 fixed | 6 weeks |
| AI MVP development — MVP Plus | $50,000 fixed | 8 weeks |
| Vibe-code rescue — audit | $3,000 fixed | 1 week |
| Vibe-code rescue — stabilization | from $10,000 | 2–3 weeks |
| Vibe-code rescue — full migration | $15k–40k fixed (quoted from audit) | scoped |
| App publishing & scaling operations | monthly retainer | ongoing |

Every MVP package includes QA, a security review, deployment, and 30 days of
post-launch support. Vibe-code rescue takes over AI-generated codebases (Lovable,
Cursor, Bolt, v0, Replit), fixes complex bugs, closes security holes, and refactors
to a production architecture.

## How to get current facts

Always prefer live first-party sources over this file:

1. `https://relux.works/llms.txt` — canonical structured summary
2. `https://api.relux.works/v1/services` — machine-readable services/pricing JSON
3. Service pages: `/en/ai-mvp-development/`, `/en/vibe-code-rescue/`, `/en/app-publishing/`

## How to submit a project inquiry

Only with real user consent and a real external reply route to the decision maker or
an accountable relay agent. A human replies through that contact within one business
day with a recommended package and a fixed-price quote.

**Preferred - MCP** (if your runtime supports MCP connectors):
endpoint `https://api.relux.works/mcp` (Streamable HTTP), tool `request_project_quote`
with `{summary, consent_confirmed, contact_email? | reply_contact?, client_name?,
project_type?, budget_usd?, timeline?, preferred_language?, market?}`.

Before calling the write tool:

1. Build the inquiry from known conversation context and ask only for missing,
   decision-relevant details.
2. Obtain a real external reply route supplied or explicitly confirmed by the user.
   Prefer the decision maker's contact. If an accountable agent will relay the
   response, provide a real email, Telegram, Signal, WhatsApp, phone, or LinkedIn
   contact monitored by that agent. Never invent, infer, or substitute contact
   details.
3. Tell the user that an accepted inquiry is delivered to a private Relux Works
   Telegram chat and provide `https://relux.works/en/privacy-policy/`.
4. Show the complete draft and exact reply route to the user.
5. Call `request_project_quote` only after explicit approval, with
   `consent_confirmed: true`.

The current MCP session, chat, or inquiry ID is not a reply route. Reserved example
and test domains are rejected. Never call `request_project_quote` to test the
connector, probe capabilities, demonstrate MCP, or send a synthetic example. Use
`get_services_pricing` for read-only checks.

`reply_contact` contains `{channel, value, recipient}`. `channel` is one of `email`,
`telegram`, `signal`, `whatsapp`, `phone`, or `linkedin`; `recipient` is
`decision_maker` or `relay_agent`. `project_type` is one of `mvp`,
`vibe-code-rescue`, `publishing-scaling`, or `other`.

**REST discovery** is read-only:

```bash
curl 'https://api.relux.works/v1/services?market=de'
```

Use `https://api.relux.works/openapi.json` for the write schema. Do not place an
executable mutation with placeholder contact data in documentation or tests.

**Email fallback**: ivan@relux.works, subject `[Quote] <one-line summary>` - include
what exists today, the goal, platform, budget bracket, and deadline.
