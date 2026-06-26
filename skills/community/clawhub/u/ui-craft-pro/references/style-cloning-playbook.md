# Style Cloning Playbook

Use this when the goal is to study a strong public design language and turn it into your own implementation system.

## Core rule
Do not clone pixels first.
Clone the design language in this order:
1. spacing rhythm
2. typography hierarchy
3. surface treatment
4. component behavior
5. motion intensity
6. only then visual accents

If you copy colors or effects before rhythm and hierarchy, the result usually feels fake.

## What to extract from a source system
For each reference system or product, capture:
- product type
- audience
- emotional tone
- primary use context
- color strategy
- spacing rhythm
- radius scale
- border density
- shadow depth
- typography roles
- icon style
- component tone
- section sequencing
- motion level
- accessibility posture
- what makes it feel distinct
- what would break if copied carelessly

## Safe cloning loop
### 1) Choose the right source
Pick a source that matches the product reality.
- do not clone Linear for a trust-heavy government form
- do not clone USWDS for a cinematic launch page
- do not clone Stripe gradients for a dense admin table UI

### 2) Write a style signature first
Before implementation, summarize the source in a compact signature:
- mood
- token DNA
- layout DNA
- component DNA
- motion DNA
- anti-patterns

### 3) Translate signature into tokens
Lock:
- color tokens
- spacing tokens
- radius scale
- shadow scale
- type scale
- motion scale

### 4) Translate tokens into component rules
Define how the chosen style affects:
- buttons
- cards
- forms
- tabs
- sidebars
- empty states
- modals
- tables
- navs

### 5) Preserve the source logic, not the source branding
Good cloning means:
- similar rhythm
- similar clarity
- similar pacing
- your own brand colors, copy, and details

Bad cloning means:
- obvious one-to-one copy
- same screenshots/illustrations
- same decorative quirks without the structural logic

## Quick teardown prompts
Ask these before coding:
- What makes this system feel expensive or trustworthy?
- Is it type-led, grid-led, or effect-led?
- Are surfaces mostly flat, bordered, elevated, or translucent?
- Does the system win through calmness, density, or spectacle?
- Which 3 things are essential to preserve?
- Which 3 things should not be copied literally?

## Cloning by layer
### Layer 1 — Rhythm
Study padding, gaps, section spacing, content width, and density.

### Layer 2 — Hierarchy
Study headline scale, label sizes, metadata treatment, and CTA prominence.

### Layer 3 — Surfaces
Study background contrast, border treatment, radius, and shadow depth.

### Layer 4 — Components
Study how buttons, inputs, cards, tables, and navigation feel as a family.

### Layer 5 — Motion
Study whether motion is invisible, helpful, premium, playful, or dramatic.

## Source families worth studying
A useful cloning library should cover multiple source families, not just one flavor of SaaS.
At minimum, keep references across:
- developer systems (GitHub, Vercel, Resend, Segment)
- enterprise workflow systems (Polaris, Atlassian, Carbon, Fluent)
- command/productivity tools (Linear, Raycast, Superhuman)
- knowledge/content systems (Notion, Perplexity, Apple docs)
- creative/premium launches (Stripe, Framer, Arc)
- universal system foundations (Material, Radix, Base UI, USWDS)

## Output expectation
A good cloning pass should produce:
- a named style direction
- a token set
- component rules
- layout guidance
- anti-pattern warnings
- a result that feels inspired by the source, not trapped under it
