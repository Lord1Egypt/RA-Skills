---
name: research-suite
description: Router and map for the podcast/review-scout/ideation/signal-report skill family — explains what each skill does, when to reach for which one, and how the shared infra (render_report.py, template.html, analytics-check.md, per-skill ledgers) fits together. User-invoked only; never fires automatically.
disable-model-invocation: true
metadata:
  openclaw:
    homepage: https://github.com/OrenSegal/signal-skills
---

Four skills, one shared rendering/analytics spine, each with its own
state. This skill doesn't do research itself — it's the map, so you
(or a teammate new to this setup) don't have to read four SKILL.md files
to figure out which one to reach for.

## Naming heads-up

`signal-report` here is a **local render/report-generation skill**. It
owns the canonical `render_report.py`/`template.html` that the other
three skills ship generated copies of. It was called `signal-scout`
before plugin version 2.0.0 and is distinct from Oren's
separate `signal-scout` customer-discovery product
(https://github.com/OrenSegal/signal-scout), which is a different tool.

## Which skill for which ask

| You're asking | Reach for | Why not the others |
|---|---|---|
| "What's this podcast/episode actually saying" | `podcast` | Extracts insights from audio/transcript, not reviews or app-store data |
| "What are users saying / app reviews / store feedback" | `review-scout` | Same extract-don't-summarize discipline, applied to reviews across mobile/extension/web-SaaS, not audio |
| "What should we build/fix/test next" | `ideation` | The only one that reads across the other two's findings and produces a prioritized, cited proposal — not another findings dump |
| "I need a report rendered from a findings payload" | (shared `render_report.py`, lives in `signal-report`) | Not a research skill itself — the mechanical renderer all three call |

If a request doesn't match any row, it's not this family's job — answer
directly or say so.

## Shared infra map

- **`render_report.py` / `template.html`** — canonical copies live in
  `signal-report`; `podcast`, `review-scout`, `ideation` ship generated
  copies (see `scripts/sync-shared-files.sh`).
  Mechanically enforces no-em-dash, required confidence tags, and
  theme-token safety — not manual-review rules anymore.
- **`analytics-check.md`** — canonical copy lives in `podcast`;
  `review-scout` symlinks it. Backend-agnostic cross-check contract
  (PostHog, Amplitude, Mixpanel, GA4), detected at runtime. `ideation`
  doesn't need its own copy — it reads already-cross-checked findings
  from the other two rather than querying analytics directly.
- **`ledger.py`** — deliberately NOT shared. Each of `podcast`,
  `review-scout`, `ideation` has its own real copy, same shape, different
  keys (show/episode, app/batch, idea/status). A shared symlinked copy
  was tried once and reverted: `Path(__file__).resolve()` follows the
  symlink back to the *other* skill's directory and silently writes state
  into the wrong skill's `config.json`/`state/`. If you're tempted to
  dedupe this file again, don't — read the docstring in any of the three
  copies for the full story first.
- **`AGENTS.md`** — every skill in this family has one, pointing any
  non-Claude harness (OpenCode, Codex CLI, etc.) back at `SKILL.md` as
  the single source of truth, and documenting the two Claude-specific
  fallbacks every skill needs (subagent fan-out → sequential fallback;
  `Artifact` publish → `render_report.py --open`).

## On proactive routing

This router is `disable-model-invocation: true` — it only runs when you
explicitly invoke it, and it never auto-invokes the other three skills
either. That's a deliberate choice, not an oversight: Garry Tan's
`gstack` suite (github.com/garrytan/gstack) takes the opposite stance —
its router skill defaults to *proactively* invoking downstream skills
whenever a request pattern-matches, on the reasoning that a false
positive (invoking a skill that wasn't needed) is cheaper than a false
negative (answering ad-hoc when a structured workflow existed), with a
persisted per-user toggle to opt out. If that tradeoff appeals more than
this family's current "only when asked" default, the pattern to copy is:
give `podcast`/`review-scout`/`ideation` normal (non-disabled)
`description` frontmatter, so their own descriptions do the matching, and
skip a central proactive router entirely — Claude Code already invokes
model-invoked skills off their descriptions without one.

## Completion criteria for this skill

Answering "which skill / why / how do they connect" from this file alone,
with no need to open any of the four `SKILL.md` files first, unless the
user wants the actual step-by-step procedure — at which point, name the
specific skill and stop; don't reproduce its steps here.
