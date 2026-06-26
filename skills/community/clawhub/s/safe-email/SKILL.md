---
name: safe-email
description: Privacy-first workflow for processing explicitly forwarded emails via IMAP in a dedicated inbox. Use only when the user explicitly asks to process the latest forwarded email. Extract structured information and return safe next-step suggestions; do not auto-read or auto-act on external systems.
metadata:
  openclaw:
    requires:
      bins: ["himalaya"]
      env:
        - SAFE_EMAIL_IMAP_USERNAME
        - SAFE_EMAIL_IMAP_APP_PASSWORD
    capabilities:
      - imap_read_latest_only
      - optional_email_delete
    compliance:
      explicitTriggerRequired: true
      autoPollingForbidden: true
      destructiveActionsNeedConsent: true
      forwardToDedicatedInboxRequired: true
---

# Safe Email (Privacy-First, Extraction-Only)

Use this skill to safely process forwarded emails from a dedicated inbox via IMAP.

This skill is **extraction-only**:
- Read newest forwarded email (when explicitly asked)
- Extract structured details
- Return suggested next actions
- Do **not** write to calendar/reminder or other external systems automatically

## What users must know first

1. Use a dedicated inbox (recommended: a brand-new Gmail account).
2. Forward target emails to that dedicated inbox before running this skill.
3. This skill does not auto-check inboxes; it runs only on explicit user instruction.

## Required secrets/config (declared in metadata)

- `SAFE_EMAIL_IMAP_USERNAME`
- `SAFE_EMAIL_IMAP_APP_PASSWORD`

Policy:
- Provide secrets through secure runtime configuration.
- Never store plaintext credentials inside the skill package.

## Security rules

1. Never auto-check email without explicit user instruction.
2. Read minimally: only newest relevant message for the request.
3. Deletion is optional and requires explicit consent.
4. Ask before ambiguous or destructive actions.

## Setup guide (Gmail + IMAP)

1. Create a dedicated Gmail account for automation.
2. Enable 2-Step Verification.
3. Generate an App Password.
4. Configure IMAP client (example: Himalaya):
   - IMAP: `imap.gmail.com:993` (TLS)
   - SMTP (optional if sending needed elsewhere): `smtp.gmail.com:587` (STARTTLS)

## Execution workflow

### Step 0 — Require explicit trigger

Proceed only if user explicitly asks, e.g.:
- "I forwarded an email, process it."
- "Read the latest forwarded email."

Otherwise, stop.

### Step 1 — Read newest relevant email only

- List recent inbox messages.
- Open only the newest relevant candidate.
- Do not bulk-read old/unrelated messages.

### Step 2 — Extract structured details

Extract as available:
- sender
- subject/title
- date/time window (and timezone if present)
- location
- links
- key notes (confirmation numbers, seats, participants, etc.)
- actionable items

If time/timezone is ambiguous, ask user for confirmation.

### Step 3 — Return extraction + suggested next actions

Return:
1. Structured summary
2. Confidence/ambiguities
3. Suggested next actions (examples):
   - "Create a calendar event"
   - "Create a reminder/task"
   - "Draft a reply"
   - "Archive/delete email"

Do not execute those actions unless user explicitly asks.

### Step 4 — Optional email deletion (consent required)

If and only if user explicitly requests deletion:
1. Move processed email to Trash
2. Permanently expunge when supported
3. Report deletion status

If not requested, leave email untouched and state so clearly.

## Failure handling

- If parsing fails: provide partial extraction + clarification questions.
- If deletion fails: report exact status and ask whether to retry.

## Default privacy posture

- Explicit trigger only
- Minimal access scope
- No background surveillance behavior
- No automatic downstream writes
- Optional deletion with explicit consent
