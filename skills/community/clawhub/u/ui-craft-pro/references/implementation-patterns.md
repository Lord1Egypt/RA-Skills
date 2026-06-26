# Implementation Patterns

Use this file when you need to turn the chosen design system into real interface code.

## 1) Lock tokens before coding

After generating a design system, define a small token set first.

Minimum token groups:
- colors
- typography
- spacing
- radius
- shadow
- border
- motion

Example mapping:

- colors
  - `--bg`
  - `--surface`
  - `--text`
  - `--muted`
  - `--primary`
  - `--secondary`
  - `--cta`
- typography
  - heading font
  - body font
  - mono/data font if relevant
  - heading sizes
  - body sizes
- radius
  - small / medium / large
- shadow
  - subtle / medium / strong
- motion
  - hover duration
  - transition curve
  - reduced-motion fallback

Do not start component styling before token choices are stable.

## 2) Map style direction into component behavior

Translate the selected style into concrete component rules.

Examples:

### Minimal / premium
- fewer sections
- more whitespace
- restrained copy
- one strong CTA
- quiet borders
- soft shadow depth
- typography carries hierarchy more than decoration

### Gaming / bold / high-energy
- larger headings
- stronger contrast
- more assertive CTA treatment
- card blocks with clear visual rhythm
- motion can be more visible, but keep readability first

### Liquid-glass / translucent
- use blur intentionally, not everywhere
- keep text on strong-contrast surfaces
- treat glass as accent structure, not as the entire UI
- watch accessibility and performance carefully

## 3) Decide section structure before polishing visuals

For landing pages, lock the section order early.

Common structures:
- hero → benefits → CTA
- hero → proof → feature blocks → CTA
- hero → narrative/story → product advantages → CTA

Do not keep adding sections because the page feels empty.
If the pattern is minimal, let whitespace do the work.

## 4) Keep component families coherent

Within one page, keep these aligned:
- button treatment
- card treatment
- input treatment
- icon style
- radius scale
- border density
- shadow depth

If one button feels premium-glass and another feels default SaaS, fix it.

## 5) Tune for the real stack

### Astro
- Prefer page composition with reusable sections/components.
- Put tokens in a global stylesheet or layout-level CSS variables.
- Keep page sections clean and readable; avoid burying style rules inside many isolated files unless needed.

### React / Next
- Centralize tokens in theme variables or Tailwind config.
- Avoid component-by-component visual drift.
- If using a component library, restyle the library to match the selected design system instead of mixing defaults with custom pieces.

### Tailwind
- Convert palette, radius, shadow, and typography into reusable utilities/config where possible.
- Reuse classes through components or extracted patterns instead of one-off utility soup for every section.
- If the page relies on one special effect, make it reusable.

## 6) Implementation sanity rules

Before saying the UI is done:
- check contrast
- check focus-visible states
- check hover/active states
- check mobile spacing
- check if motion is tasteful
- check if the page still feels like the chosen style

If the page feels generic, identify which layer drifted:
- tokens
- hierarchy
- layout
- components
- motion
