# Patterns — Composite Layout Recipes

> **Layer:** Patterns (built from [Components](../deck-studio/references/layouts.md) + [Foundations](../deck-studio/references/themes.md))
> **Purpose:** Battle-tested design solutions for common interaction and workflow scenarios.

---

## What patterns are

A **pattern** is a named arrangement of multiple layout components that together solve a recurring design need. Unlike a single layout (which is one slide), a pattern is a small sequence of slides that form a complete narrative unit.

Patterns prevent agents from reinventing common structures from scratch — they provide a proven skeleton that can be filled with domain-specific content.

---

## Pattern catalog

### P1. Pitch flow — Brand → Problem → Solution → Traction → Ask

Standard investor deck narrative arc. Use when the user asks for a pitch deck, funding request, or startup proposal.

```
1. cover          — Brand name + one-line value prop + deck date
2. big-quote      — A single shocking statistic or founder belief (the "why now")
3. bullets        — Problem: 3 cards, each a pain point
4. two-column     — Solution: screenshot/mockup left, explanation right
5. stat-highlight — Traction: one giant number (revenue, users, growth %)
6. kpi-grid       — 3-4 key metrics with up/down deltas
7. timeline       — Roadmap: past milestones + next 3 quarters
8. cta            — The ask: amount + use of funds + contact
```

**Theme pairing:** `pitch-deck-vc` for formal fundraising; `swiss-grid` for product pitches.

---

### P2. Hero landing — Hook → Features → Proof → CTA

Standard product landing page. Use when the user asks for a landing page, product page, or marketing site.

```
1. image-hero     — Full-bleed hero with headline + primary CTA
2. three-column   — 3 feature pillars (icon + title + one line)
3. comparison     — Before vs After, or Us vs Them
4. stat-highlight — Social proof: "X companies trust us" or "Y% improvement"
5. kpi-grid       — 3-4 proof metrics
6. cta            — Final conversion: headline + email/signup button
```

**Theme pairing:** `swiss-grid` or `corporate-clean` for SaaS; `soft-pastel` for consumer.

---

### P3. Dashboard overview — KPIs → Trend → Table → Detail

Standard analytics or admin dashboard. Use when the user asks for a dashboard, analytics page, or data report UI.

```
1. kpi-grid       — 4 KPI cards at top (the "at a glance" row)
2. chart-line     — Primary trend: 7/30/90 day line chart
3. chart-bar      — Secondary breakdown: categorical comparison
4. table          — Recent transactions / top items with sortable columns
5. chart-pie      — Composition: donut chart + legend
```

**Theme pairing:** `tokyo-night` or `dracula` for developer tools; `corporate-clean` for business dashboards.

---

### P4. Narrative deck — Hook → Sections → Takeaway

Story-driven presentation. Use when the user asks for a tech talk, storytelling deck, or any narrative-heavy presentation.

```
1. cover          — Title + speaker name + event
2. big-quote      — The opening hook (a belief, question, or stat)
3. section-divider — "01" section opener
4. bullets        — 3 supporting arguments
5. section-divider — "02" section opener
6. two-column     — Concept + concrete example
7. image-hero     — Emotional anchor: full-bleed visual moment
8. section-divider — "03" section opener
9. timeline       — Chronological progression
10. big-quote     — The closing argument (circle back to opening)
11. thanks        — Speaker contact + Q&A prompt
```

**Theme pairing:** Varies by audience — `catppuccin-mocha` for dev conferences; `magazine-bold` for design talks.

---

### P5. Comparison / decision matrix — Options → Criteria → Recommendation

Use when the user wants to compare products, approaches, or technologies.

```
1. cover          — "X vs Y vs Z" title
2. comparison     — Side-by-side two-panel (if 2 options)
3. table          — Multi-column comparison table (if 3+ options)
4. chart-radar    — Spider chart comparing on 5-6 dimensions
5. pros-cons      — Balanced pros/cons for the recommended option
6. cta            — Recommendation + next step
```

**Theme pairing:** `corporate-clean` for professional evaluations; `bauhaus` for design comparisons.

---

### P6. Process / workflow explanation — Steps → Roles → Timeline

Use when the user wants to explain a process, workflow, or methodology.

```
1. cover          — Process name + outcome
2. process-steps  — 4-6 numbered steps in cards
3. flow-diagram   — Visual pipeline with arrows
4. arch-diagram   — Roles / responsibilities grid
5. gantt          — Timeline with parallel tracks
6. cta            — "Get started" or "Learn more"
```

**Theme pairing:** `blueprint` for engineering processes; `swiss-grid` for business workflows.

---

### P7. Weekly / status report — Summary → Metrics → Blockers → Plan

Use when the user asks for a weekly report, sprint review, or status update.

