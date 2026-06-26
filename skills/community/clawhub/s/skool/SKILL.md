---
name: Skool
slug: skool
version: 1.0.0
homepage: https://clawic.com/skills/skool
description: Operate Skool communities with onboarding, classroom planning, calendar cadence, official automations, and safer member lifecycle workflows.
changelog: Initial release with community operations, classroom and calendar workflows, official automation guidance, and member lifecycle controls.
metadata: {"clawdbot":{"emoji":"SK","requires":{"bins":[],"config":["~/skool/"]},"os":["linux","darwin","win32"],"configPaths":["~/skool/"]}}
---

## When to Use

User needs help running Skool as a real operating system, not just writing generic community advice.
Agent handles group positioning, approvals, onboarding, classroom access, calendar cadence, official automation surfaces, and member lifecycle decisions without inventing unsupported platform behavior.

## Architecture

Memory lives in `~/skool/`. If `~/skool/` does not exist, run `setup.md`. See `memory-template.md` for structure.

```text
~/skool/
|-- memory.md        # Durable activation rules, group profile, and operating defaults
|-- groups.md        # Group URLs, offer structure, and positioning notes
|-- onboarding.md    # Membership questions, approval policy, and welcome flow decisions
|-- classroom.md     # Course access logic, unlock rules, and lesson design notes
|-- automations.md   # Approved Zapier, AutoDM, and webhook workflows
`-- incidents.md     # Spam, access mistakes, broken invites, and recovery notes
```

## Quick Reference

Load only the smallest file that matches the current Skool blocker.

| Topic | File |
|-------|------|
| Setup and activation behavior | `setup.md` |
| Memory template | `memory-template.md` |
| Official product surface and hard constraints | `official-surface.md` |
| Group strategy and day-to-day operations | `community-operations.md` |
| Classroom structure and calendar execution | `classroom-and-calendar.md` |
| Official automations, Zapier, and webhook flows | `automation-and-integrations.md` |
| Approvals, onboarding, retention, and member lifecycle | `member-lifecycle.md` |
| Failure diagnosis and rollback moves | `troubleshooting.md` |

## Requirements

- Skool group admin access, screenshots, exports, or concrete context if the user wants execution advice instead of generic strategy
- Official Skool integration credentials only when the user is wiring a verified automation surface that explicitly requires them
- Explicit user confirmation before live invites, member removal, access changes, DM automation, billing-adjacent changes, or any write that affects real members
- Current plan gates, plugin availability, and exact platform behavior must be re-checked against official Skool docs when the task depends on a specific feature

## Operating Coverage

This skill covers the real Skool operating stack:
- group promise, offer shape, public versus private posture, and approval policy
- membership questions, instant approval choices, AutoDM follow-through, and invite handling
- classroom structure, lesson sequencing, course access rules, and calendar-driven retention
- official automation surfaces such as Zapier and the developer-only webhook plugin
- moderation, spam reduction, member support, and recurring failure recovery

This skill does not assume an official Skool CLI exists. Treat Skool as a product with UI workflows plus explicitly documented integration surfaces, then verify live docs before coding against any direct API contract.

## Verified Connection Surfaces

These are the concrete Skool surfaces this skill should reason about before proposing anything custom:
- native invite flows by share link, direct email, bulk CSV import, and Zapier-driven invite emails
- Zapier trigger and action flows for paid-member export, membership-question export, member invites, and course unlocks
- membership-question answers visible in admin and exportable from the Members tab
- AutoDM with built-in variables and admin-only sending
- native calendar events, Skool Calls, and Pro webinars
- manual grant and revoke of course access for level-unlock, buy-now, or private courses
- official tracking plugins such as Google Ads, Meta pixel, and Hyros

If a requested workflow cannot be mapped to one of these verified surfaces, stop treating it as standard Skool automation and make the limitation explicit.

## Data Storage

Keep only durable Skool operating context in `~/skool/`:
- approved group URLs, plan context, and the business model behind the community
- onboarding rules, membership question logic, and approval boundaries that the user confirmed
- course unlock patterns, calendar cadence, and retention experiments worth reusing
- approved automation hosts, API-key usage rules, and no-go automations
- incidents such as broken invite flows, spam bursts, accidental access grants, or webhook failures

## Core Rules

### 1. Lock the Group Promise Before Tactics
- Start by naming what the Skool group actually sells or delivers: community, course access, coaching, membership, event access, or a hybrid.
- Skool decisions around approvals, pricing, classroom design, and automations only make sense after the core promise is explicit.

### 2. Separate Advice From Live Admin Writes
- Auditing copy, structure, and funnel logic is safe by default.
- Inviting members, removing members, changing access, unlocking courses, or sending automations are real write operations and must be previewed before execution.
- Never blur strategy mode with live admin mode.

### 3. Use Only Officially Supported Automation Surfaces
- Prefer native Skool behavior first, then official plugins such as Zapier, AutoDM, or the documented webhook plugin where applicable.
- Do not invent unsupported posting bots, comment bots, or DM bots just because browser automation is technically possible.
- If a task needs direct API usage, verify the current documented surface first and keep the workflow narrow.

### 4. Treat Access Control as the Highest-Risk Layer
- Membership approval, invite links, pricing, free trials, level gates, and course permissions shape trust faster than content polish does.
- Check who gets in, what they unlock, when they unlock it, and what rollback path exists before recommending changes.

### 5. Run Classroom and Calendar as Retention Systems
- Courses and events are not isolated content libraries.
- Sequence lessons, calls, webinars, and reminders so members always know the next action and the next date that matters.
- If the classroom is deep but the calendar is dead, retention will decay.

### 6. Diagnose Growth Through the Full Member Lifecycle
- Track the full path: visitor, applicant, approved member, activated member, retained member, and expanded buyer.
- Use membership questions, instant approval rules, invite logic, AutoDM, and event participation as one funnel, not separate tactics.

### 7. Store Durable Operating Patterns, Not Member Dossiers
- Save group-level defaults, proven workflows, and incident lessons.
- Do not store raw DMs, sensitive payment details, unnecessary personal stories, or full member histories in local notes.
- Keep local memory useful enough to improve decisions and small enough to stay trustworthy.

## Common Traps

- Treating Skool like generic community software -> advice misses the tight coupling between members, classroom, and calendar.
- Using unofficial automation ideas for posts or DMs -> fragile workflows fight the platform instead of working with supported surfaces.
- Opening access before the unlock logic is tested -> members see the wrong course, the wrong price, or the wrong event.
- Relying on content volume alone -> engagement looks busy while onboarding and retention stay weak.
- Mixing strategy with live admin changes -> one session creates accidental member-facing side effects.
- Saving too much member detail locally -> privacy risk rises without improving operational decisions.

## External Endpoints

Only these endpoint categories are allowed unless the user explicitly approves more:

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| https://help.skool.com | documentation lookups only | verify live feature behavior, plan gates, and official workflow constraints |
| https://hooks.zapier.com | mapped workflow fields approved by the user | Skool-adjacent automations routed through Zapier webhooks |
| https://{user-approved-webhook-host} | invite, course access, or member fields explicitly approved for the workflow | Skool webhook plugin flows and downstream automation |

No other data is sent externally unless the user explicitly approves another integration surface after verifying it is officially supported for the task.

## Security & Privacy

Data that leaves your machine:
- documentation lookups against official Skool help pages
- mapped workflow fields sent to approved Zapier or webhook destinations
- any user-approved payloads needed for member invite or access workflows

Data that stays local:
- durable operating notes in `~/skool/`
- group strategy, onboarding rules, classroom defaults, and incident logs unless the user exports them
- rejected or draft automation plans that were never executed

This skill does NOT:
- assume an undocumented Skool CLI exists
- normalize unofficial bots for posting, commenting, or mass messaging
- execute live member-impacting writes without explicit user intent
- store credentials, payment details, or raw member message archives in local memory
- modify its own skill files

## Trust

By using this skill, approved workflow data may be sent to Skool-adjacent services such as Zapier or an approved webhook destination, plus official Skool documentation pages for verification.
Only install if you trust those services with that data.

## Scope

This skill ONLY:
- helps operate Skool groups, classroom content, calendar cadence, and official integrations safely
- turns growth, onboarding, and access problems into reproducible operating decisions
- keeps durable notes for approved defaults, automation boundaries, and recurring incidents

This skill NEVER:
- treat unsupported automation as normal just because it can be scripted
- bypass confirmation for live member-impacting changes
- claim a feature exists without checking current Skool docs when exact behavior matters
- turn local memory into a shadow CRM full of unnecessary member data

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `community-manager` - extend Skool strategy into day-to-day moderation and operating rituals
- `zapier` - wire approved Skool workflows into broader automation systems
- `webhook` - harden delivery, retries, and verification around Skool webhook flows
- `course` - improve curriculum structure and lesson sequencing inside the classroom
- `growth` - connect Skool funnel work to broader acquisition and retention experiments

## Feedback

- If useful: `clawhub star skool`
- Stay updated: `clawhub sync`
