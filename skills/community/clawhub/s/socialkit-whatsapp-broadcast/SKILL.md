---
name: socialkit-whatsapp-broadcast
description: Sends an approved WhatsApp template to opted-in contacts only through the official WhatsApp Cloud API, after showing recipients, exclusions and an estimated cost and getting the user's approval. Use when the user wants to message a list of customers on WhatsApp, send a WhatsApp campaign, announcement or bulk update.
license: MIT
metadata:
  author: Ahmad Hussain
  platform: whatsapp
  requires: socialkit-social-core socialkit-whatsapp-templates
---

# WhatsApp broadcast

Official Cloud API only. Setup: [setup](references/setup.md). Pricing file:
[pricing](references/pricing.md).

## Rules

- Only contacts with a recorded opt-in (`opt_in_at` column) are messaged. Never add an
  opt-in date the user did not record; ask instead.
- Only approved templates can be broadcast. Free-form text is not possible here.
- The user approves the exact recipient list, template and estimated cost.

## Steps

1. `node scripts/broadcast.mjs --init --dir wa-bc-<slug>`
2. Fill `broadcast.json` (template name, language, category, `bodyParams` such as
   `"{name}"` that reference contacts.csv columns) and place the user's `contacts.csv`.
3. Preview: `node scripts/broadcast.mjs --plan --dir wa-bc-<slug>`. Report recipients,
   exclusions by reason (no opt-in, opted out, duplicate, invalid, US marketing) and the
   estimated cost with the rate card date.
4. Stop. Ask the user to run in their own terminal:
   `node scripts/broadcast.mjs --approve --dir wa-bc-<slug>`
5. Send: `node scripts/broadcast.mjs --send --dir wa-bc-<slug>`. It checks the template is
   APPROVED with the same category, then sends at a safe rate. Rerunning resumes and never
   double-sends.
6. Report sent, skipped and failed counts and where `results.jsonl` is.

## Failure handling

- `WA_TEMPLATE_CATEGORY`: Meta re-categorised the template; update broadcast.json, re-plan
  (cost changes) and get a new approval.
- `stoppedBy` set: an account-level error (billing, restriction, quality). Do not retry;
  show the hint to the user.
- Skipped 131049 or 131050: per-user marketing limit or opt-out. Do not resend.
