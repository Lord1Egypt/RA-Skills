---
name: ideation
description: Turn findings already mined by podcast/review-scout into prioritized "build/test next" proposals, each citing the specific finding(s) that motivated it. Use when the user asks "what should we build next", "what's worth prioritizing", or wants a synthesis across research + reviews instead of another raw findings dump.
metadata:
  openclaw:
    homepage: https://github.com/OrenSegal/signal-skills
    requires:
      bins: [python3]
---

Findings are not decisions. `podcast` and `review-scout` each produce ranked
findings; this skill is the one step further — turning "23 reviews complain
about slow checkout" into "ship a one-tap checkout retry, here's why, here's
the confidence." Every proposal must cite a finding. An idea with no
citation is a guess wearing a findings hat — don't generate those.

## Step 0 — Check the ledger before proposing

```bash
python3 ~/.claude/skills/ideation/ledger.py list --status proposed
python3 ~/.claude/skills/ideation/ledger.py list --status shipped
```

Don't re-propose something already `proposed` (still pending a decision),
`shipped` (done), or `rejected` (already said no, would need new evidence to
revisit). Only `parked` ideas are fair game to resurface if new findings
strengthen the case.

## Step 1 — Pull source findings

Read the other skills' state directly, don't re-derive from scratch:

```bash
python3 ~/.claude/skills/podcast/ledger.py known-issues 2>/dev/null
python3 ~/.claude/skills/review-scout/ledger.py known-issues 2>/dev/null
python3 ~/.claude/skills/review-scout/ledger.py dedup --threshold 0.5 2>/dev/null
```

If the user already has a specific rendered report (podcast/review-scout
output) in this conversation, use that directly instead of re-querying the
ledger — it's the same data, already synthesized.

## Step 2 — Generate proposals, one per candidate

For each build/test candidate, work out:

1. **The citation** — which specific finding(s) motivate this, verbatim
   claim text or a short paraphrase plus source (app/show, batch/episode).
2. **The shape** — is this a bug fix, a feature, an experiment, or a
   "needs more data" flag? Don't force everything into "build this."
3. **Effort vs. confidence** — cheap+high-confidence beats expensive+
   speculative; say which bucket this falls in, don't just list ideas flat.
4. **What would make this wrong** — the one thing that, if true, kills the
   idea. Forces you to actually think about it instead of pattern-matching
   "reviews complained → build the fix."

Record each as you go:

```bash
python3 ~/.claude/skills/ideation/ledger.py propose --title "<short title>" \
  --citations-json '["23 reviews cite slow checkout, v2.4-2.6 (review-scout)", "..."]' \
  --note "<effort/confidence/kill-condition, one line each>"
```

## Step 3 — Rank, don't just list

Sort by confidence × leverage, not by recency or by which source skill
produced it. A single well-corroborated review-scout regression outranks
three speculative podcast takeaways with no repeat citation.

## Step 4 — Report (shared renderer)

Same `render_report.py`/`template.html` as the other three skills
(a real copy here, kept in sync with the canonical one in `signal-report`
— packaged plugins ship real files, not symlinks, so this installs standalone). Tiers should reflect decision-readiness, not just
severity — e.g. "Ship now (cheap, confirmed)", "Worth a spike (confidence
gap)", "Needs more data before deciding", "Parked (rejected once, revisit
if new evidence)".

```bash
python3 ~/.claude/skills/ideation/render_report.py payload.json out.html
```

Publish with `Artifact` on Claude Code; elsewhere use `--open` or report
the path.

For a paste-into-a-ticket/prompt form of the same proposals, add a `.md`
target in the same invocation:

```bash
python3 ~/.claude/skills/ideation/render_report.py payload.json out.html out.md
```

## Step 5 — After the user decides

Update status so the next run doesn't re-propose it:

```bash
python3 ~/.claude/skills/ideation/ledger.py set-status --title "<title>" --status shipped
python3 ~/.claude/skills/ideation/ledger.py set-status --title "<title>" --status rejected
python3 ~/.claude/skills/ideation/ledger.py set-status --title "<title>" --status parked
```

## Hygiene

- State lives in `~/.claude/skills/ideation/config.json` and
  `state/ideas.json` — a real copy of the ledger pattern, deliberately NOT
  symlinked to podcast's or review-scout's ledger.py (same
  `Path(__file__).resolve()`-follows-symlinks state-isolation bug that
  ruled out sharing ledger.py anywhere else in this skill family).
- This skill reads podcast/review-scout state but never writes to it.
