---
name: socialkit-whatsapp-templates
description: Drafts WhatsApp Business message templates (marketing, utility, authentication), validates them, and submits them to Meta for review through the official WhatsApp Cloud API after the user approves. Use when the user needs a WhatsApp template, wants to check template status or quality, or a broadcast needs a template that does not exist yet.
license: MIT
metadata:
  author: Ahmad Hussain
  platform: whatsapp
  requires: socialkit-social-core
---

# WhatsApp templates

Official Cloud API only. Setup: [setup](references/setup.md).

## Steps

1. Ask what the message is for, then pick the category honestly:
   - UTILITY: about an existing order, booking or account (shipping update, reminder)
   - MARKETING: anything promotional; Meta re-categorises promotional utility drafts
   - AUTHENTICATION: one-time passcodes only
2. Create a folder and skeleton: `node scripts/templates.mjs --init --dir wa-tpl-<name> --name <name>`
3. Edit `template.json`: body text with `{{1}}`, `{{2}}` variables in order, an example
   value for every variable, optional header, footer and buttons. Apply socialkit-social-core voice.
4. Validate: `node scripts/templates.mjs --check --dir wa-tpl-<name>` and fix every error.
5. Stop. Show the template and ask the user to run, in their own terminal:
   `node scripts/templates.mjs --approve --dir wa-tpl-<name>`
6. Submit: `node scripts/templates.mjs --submit --dir wa-tpl-<name>`
7. Check review status later: `node scripts/templates.mjs --status --name <name>`

## Output contract

`template.json`, the check report, and after submission the template id and status.

## Failure handling

- `APPROVAL_REQUIRED`: the template changed or was never approved; ask again.
- REJECTED status: show `rejected_reason`, revise, and go through approval again.
- Error 100 with subcode 2388024: a template with this name and language exists; pick a new name.
