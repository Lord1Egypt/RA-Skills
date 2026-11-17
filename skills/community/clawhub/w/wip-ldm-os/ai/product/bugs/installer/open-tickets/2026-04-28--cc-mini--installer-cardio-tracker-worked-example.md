# Worked example: cardio tracker as bespoke agent composition

**Date:** 2026-04-28
**Owner:** unassigned
**Status:** open
**Master plan:** [2026-04-28--cc-mini--installer-eight-interfaces-master-plan.md](2026-04-28--cc-mini--installer-eight-interfaces-master-plan.md)

## Why this exists

Karpathy's vibe-coded cardio dashboard (1 hour today, should be 1 minute) is the canonical illustration of the vision: bespoke, personal, disposable software assembled from agent-native sensors and actuators. It is the cleanest test case for whether the universal-installer model serves the destination or just describes the plumbing.

A compact sketch already lives in [`docs/universal-installer/SPEC.md ... Worked example (compact sketch)`](../../../docs/universal-installer/SPEC.md#worked-example-compact-sketch). This ticket carries the full version so the SPEC.md sidebar stays compact and the vision narrative stays coherent.

## What

Write the full worked example as a standalone doc (location TBD: most likely `docs/universal-installer/examples/cardio-tracker.md` or under `ai/product/product-ideas/`). Walks the user prompt → bespoke artifact path end-to-end, naming every layer the universal-installer spec defines.

## Scope of the example

User prompt (verbatim, paraphrased from the source narrative):

> *"Help me track my resting heart rate over the next 8 weeks. Goal: 50 → 45 bpm. Zone 2 cardio + 1 HIIT/week."*

Walk the agent's actual path:

1. **Personal context (Memory Crystal):** RHR baseline, prior cardio experiments, units preference (imperial/metric), health constraints, calendar.
2. **Service resolution (Catalog → Install Spec → Universal Interface):** Woodway treadmill data. Catalog resolves the slug. Install spec URL teaches the agent how to authenticate and pair. Treadmill exposes Remote MCP (#4) for workout data.
3. **Time/calendar semantics:** explicit timezone, ISO dates, week boundaries, the 8-week experiment window.
4. **Composition:** agent assembles a disposable dashboard (~300 lines). Pulls Woodway data, filters to the experiment window, computes Zone 2 minute totals, plots progress vs. target.
5. **Sanity checks:** units consistent, dates aligned to the user's calendar week, RHR trend chart matches Memory Crystal's stored baseline.
6. **Persistence:** the bespoke dashboard is the agent's output, not a Universal Interface product. It lives wherever the user keeps personal automations. The agent maintains it for the experiment duration.

Each step names the layer it's drawing from, so the doc doubles as a tour of the architecture.

## What this example must demonstrate

- The user does **not** browse or pick an app.
- The agent does **not** invent capability ... it composes capability that already exists as Universal Interfaces.
- Personal context comes from a sibling LDM OS component (Memory Crystal), not the universal-installer.
- The Woodway treadmill (or any sensor) is consumed via its declared interface (Remote MCP #4 in the ideal world; today via reverse-engineered cloud API as a temporary bridge).
- The bespoke dashboard is **out of scope** as a Universal Interface product. It is the destination, not part of the spec.

## Acceptance

- A new AI reading the worked example can articulate the primary flow (outcome → resolve services → install/auth → bespoke artifact) without seeing any other vision doc.
- The example references concrete services (Woodway, Memory Crystal, calendar) and concrete interfaces (Remote MCP, Skill, Catalog, Install Spec).
- It reads as one tight narrative, not a feature list.
- A reader can answer the vision-comprehension gate in the master plan: "Why is 'cardio experiment tracker' not a product category we ship?"

## Open questions

- Does the example live under `docs/universal-installer/examples/` (canonical, agent-readable) or under `ai/product/product-ideas/vision-quest-01/` (vision narrative, less agent-facing)? Probably both: short version in `docs/`, narrative version in `ai/`.
- Should the example also include the broken/recovery path (units mistake, calendar mismatch ... the actual debugging Karpathy hit) so the doc admits the rough edges and names what the install/spec story would have prevented? Worth doing; it makes the gap to the 1-minute version concrete.

## Linked

- [Master plan: eight interfaces alignment](2026-04-28--cc-mini--installer-eight-interfaces-master-plan.md) (vision-comprehension gate is here)
- [`docs/universal-installer/SPEC.md ... Worked example (compact sketch)`](../../../docs/universal-installer/SPEC.md#worked-example-compact-sketch) (the compact version that points here)
