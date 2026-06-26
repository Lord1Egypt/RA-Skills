# Approval Workflow

The system is designed around a "Human-in-the-Loop" architecture. OpenClaw cannot execute external actions (like sending an email or sharing a document publicly) without explicit approval.

## Step-by-Step Flow

**Step 1:** OpenClaw reads an incoming email from `strategy@awalcom.net` (triggered manually via `/check`).
**Step 2:** The system analyzes the email text against `context/email-classification-keywords.json` to assign a region (Oman, Qatar, MENA).
**Step 3:** OpenClaw sends a summary card to the Telegram chat, listing the sender, subject, classification, and suggested actions.
**Step 4:** The system pauses and waits for the Chairman (user) to approve an action or provide a custom directive.
**Step 5:** Upon approval, OpenClaw executes the action using Google Workspace APIs (e.g., creating a draft in Google Docs).
**Step 6:** OpenClaw shares the link to the generated asset in Telegram and waits for final approval before taking any further steps (like finalizing or closing the loop).