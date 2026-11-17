# Skill Portfolio Dashboard — Reference

## 1. What rots in a skill portfolio

| Rot | How it happens | Detector |
|---|---|---|
| Token leakage | credential pasted into a publish script that later ships | security regex scan (ghp_, sk-, AKIA, xox, URL-embedded creds) |
| Structure drift | rushed publish skips README/LICENSE/references | per-skill structure checks |
| Script rot | env changed under a script; syntax errors creep in | `compile()` exec of every script |
| Frontmatter drift | registry rules tighten; old skills non-compliant | name==dir, description ≤1024 + trigger phrasing, version/author/license/tags |
| Unpublished work | built, never committed/pushed | git checks (`--git` mode) |
| Description bloat | the 1024-char limit approached as scope creeps | length check |

## 2. Grading model

```
issue severities: sec > struct > fm > polish
hard = count of sec/struct/fm issues
A = no issues at all
B = only polish issues
C = 1-2 hard issues
D = 3+ hard issues (or missing SKILL.md entirely)
portfolio score = 100 x (A + 0.6B + 0.3C) / N
```

Exit code 2 when any security finding or any D-grade skill exists — CI-friendly.

## 3. Security patterns (extend for your stack)

```python
("ghp_[A-Za-z0-9]{20,}",               "GitHub PAT"),
("github_pat_[A-Za-z0-9_]{20,}",       "GitHub fine-grained PAT"),
("sk-[A-Za-z0-9]{20}",                 "OpenAI-style key"),
("AKIA[0-9A-Z]{16}",                   "AWS access key"),
("xox[baprs]-[A-Za-z0-9-]{10,}",       "Slack token"),
(r"https?://[^\s/:]+:[^\s@]{6,}@",     "credentials in URL"),
```

The scan is a single compiled alternation over every text file <1 MB (fast: 221-skill portfolio in ~10 s on an SBC). Files >1 MB are skipped — none of your artifacts should be that big anyway.

**Response protocol when it fires:** revoke the token FIRST (it must be considered public the moment it touched a file that ever left the machine), then scrub history (`git filter-repo`), then rewrite the pipeline to read from env/config outside the portfolio tree.

## 4. Frontmatter parser notes

The built-in parser is deliberately minimal (flat keys + one nesting level + inline lists + folded multi-line values). It handles the peer shape:

```yaml
---
name: x-y
description: Use when ...   # one line OR folded multi-line
version: 1.0.0
author: ...
license: MIT
tags: [a, b]         # inline  OR  block list
metadata:
  hermes:
    tags: [...]
---
```

If your tree uses exotic YAML (anchors, multi-level nesting), swap `parse_frontmatter` for `yaml.safe_load` — the checks downstream don't care where the dict came from.

## 5. Operating cadence

- **Before every push:** `portfolio_dashboard.py --root .` on the skills root; zero SEC findings required.
- **Weekly:** full run + work down the fix queue by severity.
- **After registry rule changes:** re-run; new fm checks surface the grandfathered violations as a list, not an emergency.

## 6. Extending

- `check_skill()` returns structured issues — add checks (e.g., "references/ files referenced from SKILL.md", "scripts have --help") by appending to `issues` with a severity.
- `--json` output feeds anything: a static HTML badge, a cron alert, a CI gate.
- Registry cross-checks (ClawHub verify per slug, GitHub API per repo) belong in a wrapper that consumes the JSON — keep this tool offline-only and fast.

## 7. Honest limits

- Line-count-based "body too short" is a heuristic; a brilliant 150-char skill would be flagged.
- Trigger-phrase check is stylistic (recommended convention, not a registry rule).
- Git checks are opt-in because 200+ `git status` subprocess calls are slow on cold storage.
