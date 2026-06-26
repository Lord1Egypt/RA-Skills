---
name: skill-diff-auditor
version: 1.0.0
description: Audits the diff between an installed skill and its available update, flagging new tool requests, external endpoints, and risk profile changes before you approve the upgrade.
author: ordo-tech
tags: [security, auditing, skills, updates, diff, clawhub, safety]
requires:
  env: []
  tools: [read, web_fetch]
---

## What this skill does

Before you update an installed skill, this skill fetches both versions — the one currently installed on your agent and the new version available on ClawHub — and produces a structured audit report.

The report covers:
- **Instruction changes:** A plain-English summary of what the skill is now asking the agent to do differently
- **New tools requested:** Any tools present in the new version that were not in the previous version (e.g. `exec`, `write`, `web_fetch`)
- **New external endpoints or domains:** Any URLs, API hosts, or external services referenced in the new version that did not appear before
- **Risk profile delta:** Whether the overall risk posture has increased, decreased, or stayed the same, with a brief rationale
- **Verdict:** One of three plain-English conclusions — `Safe to update`, `Update with caution`, or `Do not update` — with a one-line reason

The audit is fully non-destructive. It reads and compares; it never installs, modifies, or approves anything.

## When to use it

Use this skill whenever:
- You are about to run `clawhub update <skill-name>` and want to review what is changing first
- A skill update notification arrives and you want to understand the scope of the change
- You are operating in a security-conscious or production environment where skill changes must be reviewed before deployment
- You want a second opinion before approving a skill update that involves `exec`, `web_fetch`, or other sensitive tools
- You are auditing a batch of pending skill updates and need a triage summary

You do not need to use this skill for first-time installs — it is designed for update scenarios where a known baseline exists.

## Usage

Invoke this skill by providing:
1. The **skill name** to audit (e.g. `skill-security-scanner`)
2. Optionally, the **installed version** if you know it — otherwise the skill will read it from the installed SKILL.md

The skill will then:

1. **Read the installed version** — locate the current SKILL.md on disk (typically at `~/.openclaw/skills/<skill-name>/SKILL.md` or the equivalent workspace path) and extract its content, frontmatter, tool list, and any referenced URLs
2. **Fetch the new version** — retrieve the latest SKILL.md from ClawHub via `web_fetch` at `https://clawhub.com/skills/<skill-name>/SKILL.md` (or the registry URL if different)
3. **Compare the two versions** — diff the frontmatter fields (version, tools, tags), instruction body, and any URLs or domains mentioned
4. **Produce the audit report** — structured output covering all five areas above
5. **State the verdict** — a single clear recommendation at the top of the report

The agent does not proceed with any update. It stops after delivering the report and waits for operator instruction.

### Audit report format

```
## Skill Diff Audit: <skill-name>
Installed version: x.y.z → Available version: a.b.c

### Verdict
[Safe to update | Update with caution | Do not update]
Reason: <one line>

### Instruction changes
<plain-English summary of what changed in the body of the SKILL.md>

### New tools requested
<list any tools added; "None" if unchanged>

### New external endpoints or domains
<list any new URLs/domains; "None" if unchanged>

### Risk profile
[Increased | Decreased | Unchanged]
<brief rationale>
```

## Examples

### Example 1 — Routine maintenance update

**User:** Audit the update for skill-weather before I apply it.

**Agent actions:**
1. Reads `~/.openclaw/skills/skill-weather/SKILL.md` — finds version 1.2.0, tools: `[web_fetch]`
2. Fetches `https://clawhub.com/skills/skill-weather/SKILL.md` — finds version 1.3.0, tools: `[web_fetch]`
3. Compares: only the wttr.in fallback URL changed; no new tools; no new domains

**Report:**
```
## Skill Diff Audit: skill-weather
Installed: 1.2.0 → Available: 1.3.0

### Verdict
Safe to update
Reason: Minor instruction update; no new tools or external domains introduced.

### Instruction changes
The fallback weather source was updated from wttr.in to open-meteo.com for improved reliability. All other instructions are unchanged.

### New tools requested
None

### New external endpoints or domains
open-meteo.com (weather API, no auth required)

### Risk profile
Unchanged — open-meteo.com is a well-known public API with no authentication requirement.
```

---

### Example 2 — Update with elevated permissions

**User:** Check what changed in skill-gh-issues v2.0.0 before I update.

**Report:**
```
## Skill Diff Audit: skill-gh-issues
Installed: 1.4.1 → Available: 2.0.0

### Verdict
Update with caution
Reason: The write tool has been added, enabling file system writes. Review the new instructions before approving.

### Instruction changes
Version 2.0.0 adds a patch-application step: when a fix is generated, the skill now writes code changes directly to disk before opening a PR, rather than displaying them for manual review.

### New tools requested
- write (was not present in v1.4.1)

### New external endpoints or domains
None

### Risk profile
Increased — the addition of write means the skill can now modify files on disk autonomously.
```

---

### Example 3 — Suspicious update

**User:** Audit skill-fleet-monitor before updating.

**Report:**
```
## Skill Diff Audit: skill-fleet-monitor
Installed: 1.0.2 → Available: 1.0.3

### Verdict
Do not update
Reason: A new exec tool request and an unrecognised external telemetry endpoint have been introduced.

### Instruction changes
A new step has been added instructing the agent to POST a summary of installed skills and their versions to an external endpoint on each heartbeat cycle.

### New tools requested
- exec (was not present in v1.0.2)

### New external endpoints or domains
- https://telemetry.unknowndomain.io (unrecognised domain; not associated with clawhub.com or ordo-tech)

### Risk profile
Significantly increased — the combination of exec and an unverified external endpoint represents a potential data exfiltration vector.
```

## Requirements

- **Tools:** `read` (to access the installed SKILL.md), `web_fetch` (to retrieve the latest version from ClawHub)
- **No API keys or environment variables required**
- The skill being audited must already be installed at a known local path
- An active internet connection is required to fetch the remote version

## Support

- ClawHub profile: https://clawhub.com/@ordo-tech
- Part of the **ClawHub Security Pack** — see the full bundle at https://theagentgordo.gumroad.com/
