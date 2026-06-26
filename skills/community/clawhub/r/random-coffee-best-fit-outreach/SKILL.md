---
name: random-coffee-best-fit-outreach
description: Offline random coffee skill for ranking opt-in people and preparing consent-first intro packets. It creates local reports only; any external communication stays outside the public skill.
version: 0.1.4
homepage: https://github.com/zack-dev-cm/random-coffee-best-fit-outreach
license: MIT
user-invocable: true
metadata: {"openclaw":{"homepage":"https://github.com/zack-dev-cm/random-coffee-best-fit-outreach","skillKey":"random-coffee-best-fit-outreach","requires":{"anyBins":["python3","python"]}}}
---

# Random Coffee Best Fit Outreach

## Goal

Run a consent-first random coffee workflow from local participant data:

- normalize opt-in people into a small participant CSV
- rank best-fit 1:1 intro candidates by mutual utility
- draft first-touch and double opt-in intro text
- render an offline review packet for the operator
- keep external communication outside this public skill

## Use This Skill When

- the user asks for random coffee, best-fit introductions, warm networking, or founder/operator matching
- the source data is already opt-in, consented, or intentionally provided by the operator
- an older chat-first matching project exists and should be adapted into a public-safe intro workflow
- Codex should produce a repeatable intro packet, not ad hoc social copy

## Inputs

Use a CSV with these canonical columns:

```csv
person_id,display_name,role,organization,location,timezone,languages,domains,skills,offers,needs,preferred_channel,availability,consent_notes,do_not_match,notes
```

Read `references/intake-schema.md` when the user gives messy notes, a contact map, or community notes.

## Workflow

1. Restate the cohort goal, target audience, consent boundary, and verification command.
2. Normalize participant data into the CSV schema. Use placeholder or consented data only.
3. Rank matches:
   - In a cloned repo: `python3 -m random_coffee_matcher rank <people.csv> --format markdown --out <report.md>`.
   - From this skill wrapper in the repo: `python3 {baseDir}/scripts/random_coffee_matcher.py rank <people.csv> --format markdown --out <report.md>`.
4. Review the top matches. Prefer pairs with clear mutual utility, language overlap, manageable timezone gaps, and complete consent notes.
5. Generate a reviewed packet for any selected pair:
   - `python3 -m random_coffee_matcher packet <people.csv> <person-a-id> <person-b-id> --out <packet.md>`.
6. Hand the packet to the operator. Any external communication happens outside this public skill.
7. Log the operator-recorded outcome: skipped, blocked, opted in, declined, scheduled, or closed.

## External Communication Boundary

Read `references/outreach-surface-runbook.md` before using the packet outside the repo.

Rules:

- Use only operator-provided or consented participant data.
- Keep the generated packet local until the operator approves it.
- Do not include private notes, long copied profile text, or private conversations in public artifacts.
- Do not reveal names, handles, links, or detailed context until both sides opt in.
- If any platform, privacy, or account-control issue appears, stop this workflow and ask for human handling outside the skill.

## Outreach Rules

- First touch asks whether the person wants to be considered. It should not reveal another person's identity.
- Double opt-in asks each side before sharing names, handles, links, or detailed context.
- Keep drafts short, concrete, and easy to decline.
- Avoid fake urgency, pressure, claims of personal familiarity, or unverifiable praise.
- If either person declines or does not reply after the agreed follow-up limit, close the case.

## Verification

For the open-source repo, run:

```bash
python3 -m pytest -q
python3 -m random_coffee_matcher rank examples/participants.csv --format text
python3 scripts/check_clawhub_skill_surface.py
```

Before publishing, run the local public-surface audit available in the surrounding Codex workspace when present.
