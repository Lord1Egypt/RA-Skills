---
name: standup-mobi
description: Use when a team member is sick, on vacation, or has left and you need to cover their duties tomorrow — builds a real transfer-of-knowledge instrument that finds coverage owners for every task, maps knowledge that lives only in their head, generates a one-week ramp plan with graded shadow→assist→solo levels, and writes their daily checklist to paper without requiring their participation.
version: 1.0.2
author: Denis Voronin
license: MIT
tags: [team-management, knowledge-transfer, absence-coverage, onboarding, work-continuity, operations]
---

# Standup Mobi

## Overview

Someone disappears from a team for a week — sick, vacation, parental leave,
or quit — and the team discovers, under fire, which duties only that person
knew how to do. Coverage is improvised in Slack threads at 23:00 the night
before.

This skill turns absence coverage into a 20-minute planning exercise
instead of a crisis:

1. **Duty inventory** — everything the absentee does on a cadence (daily
   standup notes, weekly reports, on-call, invoicing, deployments…),
   captured as structured data.
2. **Coverage solver** — assigns every duty an owner from the remaining
   team given each person's capacity, skill match, and a fairness rule
   (nobody absorbs more than 1.5× the average added load).
3. **Single-point-of-knowledge detector** — duties that are `tribal=True`
   (no docs, no runbook) are flagged and turned into a 15-minute knowledge
   extraction checklist while the person is still reachable.
4. **One-week ramp plan** — for duties that need real ramp-up, a graded
   schedule: **watch → shadow → assist → solo**, one level per day, with
   explicit "stop and ask" triggers.
5. **Paper checklist** — the absentee's daily/weekly duties become a
   printable one-pager for the substitute, no app required.

Works without the absentee's cooperation (a best-effort rebuild from
standup notes), but includes a 12-question extraction interview for when
they're reachable.

## When to Use

- "Alex is on vacation next week — who covers what?"
- A teammate resigned; two-week notice just started
- Sudden sick leave / surgery recovery / parental leave coverage
- Pre-vacation planning: proactively, before the absence starts
- Audit question: "what would break if <person> disappeared tomorrow?"

**Don't use for:** long-term reorganizations (HR process), hiring plans,
or performance management. This is tactical absence coverage, not
headcount planning.

## Quick Start

```bash
# 1. Generate starter files (team.json + duties.json) pre-filled with an example
python3 scripts/mobi.py init --dir cover_alex

# 2. Add what you know about the absentee's duties (edit duties.json, or:)
python3 scripts/mobi.py duty --dir cover_alex --name "invoicing run" \
    --cadence weekly --skill finance --minutes 45 --tribal

# 3. Solve coverage: assign owners under capacity + fairness constraints
python3 scripts/mobi.py solve --dir cover_alex

# 4. Knowledge extraction checklist for tribal duties
python3 scripts/mobi.py extract --dir cover_alex

# 5. Ramp plan for the substitute(s), graded watch->shadow->assist->solo
python3 scripts/mobi.py ramp --dir cover_alex --owner jordan

# 6. Printable daily checklist for the substitute
python3 scripts/mobi.py checklist --dir cover_alex --owner jordan --out jordan.md
```

## The Data Model

**team.json** — everyone available during the absence:
```json
[
  {"name": "jordan", "capacity_min_per_day": 240, "skills": ["ops", "linux"]},
  {"name": "sam", "capacity_min_per_day": 300, "skills": ["finance", "reporting"]}
]
```
`capacity_min_per_day` is the *spare* capacity realistically available for
absence coverage, not the workday length.

**duties.json** — the absentee's duties:
```json
[
  {"name": "invoicing run", "cadence": "weekly", "skill": "finance",
   "minutes": 45, "tribal": true, "risk": "high",
   "notes": "Xero + spreadsheet recon; supplier codes in Alex's head"}
]
```
- `tribal: true` — no runbook exists; knowledge lives only in the absentee
- `risk` — what happens if it's skipped or done wrong (high/med/low)