```
1. cover          — Team name + date range
2. stat-highlight — One headline metric (shipped features, closed tickets)
3. kpi-grid       — 4 status indicators (green/yellow/red)
4. bullets        — 3 accomplishments this week
5. bullets        — 3 blockers / risks (use card-accent with warn color)
6. roadmap        — NEXT / LATER columns for upcoming work
7. cta            — Action items + owners
```

**Theme pairing:** `corporate-clean` for formal reports; `minimal-white` for lightweight updates.

---

### P8. Course / educational module — Objective → Concept → Example → Exercise

Use when the user asks for a course slide, tutorial, or educational content.

```
1. cover          — Module title + learning objectives
2. big-quote      — Why this matters (motivation)
3. bullets        — 3 key concepts (each with a card)
4. code           — Live code example
5. two-column     — "Do this" vs "Not that" comparison
6. terminal       — Hands-on exercise with expected output
7. cta            — "Next module" link + recap
```

**Theme pairing:** `catppuccin-mocha` or `dracula` for developer education; `academic-paper` for formal courses.

---

## How to use patterns

### For agents
When the user's request matches a pattern trigger (e.g., "pitch deck" → P1, "dashboard" → P3):
1. Announce which pattern you're using: "Using the **Pitch flow** pattern (P1)."
2. Fill each slide slot with domain-specific content from the user's brief.
3. If the user provides their own structure, respect it — patterns are defaults, not mandates.

### For humans
When you know what kind of deliverable you want, reference the pattern by name:
- "Use the **Dashboard overview** pattern" → agent builds P3
- "I want a **Narrative deck** structure" → agent builds P4

### Pattern composition rules
- **Don't mix patterns within one deliverable** unless the user explicitly asks. A pitch deck that suddenly switches to dashboard layout breaks narrative coherence.
- **Patterns can be truncated.** A 5-slide pitch might use only slots 1-2-3-8 from P1. That's fine — skip the middle, keep the arc.
- **Theme applies across the whole pattern.** Don't switch themes between slides within one pattern instance.

---

## Relationship to other layers

```
Foundations (themes.md)     ←  visual tokens (color, type, spacing, shadow)
    ↓
Components (layouts.md)     ←  single-slide building blocks (31 layouts)
    ↓
Patterns (this file)         ←  multi-slide narrative recipes (8 patterns)
```

- **Foundations** answer "what does it look like?"
- **Components** answer "what single slide can I build?"
- **Patterns** answer "what sequence of slides tells this story?"

---

## Adding a new pattern

If you find yourself building the same 4-5 slide sequence repeatedly for a specific deliverable type, it may deserve to become a pattern. Criteria:
1. Used for ≥ 2 distinct deliverable types (not one-off)
2. Has a clear narrative arc (beginning → middle → end)
3. Can be themed independently of content

To propose: add a new `P<N>` entry above with the same structure (name, trigger, slot sequence, theme pairing).

---

## Swizzle / Open internals

Inspired by Astryx's "open internals" philosophy: components are built to be composed at any level, not locked behind a closed top-level API.

### How it works

Key sub-blocks in single-page layouts are annotated with `data-block-id` attributes. These mark reusable fragments that can be extracted ("ejected") from a template without copying the entire file.

**Currently tagged blocks:**

| `data-block-id` | Found in | What it extracts |
|---|---|---|
| `kpi-card` | `kpi-grid.html` | A single KPI card (label + counter + delta) |
| `hero-counter` | `stat-highlight.html` | The giant animated number block |
| `process-step` | `process-step.html` | A single numbered step card |
| `cta-buttons` | `cta.html` | The button group (primary + outline) |

### Ejecting a block

```bash
# Extract a single KPI card from the grid
./scripts/xdesign eject templates/single-page/kpi-grid.html kpi-card my-kpi.html

# Extract the CTA button group
./scripts/xdesign eject templates/single-page/cta.html cta-buttons my-buttons.html
```

The ejected block is a standalone HTML fragment that can be pasted into any other deck or prototype. It inherits the current theme's CSS variables, so it automatically matches the visual context.

### When to eject vs copy

- **Eject** when you need a single reusable fragment (one KPI card, one step, one button group).
- **Copy the whole layout** when you need the full slide structure (the entire 4-card grid, the entire process section).
- **Copy from another agent** when the block you need isn't tagged yet — open the source file and copy the relevant `<div>` manually.

### Tagging new blocks

When adding a new single-page layout, annotate reusable sub-blocks with `data-block-id`. Rules:
- Use kebab-case, descriptive names (`kpi-card`, not `card-1`).
- Tag at the coarsest useful granularity — a single card, not the whole grid.
- Document the new block in the table above.
