---
name: skill-publisher-verifier
version: 1.0.0
description: Before installing any ClawHub skill, verify the publisher's reputation and return a trust score of TRUSTED, ESTABLISHED, NEW, or FLAGGED.
author: ordo-tech
tags: [security, verification, trust, publishers, marketplace, clawhub, pre-install]
requires:
  env: []
  tools: [web_fetch, web_search]
---

## What this skill does

Before you install a skill from ClawHub, this skill investigates the publisher behind it. It collects publicly available signals from the ClawHub marketplace and returns a structured trust assessment so you can make an informed decision before running any third-party skill.

Signals checked:

- **Catalogue size** — total skills published by this author
- **Install volume** — cumulative installs across their catalogue
- **Flagged/hidden/deleted skills** — especially any removed post-ClawHavoc
- **Stars and highlights** — community endorsement signals
- **Account age** — how long the publisher has been active on ClawHub
- **Known associations** — any links to previously flagged or banned publishers

The result is a single trust label plus a brief evidence summary:

| Score | Meaning |
|---|---|
| **TRUSTED** | Established author, high installs, no flags, long track record |
| **ESTABLISHED** | Active author, reasonable history, minor concerns if any |
| **NEW** | Recently created account or very small catalogue — proceed with caution |
| **FLAGGED** | Known flags, deleted skills post-ClawHavoc, or suspicious associations |


## When to use it

Use this skill **before installing any unfamiliar skill** from ClawHub, especially when:

- The publisher is unknown to you
- The skill requests elevated tool access (exec, write, process)
- You are installing skills in bulk or via automation
- You are operating in a production or shared environment
- The skill was recently published (new entries carry higher risk)
- You encountered the skill via a link rather than browsing the marketplace directly

You do not need to run this skill for well-known authors you already trust. But when in doubt, verify first.


## Usage

Invoke this skill by providing a ClawHub publisher handle or skill URL. The agent will search and fetch publisher data from ClawHub, analyse the signals, and return a structured report.

**Input options:**

1. Publisher handle: `@ordo-tech`
2. Skill URL: `https://clawhub.com/skills/some-skill`
3. Skill name: `skill-name` (agent will resolve the publisher)

**What the agent does, step by step:**

1. Resolve the publisher handle from the input (extract from URL or skill name if needed)
2. Fetch the publisher's ClawHub profile page using `web_fetch` at `https://clawhub.com/@{handle}`
3. Extract: skill count, total installs, stars, account creation date, any visible flags or warnings
4. Search for the publisher handle using `web_search` to surface any external flags, forum reports, or ClawHavoc-era incidents
5. Check for known associations with flagged publishers (cross-reference any co-author or fork relationships visible on their profile)
6. Synthesise the signals into a trust score
7. Return a structured report (see output format below)

**Output format:**

```
Publisher: @{handle}
Trust Score: TRUSTED | ESTABLISHED | NEW | FLAGGED

Signals:
- Skills published: {n}
- Total installs: {n}
- Flagged/deleted skills: {n}
- Stars: {n}
- Account age: {n} months
- External flags: none | {description}
- Associations: none | {description}

Summary: {1–2 sentence plain-language verdict}

Recommendation: Install / Install with caution / Do not install
```

If data cannot be retrieved (publisher profile not found, private, or ClawHub unavailable), report that explicitly and return score: **NEW** with a note that verification was incomplete.


## Examples

### Example 1 — Checking a publisher by handle before installing

> User: "I want to install a skill from @rapid-skills-99. Check them first."

Agent fetches `https://clawhub.com/@rapid-skills-99`, finds: 2 skills published, 47 total installs, account created 11 days ago, no stars, one skill hidden. Web search returns no external mentions.

```
Publisher: @rapid-skills-99
Trust Score: NEW

Signals:
- Skills published: 2
- Total installs: 47
- Flagged/deleted skills: 1 (hidden)
- Stars: 0
- Account age: 11 days
- External flags: none found
- Associations: none found

Summary: Very new account with limited history and one hidden skill. Insufficient track record to assess intent.

Recommendation: Install with caution
```

---

### Example 2 — Verifying a publisher from a skill URL

> User: "Verify the publisher of https://clawhub.com/skills/auto-deployer-pro"

Agent extracts publisher handle from the skill page, then runs full verification.

```
Publisher: @deploy-forge
Trust Score: ESTABLISHED

Signals:
- Skills published: 8
- Total installs: 4,200
- Flagged/deleted skills: 0
- Stars: 14
- Account age: 9 months
- External flags: none found
- Associations: none found

Summary: Active publisher with a solid catalogue and no red flags. Reasonable install volume relative to account age.

Recommendation: Install
```

---

### Example 3 — Flagged publisher detected

> User: "Check @xfiltrate-skills before I install their memory exporter."

Agent fetches profile and runs web search. Finds: account created post-ClawHavoc, 3 skills deleted by ClawHub moderation, community forum thread flagging suspicious data exfil behaviour.

```
Publisher: @xfiltrate-skills
Trust Score: FLAGGED

Signals:
- Skills published: 1 (active), 3 (deleted by ClawHub)
- Total installs: 220
- Flagged/deleted skills: 3 (removed by moderation)
- Stars: 0
- Account age: 2 months
- External flags: Community forum report — suspected data exfiltration pattern
- Associations: Possible link to banned publisher @data-grab-co (shared skill descriptions)

Summary: Multiple skills removed by ClawHub moderation and credible external reports of malicious behaviour. High risk.

Recommendation: Do not install
```


## Requirements

- **Tools required:** `web_fetch`, `web_search`
- **Environment variables:** none
- **ClawHub account:** not required — checks public profile data only
- **Network access:** required to reach `clawhub.com` and run web searches

This skill uses only public data. It does not authenticate with ClawHub or store any information between runs.


## Support

- Publisher profile: https://clawhub.com/@ordo-tech
- Issues and feedback: https://clawhub.com/@ordo-tech
- Part of the **ClawHub Security Pack** — see the full bundle at https://theagentgordo.gumroad.com/
