---
name: tinytroupe-feed-research-lab
description: Run bounded synthetic audience research for draft posts and X-style feed experiments inspired by TinyTroupe and public xai-org/x-algorithm architecture. Use when Codex needs to compare content drafts, persona reactions, conversation quality, link friction, safety/spam risk, or feed-loop hypotheses without claiming reach prediction, shadowban detection, live For You cloning, or private account analysis.
license: MIT-0
metadata: {"openclaw":{"homepage":"https://github.com/zack-dev-cm/open-feed-recsys-lab","skillKey":"tinytroupe-feed-research-lab","requires":{"anyBins":["python3","python"]}}}
---

# TinyTroupe Feed Research Lab

Use this skill to compare draft posts with synthetic audience personas and produce a research report. Treat outputs as qualitative pretesting and hypothesis generation, not live X ranking predictions.

## Core Workflow

1. Collect 2-10 draft posts or content angles.
2. Clarify the target audience if available.
3. Run `scripts/tinytroupe_feed_research_lab.py` in deterministic mode.
4. Read `feed_research_report.md`, `feed_research.json`, and `persona_reactions.csv`.
5. Present the best draft, why it won, key objections, rewrite suggestions, and the boundary statement.
6. If the user asks for TinyTroupe proper, use the generated persona specs and experiment plan as the input to a separate TinyTroupe notebook or script.

## Quick Start

```bash
SKILL_DIR="${CODEX_HOME:-$HOME/.codex}/skills/tinytroupe-feed-research-lab"
python3 "$SKILL_DIR/scripts/tinytroupe_feed_research_lab.py" \
  --audience "AI builders and creator-operators interested in X algorithm research" \
  --draft "I audited this viral X algorithm claim against public source. Verdict: misleading." \
  --draft "Replies are king. Here is what the public repo actually proves." \
  --output-dir /tmp/tinytroupe-feed-research
```

Use files:

```bash
python3 "$SKILL_DIR/scripts/tinytroupe_feed_research_lab.py" \
  --drafts-file /tmp/drafts.json \
  --personas-file /tmp/personas.json \
  --output-dir /tmp/tinytroupe-feed-research
```

The script writes:

- `feed_research_report.md`: human-readable comparison and rewrite guidance.
- `feed_research.json`: machine-readable drafts, personas, reactions, and warnings.
- `persona_reactions.csv`: row-level persona reactions.
- `share_card.md`: short public-safe summary.
- `share_card.svg`: visual summary card.
- `tinytroupe_experiment_plan.md`: optional bridge plan for a real TinyTroupe run.

## Input Formats

`--drafts-file` accepts:

- JSON list of strings.
- JSON list of objects with `id` and `text`.
- Plain text blocks separated by `---`.

`--personas-file` accepts JSON objects with:

- `name`
- `segment`
- `interests`
- `dislikes`
- `reply_bias`
- `skepticism`
- `link_sensitivity`
- `safety_strictness`

Missing persona fields fall back to conservative defaults.

## Boundaries

Read `references/research-boundaries.md` before presenting results that mention algorithms, feed ranking, virality, reach, shadowbans, or account status.

Never say:

- "this predicts reach,"
- "this clones the X For You feed,"
- "this proves a shadowban,"
- "this optimizes for the live algorithm,"
- "this is what real users will do."

Prefer:

- "synthetic audience reaction,"
- "draft pretest,"
- "conversation-quality signal,"
- "X-style feed research sandbox,"
- "hypothesis to validate with real posting or user research."

## TinyTroupe Bridge

The MVP script does not require TinyTroupe. It produces `tinytroupe_experiment_plan.md` so a later agent can create a TinyTroupe notebook with:

- the same personas,
- the same draft set,
- a structured reaction schema,
- a validation note that simulation outputs are research signals.

## Companion Skills

Use `x-algo-claim-auditor` when the task is checking whether a viral algorithm claim is true. Use `open-feed-recsys-lab` when the task is verifying the public source repo, Phoenix artifact readiness, or architecture map.
