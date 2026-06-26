---
name: ui-craft-pro
description: Design, refine, and implement better UI for websites, dashboards, apps, landing pages, and components by using a local design knowledge base plus a code-first implementation workflow. Use when the goal is not just to get style ideas, but to turn a chosen visual direction into real interface code that looks more polished, more intentional, and less like generic AI UI. Especially useful for choosing styles, colors, typography, layout patterns, UX guidelines, chart types, generating a project-specific design system, and then coding the UI to match that system.
---

# UI Craft Pro

Use this skill to make UI output look sharper and feel more deliberate.

This skill is not just for searching design references.
Its real job is:
1. choose a design direction that fits the product
2. turn that direction into a usable design system
3. implement code that actually follows that system
4. review the output so the final UI still matches the intended vibe

## What this skill contains

- `data/` — local design knowledge base: styles, colors, typography, charts, landing patterns, UX guidelines, product mappings, reasoning rules
- `scripts/search.py` — search + design-system entry point
- `scripts/core.py` — local BM25 search engine over the CSV data
- `scripts/design_system.py` — design-system generator that combines product type, style direction, color, typography, and anti-pattern guidance
- `scripts/style_signature.py` — compact style-cloning brief generator for "X-like but mine" work
- `references/implementation-patterns.md` — how to translate a chosen design system into real code
- `references/review-checklist.md` — post-build review checklist to catch drift and weak output
- `references/product-archetypes.md` — how to correct mismatched first-pass results for product types that need calmer or more specific taste

## Core rule

Do not stop at “the search result says X”.
Use the result to drive the actual implementation.

When using this skill for real UI work, the expected path is:
- understand the product
- generate or infer the design system
- map that system into code
- check whether the final UI still matches the system
- then ship or refine

## Workflow

### 1) Understand the product first
Before touching visuals, identify:
- what the product is
- who it is for
- what mood it should give off
- whether the stack is fixed already

If the user already gave a strong direction, do not overcomplicate it. Use that direction and sharpen it.

### 2) Generate a design system early
For new pages, dashboards, flows, or landing pages, start here:

```bash
python3 skills/ui-craft-pro/scripts/search.py "<product + style keywords>" --design-system -p "<project name>"
```

Examples:

```bash
python3 skills/ui-craft-pro/scripts/search.py "gaming landing page bold neon competitive" --design-system -p "Neon Rift"
python3 skills/ui-craft-pro/scripts/search.py "AI dashboard modern premium dark" --design-system -p "Aira Ops"
python3 skills/ui-craft-pro/scripts/search.py "fintech mobile app minimal trustworthy" --design-system -p "Wallet App"
```

Use the result to lock in:
- layout pattern
- style direction
- color palette
- typography pairing
- interaction feel
- anti-patterns to avoid

### 3) Correct bad first-pass matches when needed
Sometimes the first generated result is technically plausible but emotionally wrong.
That is a correction problem, not a reason to abandon the workflow.

When this happens:
1. identify the real product archetype
2. run narrower domain searches
3. lock a corrected direction
4. then continue into implementation

Read `references/product-archetypes.md` when the first result drifts toward generic app-store, generic SaaS, or any style that does not fit the product’s real emotional center.

### 4) Lock implementation decisions before coding
After choosing the direction, define the implementation layer clearly.
At minimum, lock:
- color tokens
- typography roles
- spacing rhythm
- radius and shadow system
- section structure
- component treatment
- motion intensity

Read `references/implementation-patterns.md` when moving from design direction into real UI code.

### 5) Drill into a single domain only when needed
If implementation needs more detail, search one domain directly:

```bash
python3 skills/ui-craft-pro/scripts/search.py "<query>" --domain style
python3 skills/ui-craft-pro/scripts/search.py "<query>" --domain color
python3 skills/ui-craft-pro/scripts/search.py "<query>" --domain typography
python3 skills/ui-craft-pro/scripts/search.py "<query>" --domain landing
python3 skills/ui-craft-pro/scripts/search.py "<query>" --domain ux
python3 skills/ui-craft-pro/scripts/search.py "<query>" --domain chart
```

Use this when you need:
- a stronger visual direction
- a better palette
- a better font pairing
- a better landing-page section flow
- UX correction before or after coding
- chart guidance for dashboards

### 6) Translate the design system into code
This is the important part.

After choosing a direction, map it into implementation decisions such as:
- color tokens / CSS variables / Tailwind tokens
- typography roles for headings, body, labels, metadata
- spacing rhythm
- corner radius / shadow depth / border treatment
- section structure
- component behavior
- hover/focus/active states
- motion intensity

Do not code a random pretty page after generating a design system.
Code in a way that clearly reflects the chosen style.

### 7) Keep the implementation coherent
While coding:
- keep one main visual language
- do not mix unrelated styles randomly
- keep type, spacing, contrast, and component treatment consistent
- preserve usability while making it look better
- avoid overdoing effects that hurt readability or feel gimmicky

### 8) Review the result before calling it done
Before shipping or reporting back, check:
- does the final UI still match the chosen direction?
- does it feel generic or intentional?
- are the primary sections/components visually coherent?
- are there obvious UX or readability issues?
- did the implementation accidentally drift away from the design system?

Read `references/review-checklist.md` for the final pass.
If the page still feels bland, refine hierarchy and consistency before adding flair.

## Default behavior when using this skill

Prefer this order internally:
1. understand the ask
2. infer or generate direction
3. correct drift if needed
4. lock implementation choices
5. implement the UI
6. review the result
7. present the result simply

Do not dump raw search results unless they are directly useful.
Use them to improve judgment and implementation.

## High-value domains

- `product` → product type and expected design language
- `style` → visual direction, mood, effects, compatibility, complexity
- `color` → palettes aligned to product type and emotional tone
- `typography` → font pairing and reading hierarchy
- `landing` → section order, CTA placement, conversion structure
- `ux` → best practices and anti-patterns
- `chart` → chart choice for dashboard/data work
- `google-fonts` → font discovery
- `icons` → icon direction
- `react` / `web` → implementation guidance when useful
- `design-systems` → reference systems worth studying by product context
- `style-signatures` → "X-like but mine" style DNA
- `patterns-shells` → reusable page/app structural patterns
- `anti-generic-ui` → common AI-generic smells and fixes

## Notes

- This skill improves taste, structure, and consistency; it does not replace product judgment.
- For small UI tweaks, you may not need the full workflow. Use the guidance and ship.
- For bigger UI tasks, run `--design-system` first so the result has a coherent visual language.
- If the first result is wrong, correct it with narrower domain search instead of throwing the whole process away.
- If the user asks whether a design direction is good, answer directly.
- If the user asks to build the UI, use this skill to guide both design choices and code choices.
ult has a coherent visual language.
- If the first result is wrong, correct it with narrower domain search instead of throwing the whole process away.
- If the user asks whether a design direction is good, answer directly.
- If the user asks to build the UI, use this skill to guide both design choices and code choices.
esult has a coherent visual language.
- If the first result is wrong, correct it with narrower domain search instead of throwing the whole process away.
- If the user asks whether a design direction is good, answer directly.
- If the user asks to build the UI, use this skill to guide both design choices and code choices.
ult has a coherent visual language.
- If the first result is wrong, correct it with narrower domain search instead of throwing the whole process away.
- If the user asks whether a design direction is good, answer directly.
- If the user asks to build the UI, use this skill to guide both design choices and code choices.
