---
name: taste-pm
description: "Use when designing a product's structure, information architecture, page layout, entry points, or user-experience flow — turning a business or feature need into a product design for web or app. Triggers include 'design a product', 'how should this feature be laid out', 'where does the entry point go', 'product structure', 'information architecture', 'how to design the pages', 'what's the user flow', or doing product-manager work for a web product. Not for visual styling (use a UI skill) or backend implementation."
---

# taste-pm · Product Design With Taste

## What this is

Turn a business need or feature idea into a product design **with taste** — an information architecture and interaction model that's clean, frictionless, and instant.

**Core belief: the real problems in product design live in the information architecture and the interaction**, not in the pixels and not in the API. How a feature gets built is an engineering problem; visual styling belongs to a UI skill. This skill owns the layer in between: **who has what problem → the one thing the user most wants to do → where the entry point goes → how a pile of features gets arranged into pages → how the user moves from start to finish.**

ByteDance products (Douyin, Coze, Doubao, Jimeng/Dreamina, Hongguo, Feishu, …) are the best living examples of this craft, so they serve as the source of judgment calls and case studies. See the case-study reference (`references/产品拆解案例.md`).

## When to use / when not

**Use it** to: design the structure of a new product or feature; decide entry points, information architecture, page layout, and user flow; review whether a product structure holds up; do product-manager work for a web product.

**Don't use it** for: visual styling, color, component aesthetics (→ a UI skill); backend, APIs, tech selection (→ engineering); pure copywriting.

## Iron rule: hold the line at *this* layer

When designing, **output product structure and interaction only** — don't drift:

- ❌ Don't write tech stack / database / backend architecture (unless the user explicitly asks).
- ❌ Don't expand on business model / pricing / growth spend (at most a one-liner in step ① for "what winning looks like").
- ❌ Don't hand out visual specs / colors / font sizes.
- ✅ Output only: value definition, product classification, entry, an IA diagram, page layout, a UX flow diagram, and a landing component list.

Drifting into engineering and business model is the #1 failure mode for this skill — **if the IA and interaction aren't nailed down, no amount of tech and business talk is anything but off-topic.**

## The six steps (follow strictly when invoked)

Guiding principle: **value before features. Ask "who has what problem" first, then "where it goes and how it's tapped."** Tie every step back to this anchor. At each decision point, ask the user (one question at a time, multiple-choice preferred) — don't guess on their behalf.

**① Define the problem** — lock onto value, not features
- Pin the user down to "segment + scenario + the triggering moment." "Everyone" is banned.
- Real pain or fake need? A cool feature that solves no real problem gets cut.
- Write the core value in one line: what does the user **walk away with**.
- Note "what winning looks like" in one line (no data-system deep dive).

**② Lock the core action + classify the product** — this determines every pattern downstream
- The single highest-frequency, must-have action the user can state in one sentence.
- Classification (sets the skeleton in step ④): **consumption / creation-tool / conversational-assistant / generation / transaction / collaboration**.
- The core action = what the first screen should do.

**③ Design the entry** — make the core action reachable in zero taps
- Consumption-first: opening the app lands on a usable default state — **don't hand the user a multiple-choice question** (no blank home page, no menu lobby).
- Core action reachable in 0–1 taps. Ask back: when the user opens this, where does their finger go first?

**④ Arrange features + information architecture** — trunk, branches, how it's packed (**the center of gravity**)
- First split trunk vs. branches: a product can have only one trunk flow; everything else is a branch.
- **Pick the layout skeleton straight from the step-② classification** (the single most critical move for a web product):

  | Product type | Layout skeleton | Exemplar |
  |---|---|---|
  | Consumption (mobile) | Bottom 5 tabs: `main feed / discover / ➕create / messages / me`, ≤5, thumb-reachable, "me" rightmost holding personal assets | Douyin / Hongguo / Soda |
  | Conversational assistant (web) | Center conversation area + bottom-centered input box (`/` for skills, `+` for multimodal) + left session list + feature cards surfaced on the first screen | Doubao |
  | Creation tool (web) | Three-pane workbench: left config / center authoring canvas / right live debug-preview + resource library + template store | Coze |
  | Generation (web) | Params-left, results-right: prompt + parameters on the left, results gallery on the right, results editable in place | Jimeng / Dreamina |
  | Collaboration / admin console (web) | Left sidebar + content area, nav draggable and collapsible | Feishu |

