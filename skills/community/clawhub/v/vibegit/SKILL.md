---
name: vibegit
description: Estimate how much of a git repository is AI-assisted and how sloppy it is. Use when the user asks whether a repo (or recent work) is "vibe coded", wants an AI-slop score, a repo health/quality snapshot, a badge, or a CI gate based on commit history. Read-only - commit metadata only, no file contents, no network.
allowed-tools: Read, Bash(git:*), Bash(python3:*)
permissions: [file_read, file_write, process]
---

# vibegit v1.0.3

Estimate AI-assisted work and slop signals from git history. One command, deterministic output, zero dependencies.

## Install

```bash
clawhub install thiennhant95/vibegit
```

## When to use

- "Repo này vibe-code bao nhiêu?", "audit nhanh lịch sử commit", "có dấu hiệu AI slop không?"
- Cần badge/report cho README, PR, CI.
- So sánh chất lượng quy trình giữa các giai đoạn (`--since`).

## Commands

```bash
python3 <skill_dir>/vibegit.py <repo>                     # overview card
python3 <skill_dir>/vibegit.py <repo> --format md         # Markdown report
python3 <skill_dir>/vibegit.py <repo> --format json       # JSON
python3 <skill_dir>/vibegit.py <repo> --badge vibegit.svg # SVG badge
python3 <skill_dir>/vibegit.py <repo> --share             # one-liner
python3 <skill_dir>/vibegit.py <repo> --since "90 days ago"
python3 <skill_dir>/vibegit.py <repo> --max-score 40      # CI gate (exit 1)
```

Exit codes: `0` ok · `1` score > `--max-score` · `2` not a git repo / no commits · `4` git error.

## What it measures

- AI signals: AI-named `Co-Authored-By`/`Assisted-by`/`Generated-by` trailers, AI bot authors, "Generated with [tool]" messages (confirmed); other AI mentions (likely).
- Slop signals: giant commits (>400 lines), short/lazy messages, test deletions, file churn, lockfile-only commits.
- Slop score 0–100 with a transparent per-signal breakdown; verdict Clean / Mild slop / Slop / Heavy slop.

## Reporting guidance

- Present the AI number as an **estimate with a confidence band** (confirmed vs likely). Never claim it proves authorship.
- Quote the top signals and the score breakdown; suggest `--since` for fair periods.
- For CI, use `--max-score` (e.g. 40) instead of hard-failing on any signal.

## Privacy & safety

- Runs only `git log` and `git rev-parse` with a fixed argv list (`shell=False`).
- Never reads file contents, never touches secrets, never calls the network, never executes repository content.
- Writes only the files you request (`--badge` path, redirected reports).

## Limits

- Heuristic: AI work without trailers, bot authors, or message markers can be invisible.
- Shallow clones (`--depth 1`) expose one commit; use a full clone.
- Long-lived repos skew churn/lockfile metrics; use `--since` for comparisons.

## Related skills

- `vibecheck` — audit AI-generated code for security issues and AI slop: `clawhub install thiennhant95/vibecheck`
- `skill-firewall` — scan third-party agent skills before installing them: `clawhub install thiennhant95/skill-firewall`
- `undo-first` — reversible-action guard with snapshots, risk gate, and verified restore: `clawhub install thiennhant95/undo-first`

Source + tests: https://github.com/thiennhant95/vibegit
License: MIT.
