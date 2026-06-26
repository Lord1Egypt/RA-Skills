---
name: strategy-awal
description: OpenClaw MVP v8.1 — Email Classification & Google Workspace Execution for Awalcom.
metadata:
  {
    "openclaw": {
      "emoji": "🦅",
      "requires": { "bins": ["gog", "gh"] }
    }
  }
---

# Strategy Awal

This skill monitors `strategy@awalcom.net`, classifies incoming emails by region (Oman, Qatar, MENA), and executes approved actions via Google Docs, Sheets, and Slides.

## Core Capabilities

1. **Email Monitoring:** Uses `gog` CLI to poll the `strategy@awalcom.net` inbox for unread messages.
2. **Contextual Classification:** Automatically categorizes emails based on internal strategy keywords (Oman, Qatar, MENA) stored in `context/email-classification-keywords.json`.
3. **Approval Workflow:** Pushes a summary to Telegram and waits for the Chairman's approval before executing actions.
4. **Google Workspace Automation:** Upon approval, autonomously drafts Google Docs, creates Google Slides, or sets up Google Sheets based on the email context.

## Prerequisites

- `gog` configured and authenticated via OAuth with scopes for `gmail`, `docs`, `drive`, `sheets`.
- Telegram integration enabled on OpenClaw.

## Workflow Commands

- `/check` — Check for unread emails immediately and present a classification summary.
- `/classify [region]` — List processed emails mapped to a specific region (e.g., Oman).
- Custom Natural Language — Provide instructions directly against the email context (e.g., "Draft a response in Google Docs").

## Regional Keywords
The classification engine uses a weighted heuristic based on the Awalcom strategy:
- **Oman:** ARISE, hydrogen, SSEZ, Duqm, Vision 2040.
- **Qatar:** QNDS, climate awareness, climate action.
- **MENA:** Regional initiatives, IsDB, Arab Fund.

See `docs/approval-workflow.md` and `docs/telegram-commands.md` in the repository for full deployment guides and troubleshooting steps.
