# Design-System Routing

Decide this at Step 3 (after the register split) and record it as `design_system:` in
`.ulpi/design/DESIGN.md`. Choosing an established component system for `product`-register work is a
major consistency + accessibility win — the build inherits a vetted, accessible component model instead
of reinventing one. The chosen system is part of the build handoff: the delegated engineering agent
builds ON it (this skill does not implement it).

## Rule

- `product` register → reach for ONE established system.
- `brand` register (landing / marketing / portfolio) → bespoke is fine; identity is the product.
- **Honesty rule:** never spec a hand-recreation of a system's components. Name the system, build on
  it, and spend identity on tokens (color, type, radius, motion) + the Signature.

## Brief → system map (pick one; not exhaustive)

| Brief / product type | Reach for | Why |
|----------------------|-----------|-----|
| SaaS app / general dashboard | Radix + shadcn/ui | headless + your tokens on top; full control |
| Enterprise / data-dense | Carbon (IBM) or Material 3 | dense tables, mature patterns |
| Microsoft ecosystem | Fluent UI | native platform feel |
| Commerce / merchant admin | Polaris (Shopify) | merchant conventions |
| Developer tool / GitHub-like | Primer | familiar to the audience |
| Government / public sector | GOV.UK Design System / USWDS | compliance + accessibility baked in |
| iOS native | Apple HIG + SwiftUI system components | platform-native |
| Android native | Material 3 | platform-native |
| Marketing / landing / portfolio (`brand`) | bespoke — no system | the look IS the product |

If none fit, default to **Radix primitives + your tokens** for product UIs (accessible, unopinionated)
and record the reasoning.

## Record it

- Set `design_system:` in `.ulpi/design/DESIGN.md` frontmatter (system name, or `bespoke`).
- In the build handoff, state: which system, its install/setup note, and "theme it with our locked
  tokens — do NOT re-implement its components."
