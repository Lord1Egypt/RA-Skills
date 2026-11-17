---
title: "Structs UI: dashboards, forms, and HUDs"
meta_description: For building, not playing. Dashboards, forms, menus, HUDs and clients using SUI, the design system the game itself is built with.
name: structs-ui
description: Building interfaces and clients in the Structs universe — dashboards, forms, menus, HUDs, and companion apps using SUI, the design system the game itself is built with. Use when asked to build, style, or extend any Structs UI, or when writing client code that signs transactions, computes proof-of-work, or consumes GRASS events. This is about building software, not playing the game.
level: advanced
domain: build
---

# Structs UI: dashboards, forms, and HUDs

You are being asked to **build something**, not to play. This skill routes you to the
reference material for making an interface that looks like Structs and a client that
behaves like one.

Everything below is verified against [structs-webapp](https://structs.ai/develop/repos),
the flagship client — not inferred from the API surface. When a doc and that codebase
disagree, the codebase wins.

**Not this skill?** If you want to build *structs* — the in-game machines — that is
[`structs-building`](https://structs.ai/skills/structs-building/SKILL). If you want to
use the Desktop MCP tools, that is [`TOOLS.md`](https://structs.ai/TOOLS).

## When to use it

- Building a dashboard, form, menu, HUD, or companion app for Structs.
- Styling anything so it reads as part of the Structs universe.
- Writing client code that signs transactions, computes proof-of-work, or listens to
  GRASS.
- Extending Structs Desktop with a new MCP tool or board page.

## Decide these first

| Decision | Guidance |
|---|---|
| **UI or client?** | Visuals → the SUI pages. Chain, events, work → the client pages. Most real projects need both |
| **Scaling model** | The game renders at `scale(2)` above 1152px. At 1× SUI is half size. **Settle this before writing markup** — retrofitting is painful. [ui/](https://structs.ai/develop/ui/) |
| **Which SUI JS** | Import each class directly with `.js`. **Never import `SUI.js` outside a bundler** — it has an extensionless import that 404s and takes the module down. [ui/runtime](https://structs.ai/develop/ui/runtime) |
| **Serving assets** | SUI's URLs are root-absolute. From a subpath, every icon vanishes silently. Serve at root or rewrite. [ui/gotchas](https://structs.ai/develop/ui/gotchas) |
| **Extend or build fresh** | Adding to Structs Desktop is usually cheaper than a new app. [client/desktop-extensions](https://structs.ai/develop/client/desktop-extensions) |

## Five rules that make it look like Structs

1. **Nothing is rounded.** Hard edges, 1–2px borders, `border-radius: 0`.
2. **Emphasis is colour and case, never weight.** Font weight is 500 everywhere.
3. **Chrome is uppercase 8px ExtremeHazard; content is 16px DirectiveZero.**
4. **Colour comes from tokens and is semantic.** Teal is you, red is the enemy, amber is
   warning, gold is third parties. Never a hex literal.
5. **Density over whitespace.** This is an operations console, not a landing page.

And one that saves an hour: **never invent an icon.** There are 67 glyph icons and 29
sprite icons. If the concept has no glyph, use a text label — no emoji, no inline SVG.

## Where to go

**Interface** — [develop/ui/](https://structs.ai/develop/ui/)

| Need | Page |
|---|---|
| Colours, spacing, z-index, type | [tokens](https://structs.ai/develop/ui/tokens) |
| The two icon inventories | [icons](https://structs.ai/develop/ui/icons) |
| Markup contracts for every component | [components](https://structs.ai/develop/ui/components) |
| Steppers, tooltips, the drawer | [runtime](https://structs.ai/develop/ui/runtime) |
| Why the layout is broken | [gotchas](https://structs.ai/develop/ui/gotchas) |
| Keeping a multi-page console coherent | [patterns](https://structs.ai/develop/ui/patterns) |
| Dashboard, form, menu, HUD, assembled | [recipes](https://structs.ai/develop/ui/recipes) |
| Runnable starter files | [examples](https://structs.ai/develop/ui/examples/README) |

**Client** — [develop/client/](https://structs.ai/develop/client/)

| Need | Page |
|---|---|
| The three-channel architecture | [index](https://structs.ai/develop/client/) |
| State, factories, the string-number trap | [state-and-data](https://structs.ai/develop/client/state-and-data) |
| Wallet, signing queue, charge gating | [actions-and-signing](https://structs.ai/develop/client/actions-and-signing) |
| Proof-of-work: hashing, difficulty, workers | [work-and-pow](https://structs.ai/develop/client/work-and-pow) |
| Real-time events and all 26 listeners | [realtime-grass](https://structs.ai/develop/client/realtime-grass) |
| PFP compositing, struct art, Lottie | [rendering-entities](https://structs.ai/develop/client/rendering-entities) |
| Ambits, tiles, fog of war | [map](https://structs.ai/develop/client/map) |
| Adding an MCP tool or board page | [desktop-extensions](https://structs.ai/develop/client/desktop-extensions) |

**Context** — [repos](https://structs.ai/develop/repos) (which repository to read, and
which wins) · [frontend-architecture](https://structs.ai/develop/frontend-architecture)
(the webapp's MVVM layer) · [maintenance](https://structs.ai/develop/maintenance) (how
these pages stay true)

## Traps, in the order you will hit them

- **Assets don't resolve.** Icons and form art vanish with no console error. Check
  `document.fonts.check('16px Structicons')` first, always.
- **Everything is centred.** `body { text-align: center }` is inherited by everything;
  only eleven rules re-assert left. Left-align data surfaces explicitly.
- **A flex item won't shrink.** `min-width: auto` is the default. `word-break` does
  nothing about it — you need `min-width: 0`.
- **Alert severity colours the icon but not the text.** The text hard-sets `--text-body`.
  Four CSS rules fix it; they are in
  [sui-patch.css](https://structs.ai/develop/ui/examples/sui-patch.css).
- **Copy the typos.** `--from-input-height-content` and
  `sui-message-system-model-frame-center` are the real names.
- **Two transactions at once gives `account sequence mismatch`.** Serialise — one in
  flight, one per block. Don't track sequence numbers.
- **Charge gates actions.** `currentBlock - (lastActionBlock + 1)`. Hold the queue until
  the confirmed last-action height has loaded, or the client will think it has infinite
  charge and empty its queue into one block.
- **Proof-of-work is cheaper if you wait.** Difficulty decays with anchor age. Initiate
  early, complete later.
- **Numbers arrive as strings.** Normalise once at the boundary. The reference client is
  inconsistent about this; don't copy that part.

## Before you call it done

- [ ] Every colour from a token, every icon from the real inventories
- [ ] Form controls unclassed inside `label.sui-input-text`; checkbox container is a `<div>`
- [ ] `tabular-nums` on numeric cells, `min-width: 0` on flex items with long text
- [ ] Empty, loading and error states share one component and look different from each other
- [ ] Sweep for overflow at your narrowest width — jsdom won't catch it, only a browser will
- [ ] Keyboard focus is visible somewhere (SUI removes the default and adds nothing back)
- [ ] Transaction failures reach the operator — the reference client's settled event has
      no listeners, so failures are silent by default

Full checklist: [ui/patterns](https://structs.ai/develop/ui/patterns#checklist-for-a-new-sui-surface).