- Pull the **business / incentive engine out as a top-level entry** (Hongguo's "Rewards," e-commerce's "Cart") so the path to money is one hop.
- Consumption-type feed-form selection, card information density, and the web-tool low-barrier rule → see the pattern-library reference (`references/字节产品范式库.md`).
- **You must produce an IA diagram** (tab / page tree). Do not stop at a flat feature list.

**⑤ Wire the experience flow** — how the user moves from start to finish
- Draw the core action as a step-by-step path; count how many steps it takes.
- Instant feedback: animate interactions, refresh numbers live.
- **In-place overlays first**: comments / actions / confirmations happen in overlays so the user never leaves the main stage ("stay inside the content"). If it can be done in place, never push a new stack.
- Short paths + closed-loop jumps: consumption → creation → transaction → personal page/assets, wired into a loop.
- **You must produce a UX flow diagram** (key path + jumps).

**⑥ Land it on the component vocabulary** — how ByteDance ships it
- React / admin console defaults to **Semi Design**; for Vue or an off-the-shelf admin scaffold use **Arco** (note: Arco's community has largely stalled since 2025 — pin the version, plan to self-maintain).
- Standard skeleton `Layout` = top bar + sidebar + content area; 24-column grid; 8px-multiple spacing. Component-selection cheat sheet and tokens → see the design-system reference (`references/设计系统落地词汇表.md`).

## Output format

Produce a **structured product design doc** (not prose). Template in `assets/产品设计稿模板.md`:
1. Core value (one line)
2. User & scenario & what winning looks like
3. Core action + product classification
4. Entry design (what the first screen shows)
5. **IA diagram** (tab / page tree)
6. Core page layout (skeleton + feed form + cards)
7. **UX flow diagram** (key path step-by-step + closed-loop jumps)
8. Landing component list

Voice: like a senior PM — decisive, gives the judgment call, no waffle, no inspirational fluff.

## Common mistakes (observed in baseline testing)

| Mistake | Correction |
|---|---|
| Wanders off into tech stack / database / backend architecture | That's the engineering layer, not this skill. Stop, return to the IA. |
| Expands on business model / pricing / spend | One line for "what winning looks like" in step ① at most. Don't expand. |
| Lists features flat and calls it done | No IA diagram = no product design. Features must become a page tree + entry + flow. |
| Designs without classifying the product first | Do step ② classification first, then pick the skeleton from the step-④ table. Wrong skeleton, wrong everything. |
| First screen is a blank home page / menu to choose from | Violates "usable on open." The core action must be reachable in zero taps. |
| Hands over static pages with no interaction flow or instant feedback | Must produce a UX flow diagram + instant feedback + in-place overlay design. |

## Red flags — stop the moment one appears

- "Technically we could use Vue + FastAPI…" → stop, nobody asked about engineering.
- "For the business model, I'd suggest Freemium…" → stop, off-topic.
- About to wrap up right after listing feature modules → where's the IA diagram and the flow diagram?
- Haven't said "what the first screen shows" → the entry isn't designed.
- Designed two trunk flows for one product → cut it down to one.

## References

- `references/字节产品范式库.md` — pattern library: layout-skeleton selection, the 5-tab template, single/double-column criteria, the Toutiao card library, instant feedback, in-place overlays, closed-loop jumps, the web low-barrier rule.
- `references/产品拆解案例.md` — real structural teardowns of 13 ByteDance products (Douyin, Toutiao, Soda, Hongguo, Fanqie, Coze, Doubao, Jimeng, CapCut, Trae, Maoxiang, Douyin E-commerce, Feishu).
- `references/设计系统落地词汇表.md` — Semi vs. Arco selection, the standard layout skeleton, the component cheat sheet, tokens, the ByteDance web stack.
- `assets/产品设计稿模板.md` — the structured design-doc template for output.
