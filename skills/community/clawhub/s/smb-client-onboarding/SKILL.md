---
name: smb-client-onboarding
version: 1.0.1
author: "NASSER AL-SOLAITTI"
description: "Local client onboarding tracker. Store client records, track onboarding steps, and generate reminder text via LLM. Use when user says 'track a new client', 'add client onboarding', 'show onboarding status', or 'onboarding checklist'.
permissions:
  - filesystem-write: write onboarding and config data to ~/.openclaw/smb-client-onboarding/
  - env: read MINIMAX_API_KEY from environment (for optional LLM reminder generation)
  - network: send client name and onboarding step context to minimax LLM API when reminder generation is used
privacy: |
  Client names, contact emails, and onboarding status are stored locally at ~/.openclaw/smb-client-onboarding/.
  When MINIMAX_API_KEY is set, client name and stuck-step context are sent to api.minimax.chat for reminder text generation.
  No emails, WhatsApp, CRM, Stripe, project boards, or Slack notifications are implemented in v1.0.
  These integrations are planned for v1.1.
---

# SMB Client Onboarding

## When to use this skill

Activate when the user wants to:
- Track onboarding progress for a new client
- Store client contact info and contract details
- Generate reminder text for stuck onboarding steps (optional LLM)
- See which client onboardings are incomplete

> **Note:** Email, WhatsApp, CRM, Stripe, Trello, Slack, and Calendly integrations
> are NOT implemented in v1.0. These are planned for v1.1.

## Prerequisites

- MINIMAX_API_KEY (optional — only needed for LLM-generated reminder text)
- OpenClaw gateway running

## Workflow

### 1. Add a client onboarding record

```bash
clawhub run smb-client-onboarding new \
  --name "Acme Corp" \
  --contact "jane@acme.com" \
  --package "Growth Consulting" \
  --contract-value 5000 \
  --start-date 2026-07-01
```

### 2. Configure required documents and reminder schedule

```bash
clawhub run smb-client-onboarding configure \
  --required-docs "NDA,BriefForm" \
  --reminder-schedule "T+1,T+3,T+7" \
  --escalate-to "team@agency.com"
```

### 3. View onboarding status

```bash
# All in-progress onboardings
clawhub run smb-client-onboarding status

# Specific client
clawhub run smb-client-onboarding status --client "Acme Corp"
```

### 4. Generate reminder text for a stuck step

```bash
clawhub run smb-client-onboarding send-reminder --client "Acme Corp" --step "NDA"
# Prints reminder text to stdout — review before sending manually
```

### 5. Skip or complete a step

```bash
clawhub run smb-client-onboarding skip-step --client "Acme Corp" --step "NDA"
```

### 6. Connect integrations (v1.1 — not yet implemented)

```bash
# These are planned for v1.1 — currently print setup instructions only
clawhub run smb-client-onboarding connect gmail
clawhub run smb-client-onboarding connect hubspot
clawhub run smb-client-onboarding connect stripe
clawhub run smb-client-onboarding connect slack
```

## Outputs

- **Onboarding records**: stored at `~/.openclaw/smb-client-onboarding/onboardings.json`
- **Reminder text**: printed to stdout (review before sending — no automated delivery in v1.0)
- **Configuration**: stored at `~/.openclaw/smb-client-onboarding/config.json`

## What v1.0 actually does

- ✅ Add and track client onboarding records
- ✅ Store client name, contact email, package, contract value, start date
- ✅ Track which onboarding steps are complete/stuck
- ✅ Configure required documents and reminder schedule
- ✅ LLM-generated reminder text for stuck steps (optional, MINIMAX_API_KEY required)
- ❌ Gmail / Outlook sending — NOT implemented (v1.1)
- ❌ WhatsApp messages — NOT implemented (v1.1)
- ❌ Stripe payment setup — NOT implemented (v1.1)
- ❌ CRM (HubSpot/Pipedrive) integration — NOT implemented (v1.1)
- ❌ Project board (Trello/Asana/Linear) creation — NOT implemented (v1.1)
- ❌ Slack team notifications — NOT implemented (v1.1)
- ❌ Calendly calendar booking — NOT implemented (v1.1)
- ❌ Telegram digest — NOT implemented (v1.1)

## Cost expectations

- LLM reminder generation: ~$0.01 per reminder (only when MINIMAX_API_KEY is set)
- OpenClaw: free, self-hosted

## Troubleshooting

**Want Gmail, WhatsApp, Stripe, CRM integrations?**
- These are planned for v1.1. Currently not implemented.

**LLM reminder not generating?**
- Verify MINIMAX_API_KEY is set in your environment

**Connect commands showing instructions but not working?**
- Email, WhatsApp, Stripe, CRM, project board, and Slack integrations are v1.1 features.
- v1.0 tracks onboarding status locally only.