## How the Solver Works

1. **Eligibility** — a person can take a duty if they have the skill (or
   the duty is low-risk and learnable), expressed as a match score.
2. **Load balancing** — duties are assigned greedily (highest risk ×
   minutes first) to the eligible person with the most remaining capacity,
   keeping everyone under capacity.
3. **Fairness cap** — if the assignment would push someone past
   **1.5× the average added load**, the duty is marked UNCOVERED instead
   of quietly overloading one hero. Overload is a plan defect, not a
   person's virtue.
4. **Tribal flag** — regardless of owner, every `tribal` duty appears in
   the extraction checklist: the 12 questions that pull the knowledge out
   of the absentee's head into a page while you still can.

## The 12-Question Extraction Interview

1. What do you do that nobody else on the team could do today?
2. Walk me through <duty> end to end — where do you click first?
3. What credentials/access does it need? **Name the system only** (e.g.
   "Xero admin, TOTP on the shared vault") — never write passwords or keys
   into notes or runbooks; point to where they live in your secret manager.
4. What usually goes wrong, and how do you fix it?
5. What looks scary but is actually safe to ignore?
6. What looks harmless but must NEVER be touched?
7. Who do you contact when stuck (name + channel)?
8. If you had 15 minutes to write a runbook for this, what would page one say?
9. What can be skipped entirely for one week with zero damage?
10. What has a hard deadline in the next 14 days, and what's the penalty for missing it?
11. Where are the files this needs? (For keys/credentials: name the vault
    entry, never the value.)
12. What question should I have asked that I didn't?

Questions 9 and 12 are the highest-value ones in practice — they surface
skippable work and unknown unknowns.

## Common Pitfalls

1. **Assigning coverage by who's "reliable".** That's how your best person
   ends up covering three jobs while others watch. The fairness cap exists
   to make this visible.
2. **Treating tribal knowledge as an IT problem.** It's a 15-minute
   conversation with a checklist. Run the extraction while the person is
   reachable; after they leave it costs 10×.
3. **Coverage ≠ ramp.** Knowing *who* covers is not knowing *how*. Duties
   with risk=high get a graded ramp; a name next to a task is not a plan.
4. **Ignoring cadence.** A weekly duty covered by someone who only checks
   in daily gets done 4× or never. The checklist groups by cadence.
5. **No stop-and-ask triggers.** Substitutes fail by confidently doing the
   wrong thing. Every ramp level includes explicit "stop and ask" lines.
6. **Writing secrets into runbooks.** Runbooks name the system that holds
   each credential (vault, password manager, SSO group) — never the secret
   itself. Runbooks get shared, synced, and committed; treat them as
   public.

## Verification Checklist

- [ ] Every duty in duties.json has an owner or an explicit UNCOVERED flag
- [ ] No owner exceeds capacity or the 1.5× fairness cap
- [ ] Every tribal duty appears in the extraction checklist
- [ ] High-risk duties have a ramp plan with all four levels
- [ ] The printable checklist groups duties by cadence and day

## One-Shot Recipes

**Vacation coverage, planned (best case):**
```bash
python3 scripts/mobi.py init --dir cover_alex
# edit team.json/duties.json from standup notes
python3 scripts/mobi.py solve --dir cover_alex
python3 scripts/mobi.py extract --dir cover_alex   # run interview with Alex
python3 scripts/mobi.py ramp --dir cover_alex --owner jordan
python3 scripts/mobi.py checklist --dir cover_alex --owner jordan --out jordan.md
```

**Sudden sick leave (absentee unreachable):**
Same flow, but duties are rebuilt from standup notes and calendar; every
duty defaults to `tribal: true` and the checklist is your reconstruction
document, not an interview.

**Resignation with notice:**
Run `solve` on day one of notice, run `extract` as a series of daily
15-minute sessions (don't book one "knowledge transfer meeting" — it
won't happen), `ramp` + `checklist` for each receiver.
