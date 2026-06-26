---
name: real-estate-lead-qualifier
version: 1.0.0
description: "High-ticket lead qualification agent for realtors and property managers. Handles inbound inquiries from Zillow/Realtor.com, qualifies for budget and timeline, and schedules viewings. Hardened with ThumbGate to prevent illegal Fair Housing hallucinations."
author: "Igor Ganapolsky"
tags: ["real-estate", "lead-gen", "high-ticket", "thumbgate", "scheduling"]
price: 297
---

# Real Estate Lead Qualifier with ThumbGate Fair-Housing Safety

## What This Agent Does
- Instantly responds to new leads from property portals 24/7.
- Qualifies leads based on Pre-Approval status, Budget, and Move-in Timeline.
- Schedules viewing appointments directly into the Realtor's calendar.
- Uses **ThumbGate** to ensure the AI NEVER answers questions that violate Fair Housing laws (e.g., "Is this a safe neighborhood?" or "What's the demographic?").

## Critical ThumbGate Rules
- **Fair Housing Block:** Immediately block and redirect any response that comments on neighborhood safety, schools, or demographics to official census/police data links.
- **Budget Floor:** Block scheduling a viewing if the lead's confirmed budget is <90% of the listing price without manual approval.
- **Pre-Approval Check:** Block booking a viewing for buyers who do not have a PDF pre-approval letter uploaded.

## Setup
1. Connect your Zillow/Realtor.com email parser.
2. Link your Google/Outlook Calendar.
3. Load skill: `openclaw skill load real-estate-lead-qualifier`
