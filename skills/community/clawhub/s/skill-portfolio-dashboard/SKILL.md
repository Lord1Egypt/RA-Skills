---
name: skill-portfolio-dashboard
description: Use when you publish or maintain a portfolio of agent skills (ClawHub, GitHub, internal registry) and need a single health dashboard — which skills have dead links, missing READMEs, stale versions, inconsistent frontmatter, clone-count anomalies, or unpublishable structure — instead of checking each repo by hand.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [skills, portfolio, dashboard, quality-audit, publishing, clawhub]
---

# Skill Portfolio Dashboard

## Overview

Publishing skills at any cadence (5/day, 5/week) creates a portfolio nobody audits: 200+ directories, each with SKILL.md, scripts, references, a GitHub repo, a ClawHub listing. The failure modes are silent — a dead GitHub token means new skills quietly stop landing in repos; a rushed publish ships without README; frontmatter drifts (missing version, tags, over-long descriptions) until a registry rejects it; scripts bit-rot because a dependency changed under them.

This skill turns a build directory into a **one-command portfolio health report**: per-skill structure compliance, frontmatter consistency, script syntax/executability, README/LICENSE presence, git-tracked status, and (optionally) GitHub/ClawHub cross-checks — with a portfolio score and a prioritized fix queue.

## When to Use

- You maintain more skills than you can hold in your head (the threshold is about 10).
- After any publishing pipeline change (new token, new registry, new format rule).
- Periodic hygiene: weekly/monthly sweep before the portfolio rots.
- Before promoting your portfolio ("all 200 skills clean, linked, executable").
- Diagnosing "why did skill X fail to publish/verify" from structure alone.

Don't use for: content quality review of what a skill *says* (that's editorial), or runtime behavior inside a live agent (that's session logs).

## How It Works

1. **Scan** the portfolio root: every subdirectory containing SKILL.md = a skill.
2. **Structure checks** (publishable shape): SKILL.md present; README.md; LICENSE; `references/`; `scripts/` with ≥1 `.py`; scripts pass `python -m py_compile`; no stray junk (nested `.git` confusion, token leakage scan!).
3. **Frontmatter checks**: parses as YAML; `name` matches directory; `description` present, ≤1024 chars, starts with a use-trigger; `version` semver-ish; `author`, `license`, `tags` present; description/body ratio sane.
4. **Repo checks** (local git): is it a git repo, does it have a remote, are there uncommitted changes, does the latest commit message mention the skill.
5. **Security check**: scan all tracked text for credential patterns (`ghp_`, `sk-`, `AKIA`, `Bearer `, passwords in URLs). A skill portfolio is a lovely place to leak a token into a public repo — this catches it before push.
6. **Score & queue**: per-skill grade (A–D), portfolio score, and a fix queue ordered by severity (security > structure > frontmatter > polish).

## Report Shape

```
PORTFOLIO: 213 skills scanned
Score: 96/100   A:207  B:4  C:2  D:0

SEVERITY ORDER FIX QUEUE:
 1. [SECURITY] skill-x: token-like string in scripts/foo.py:12
 2. [STRUCTURE] skill-y: no LICENSE
 3. [FRONTMATTER] skill-z: description 1104 chars (limit 1024)
 ...
CLEAN: 207 skills fully compliant
```

## Worked Examples

`python3 scripts/portfolio_dashboard.py --root /path/to/skills --json` — scan + machine-readable output.

`python3 scripts/portfolio_dashboard.py --root . --verbose` — per-skill one-liners, not just exceptions.

(If the portfolio root also contains pipeline files — IDEAS.md, published.json — the scanner ignores non-skill directories automatically.)

## Common Pitfalls

1. **Publishing faster than auditing.** The pipeline feels productive while 30 skills silently lack READMEs; a dashboard pass takes 10 seconds and surfaces the debt.
2. **Token committed into a script.** The #1 real security incident in skill pipelines. Scan BEFORE every push, not after the leak.
3. **Frontmatter drift.** Early skills have no `version`/`tags`; registries tighten rules later; old skills start failing verification they used to pass. The dashboard shows the drift as a fix list, not a surprise.
4. **Testing scripts only at creation.** A script that imported something env-specific breaks months later. `py_compile` catches syntax rot cheaply; run the `--smoke` mode to execute `--help` on every script for import-level rot.
5. **Judging by green checkmarks on the last 5 skills.** Recency bias hides the long tail. The dashboard's job is the long tail.
6. **One giant directory with mixed concerns** (build dirs, pipeline scripts, skill dirs). Keep the scanner pointed at the skills root; it ignores non-skill dirs, but humans shouldn't have to.
7. **No version bump discipline.** If SKILL.md changed materially but version didn't, registries serve stale metadata. The dashboard flags changed-content-since-last-version if git history allows.

## Verification Checklist

- [ ] Portfolio scan runs clean (exit 0) on the whole skills root
- [ ] Zero SECURITY findings (credential patterns) before any push
- [ ] All skills carry README + LICENSE + references/ + executable script(s)
- [ ] Frontmatter: name==dir, description ≤1024 chars w/ trigger phrasing, version bumped on change
- [ ] Fix queue emptied or explicitly deferred with reasons
- [ ] Re-run after fixes confirms grade movement (D→A)
