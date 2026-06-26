# OpenClaw MVP v8.1 — Email Classification & Google Workspace Execution

## System Overview
This repository contains the configuration and context for the OpenClaw MVP v8.1. The system is designed to securely monitor the `strategy@awalcom.net` inbox, classify incoming communications by region, and automatically prepare actionable drafts in Google Workspace pending human approval.

## The Core Loop
1. **Check Email:** OpenClaw polls `strategy@awalcom.net` for unread messages.
2. **Classify:** Messages are categorized by region (Oman, Qatar, MENA) based on keyword heuristics.
3. **Summarize:** A briefing card is pushed to the Telegram channel.
4. **Wait for Approval:** The system pauses until the Chairman (user) approves an action.
5. **Execute:** OpenClaw executes the approved action using Google Workspace APIs (Docs, Sheets, Slides) and returns the asset link.

## Regional Definitions
- **Oman:** Focus on ARISE, hydrogen, SSEZ, Duqm, Vision 2040.
- **Qatar:** Focus on climate awareness, QNDS, climate action.
- **MENA:** Focus on cross-regional initiatives, IsDB, GCC.

## Core Actions (Post-Approval)
- **Draft Doc:** Generate a Google Doc response, brief, or proposal.
- **Create Slides:** Generate a presentation outline or slide deck via Google Slides/Marp.
- **Create Sheet:** Generate a data model, tracking sheet, or financial model in Google Sheets.

## Phase 2 (Deferred)
- Automated external email sending (currently blocked by policy / requires explicit human execution).
- Direct NotebookLM API integration (pending Google API availability).
- Canva API asset generation.