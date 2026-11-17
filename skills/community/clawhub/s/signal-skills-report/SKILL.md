---
name: signal-report
description: Turn a pile of ranked research findings (from podcast mining, competitor audits, doc sweeps, whatever) into one prioritized Artifact report. Use as the reporting stage of any skill that has already done the extraction and just needs to present it as a shareable, ranked, reasoned page. Not a research method itself, and not a curation step.
metadata:
  openclaw:
    homepage: https://github.com/OrenSegal/signal-skills
---

Render everything relevant, ranked, with reasoning. Don't curate down to a
"top 3" and don't dump an uncurated section-by-section wall either. Every
item in scope for the query gets a slot; priority order does the filtering
work instead of a cutoff.

## When to reach for this

Called from another skill's own report step, once that skill has already:
extracted findings, tagged confidence per finding (measured / anecdotal /
speculative, confirmed-once / confirmed-twice / unresolved), and decided
what's in scope for the user's actual query. (`podcast` owns its own
copy of this template so it can run standalone. This skill remains available for any other source type
— competitor audits, doc sweeps — that wants the same report shape without
duplicating the template.)

This skill does NOT do extraction, dedup, or synthesis. That's upstream work
specific to the source type. This is purely: take the finished findings list
and render it well.

## On-device vs. tokens

The HTML shell (`template.html`'s CSS, token structure, tier/item markup)
is static and mechanical. `render_report.py` (next to this file) generates
it from a JSON payload with zero tokens — no LLM involved in producing the
markup itself. The token spend in this skill is entirely upstream of that:
the headline framed as an answer, tier labels that mean something, and the
one-line reasoning attached to each finding. Build the JSON payload, then
run:

```bash
python3 ~/.claude/skills/signal-report/render_report.py payload.json out.html
```

and publish `out.html` with the `Artifact` tool on Claude Code. On any
other harness (OpenCode, Codex CLI, etc. — no `Artifact` tool available),
add `--open` to the same command to preview it in the local default
browser instead, or just report the output path; see `AGENTS.md` next to
this file. Never hand-write the report HTML — see the script's docstring
for the exact payload schema.

When the user wants something they can paste into a prompt, ticket, or
chat message rather than (or alongside) the Artifact, add a `.md` output
target in the same invocation — same payload, same validation, picked by
the output file's extension:

```bash
python3 ~/.claude/skills/signal-report/render_report.py payload.json out.html out.md
```

## Rules

1. **Rank, don't cut.** Every finding relevant to the query appears in the
   payload, grouped into priority tiers (e.g. ship-now, already-validated,
   open-decision, worth-testing, skip-this-source). A finding that doesn't
   make tier 1 still belongs in the report, lower down, not silently
   dropped. If a genuine volume problem exists (50+ findings), say so
   explicitly and link to the full data instead of truncating without a
   note.
2. **Reasoning travels with the finding**, not to a separate section. Each
   item's `reasoning` field states why it matters here; `source` carries
   the citation. Never split them.
3. **No em dashes anywhere in the copy.** `render_report.py` scans every
   text field in the payload and refuses to render, naming the offending
   field, if it finds one — this is enforced mechanically now, not a
   manual check.
4. **Confidence is visible, not just implied.** `tag` and `tag_class` are
   required fields per item in the payload; the script errors if either is
   missing, so there's no path to an untagged finding.
5. **Contrast is theme-aware, correctly, every time.** `render_report.py`
   makes it structural: the script only ever substitutes the title into the
   head, and never touches the `:root` / `:root[data-theme]` / media-query
   blocks, so an inverted dark/light token block (light text on a light
   card) can't come through this path.
6. **Don't default to the AI-cliché look.** Warm-cream background + serif
   headline + terracotta accent is the exact combination `artifact-design`
   calls out as a generic default, and it reads as slop on sight. This is
   the one rule the script can't enforce: if the report's subject calls for a
   different palette than `template.html`'s default (dark "signal
   intercept" panel, sans display, monospace data, signal-strength bars),
   edit the CSS variables in `template.html` directly before that run.
   Never fall back to cream+serif+terracotta.
7. **Load `artifact-design` before publishing** — required by the
   `Artifact` tool itself, not optional.

## Structure that works

- One-line eyebrow: source scope + date (e.g. "36 episodes, 2026-07-16").
- Headline framed as the answer to the query, not a generic report title.
- One-sentence restatement of the query, so the ranking makes sense.
- Priority tiers, each a short label explaining what the tier means (not
  just "Tier 1") — e.g. "Ship before the deadline", "Already validated,
  keep doing it", "Decide before building further", "Worth a test, not a
  decision", "Skip this source next time". Include every tier that has at
  least one item; the script refuses to render an empty tier rather than
  rendering a thin or hidden one, so simply leave zero-item tiers out of
  the payload.
- Within a tier: order items by confidence (confirmed-twice above measured
  above anecdotal above unresolved), not by source or chronology.
- Footer: where the source data and any backing ledger/state files live
  (`footer_left` / `footer_right` in the payload).

## Anti-patterns (seen and rejected in earlier drafts)

- Picking a "top 3-4 actionables" and demoting everything else to a
  footnote strip. The user wants full prioritized coverage, not a curated
  highlight reel.
- Section headers for "Use now / Watch / Ignore" with a fixed 3-4 item cap
  per section regardless of how many findings actually exist at that
  priority.
- Warm-cream-plus-terracotta-serif as an unexamined default (flagged by
  `artifact-design` as a cliché combination) — pick a neutral and accent
  that's actually grounded in the report's subject instead.
