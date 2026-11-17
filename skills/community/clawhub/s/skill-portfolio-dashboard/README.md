# Skill Portfolio Dashboard

**You published 200 skills. When did you last check even 10 of them?**

Skill pipelines rot silently: a token pasted into a publish script, a rushed release missing its README, frontmatter that fails a registry rule tightened last month, scripts that stopped compiling when the environment moved. Every failure is invisible until the worst moment — a public leak or a rejected publish.

This skill is a **one-command health audit** for a directory of skills: structure compliance, frontmatter consistency, script compilability, credential-leak scanning, and (opt-in) git state — graded A–D per skill with a portfolio score and a severity-ordered fix queue.

## What it does

- **Structure**: SKILL.md / README / LICENSE / references/ / scripts present; every `.py` compiles.
- **Frontmatter**: YAML parses; `name` matches the directory; description ≤1024 chars with "Use when…" trigger phrasing; version/author/license/tags present.
- **Security**: scans every text file for credential patterns (GitHub PATs, API keys, AWS keys, Slack tokens, credentials embedded in URLs) — the leak detector that runs *before* you push. Exit code 2 on any finding.
- **Grades + fix queue**: A–D per skill, portfolio score, severity-ordered queue (security > structure > frontmatter > polish).
- **Fast and offline**: 221-skill portfolio audits in ~10 s on an SBC; single compiled regex pre-filter; git checks opt-in.

Validated on a real 221-skill portfolio, where it surfaced: 6 credential-pattern findings in pipeline scripts, one frontmatter-name/directory mismatch, and 30 legacy skills lacking trigger-phrased descriptions.

## Quick start

```bash
python3 scripts/portfolio_dashboard.py --root /path/to/skills     # human report
python3 scripts/portfolio_dashboard.py --root . --json            # machine-readable
python3 scripts/portfolio_dashboard.py --root . --git             # include per-repo git checks
```

Sample output:

```
PORTFOLIO: 221 skills scanned
Score: 91/100   A:176  B:43  C:1  D:1
Security findings: 6

FIX QUEUE (severity order):
  1. [SEC    ] scripts: CREDENTIAL PATTERN (GitHub PAT) in scripts/publish_gh.py:4
  2. [STRUCT ] some-skill: no LICENSE
  ...
```

## Why it matters

- Portfolios grow faster than attention: 5 skills/week is 250/year — no human audits 250 repos by hand.
- Credential leakage into public skill repos is the #1 real security incident in publish pipelines; a 10-second pre-push scan is the cheapest defense that exists.
- Registries tighten validation over time; grandfathered skills fail verification they used to pass. A dashboard turns that from a mystery into a fix list.

## What's inside

```
SKILL.md                        triggers, report shape, pitfalls
references/dashboard-model.md   grading model, security patterns + response protocol, extension notes
scripts/portfolio_dashboard.py  the audit engine (stdlib-only, offline)
```

## Scope & honesty

Structure and metadata quality only — it does not judge whether a skill's *content* is good (that's editorial). The frontmatter parser is minimal by design (see reference §4); swap in `yaml.safe_load` for exotic YAML trees.
