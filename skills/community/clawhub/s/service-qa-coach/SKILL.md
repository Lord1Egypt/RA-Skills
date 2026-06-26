---
name: service-qa-coach
description: Review support quality for chat, email, phone, social DM, or marketplace service teams. Use when a team needs a QA scorecard, failure-mode analysis, coaching plan, calibration checklist, or service-improvement brief without live ticketing, CRM, or contact-center system access.
---

# Service QA Coach

## Overview

Use this skill to turn support quality concerns into a structured QA and coaching brief. It helps define the scorecard, isolate likely failure modes, recommend coaching actions, and organize a sampling and calibration rhythm.

This MVP is heuristic. It does **not** connect to live ticketing systems, call recordings, chat exports, CRMs, or QA platforms. It relies on the user's provided support notes, issue patterns, and service expectations.

## Trigger

Use this skill when the user wants to:
- audit customer service quality across chat, email, phone, social DM, or marketplace tickets
- build or refine a QA rubric for support teams
- diagnose recurring service failures such as poor empathy, policy errors, or weak resolution quality
- create a coaching plan for agents, team leads, or new hires
- run a calibration sprint before changing SOPs or scorecards

### Example prompts

- "Help me build a QA scorecard for our live chat team"
- "Why are refund escalations rising in customer service?"
- "Create a coaching plan for agents with low empathy and policy accuracy"
- "Turn these support issues into a QA and calibration brief"

## Workflow

1. Capture the support channel, review mode, and quality concern.
2. Choose the focus areas such as compliance, empathy, resolution, speed, or documentation.
3. Identify the likely failure modes and coaching priorities.
4. Define sampling, calibration, and follow-up rhythm.
5. Return a markdown QA coaching brief.

## Inputs

The user can provide any mix of:
- support channel such as chat, email, phone, social DM, or marketplace tickets
- quality goals such as CSAT recovery, policy compliance, or escalation reduction
- issue notes such as slow responses, low empathy, incorrect policy answers, or poor note-taking
- team context such as new hires, macro usage, QA backlog, or uneven supervisor coaching
- sample size, review cadence, and escalation process assumptions

## Outputs

Return a markdown QA coaching brief with:
- QA summary
- scorecard rubric
- failure mode review
- coaching plan
- calibration and sampling guidance
- assumptions and limits

## Safety

- Do not claim access to live tickets, recordings, or customer records.
- Do not invent agent-level performance facts that were not supplied.
- Privacy, compliance, refund, and disciplinary decisions remain human-approved.
- Reduce certainty when the sample is tiny or anecdotal.

## Best-fit Scenarios

- service teams that need a lighter QA framework before investing in tooling
- ecommerce operators managing outsourced or mixed support teams
- managers trying to reduce escalations, refunds, or poor customer sentiment

## Not Ideal For

- live contact-center monitoring or real-time QA enforcement
- regulated complaint handling that requires legal or compliance review
- detailed workforce management or call-center forecasting

## Acceptance Criteria

- Return markdown text.
- Include rubric, coaching, calibration, and limits sections.
- Keep the no-live-data framing explicit.
- Make the output practical for team leads and support managers.
