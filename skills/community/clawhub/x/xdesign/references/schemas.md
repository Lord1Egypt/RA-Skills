# XDesign — Schemas

This document pins down the on-disk and in-memory shapes XDesign relies on: the brand `DESIGN.md` format, the CSS Design Token contract Mode 2 prototypes must honor, the eval JSON, and the HTML output contract. Keep it here — agents reading this once should be able to validate any new artifact without re-deriving the rules.

If something isn't pinned here, treat it as an open question and ask the user before inventing a new convention.

---

## 1. Brand `DESIGN.md` schema

Path: `assets/design-md/<slug>/DESIGN.md` (58 brands in the current bundle; see `references/design-system-catalog.md` for the index).

| Section | Required? | Purpose |
|---|---|---|
| `# <Brand> — Design System` heading | yes | Anchor for grep / TOC |
| `## 1. Visual Theme & Atmosphere` | yes | 2–4 paragraph narrative capturing mood, hero style, what makes the brand visually distinct. Used as the prompt seed in Mode 2. |
| `## 2. Color Palette & Roles` | yes | Subsections: Primary, Brand & Dark, Accent, Interactive, Neutral, Surface & Borders, Shadow Colors. Each color listed as `- **Name** (\`#hex\`): role description.` |
| `## 3. Typography Rules` | yes | Font family (with fallbacks), OpenType features (`"ss01"`, `"tnum"`, etc.), a hierarchy table (Role / Font / Size / Weight / Line Height / Letter Spacing / Features / Notes), and 3–6 principles |
| `## 4. Component Stylings` | yes | Subsections per component (Buttons, Cards, Badges, Inputs, Navigation, …) with exact paddings, radii, shadows, hovers |
| `## 5. Layout & Spacing` | recommended | Section padding, max-width, grid columns, breakpoints |
| `## 6. Motion & Interaction` | recommended | Easing curves, transition durations, hover/press behaviors |
| `## 7. Responsive Rules` | recommended | Mobile/tablet/desktop deltas, font scaling |
| `## 8. Iconography & Imagery` | recommended | Icon style, photo treatment, illustration rules |

### Rules for the body of each section

- Colors **must** be quoted hex (`#533afd`) or `rgba()` literals — agents grep these to extract tokens.
- The hierarchy table **must** keep the column header order above; tools parse it row-by-row.
- Component rules quote concrete CSS values (e.g. `Padding: 8px 16px`), not vibes.
- Avoid TODO / TBD tokens — leave the section out instead. Half-filled sections mislead the model more than missing data.

### Minimal example (for new brands)

```markdown
# ACME — Design System

## 1. Visual Theme & Atmosphere
ACME is loud, playful, and slightly absurd. The homepage leads with a single oversized wordmark in coral on cream, then drops the user straight into a 4-up tile grid of products. The page never takes itself too seriously.

## 2. Color Palette & Roles
### Primary
- **Coral** (`#ff6a3d`): CTAs, brand moments, primary accent
- **Cream** (`#fff6e8`): page background
- **Ink** (`#1a1a1a`): body text and headings

### Surface & Borders
- **Border Default** (`#f1d9b8`): warm 1px borders
- **Shadow Coral** (`rgba(255,106,61,0.25)`): signature elevation

## 3. Typography Rules
- **Primary**: `Söhne`, fallback `system-ui, sans-serif`
- OpenType: `ss01` enabled globally
- Hierarchy:
  - Display Hero — 56px / weight 700 / -1.0px tracking
  - Body — 16px / weight 400 / 1.45 line-height

## 4. Component Stylings
### Buttons
- Background: `#ff6a3d`, text `#fff6e8`, radius `999px`, padding `12px 20px`
- Hover: `#e85826`

### Cards
- Background `#fff6e8`, border `1px solid #f1d9b8`, radius `16px`
- Shadow: `0 4px 20px rgba(255,106,61,0.18)`
```

> **Why this format**: the column order in section 3, the `- **Name** (\`hex\`)` line shape in section 2, and the literal CSS in section 4 are all stable enough that a regex extractor could build a `tokens.css` from a brand file in <100 lines. Don't reformat the existing 58 files unless you're prepared to update the extractor too.

---

## 2. CSS Design Token contract (Mode 2)

Every Mode 2 prototype (`scripts/new-prototype.sh` scaffold, hand-written files, AI-generated HTML) **must** declare at minimum these CSS custom properties on `:root`. They form a minimum viable design system; consumers can override them per project.

```css
:root {
  /* Color */
  --color-bg:        #ffffff;   /* page background */
  --color-surface:   #f7f7f8;   /* cards, elevated surfaces */
  --color-text:      #0a0a0a;   /* primary text */
  --color-text-2:    #6b6b6b;   /* secondary text */
  --color-accent:    #3b5bff;   /* CTA, links, focus rings */
  --color-border:    #e5e5e5;   /* dividers, input borders */

  /* Geometry */
  --radius:          12px;      /* default corner radius */
  --radius-sm:        6px;
  --radius-lg:       20px;

  /* Elevation */
  --shadow:          0 1px 3px rgba(0,0,0,.04), 0 8px 24px rgba(0,0,0,.06);

  /* Type */
  --font-sans:       'Inter', system-ui, -apple-system, sans-serif;
  --font-mono:       'JetBrains Mono', 'SF Mono', Menlo, monospace;

  /* Spacing scale (4px base) */
  --space-1:         4px;
  --space-2:         8px;
  --space-3:        12px;
  --space-4:        16px;
  --space-6:        24px;
  --space-8:        32px;
  --space-12:       48px;
  --space-16:       64px;
}
```

### Why these specific tokens

- **`--color-*`**: naming uses semantic role, not hue. Never `#3b5bff` in a stylesheet; always `var(--color-accent)`. This is what lets brand overrides stay clean.
- **`--radius` / `--shadow`**: the two most-violated tokens when people freestyle. Pinning them prevents "this card looks like Material, that one looks like Stripe" inconsistency inside a single screen.
- **`--font-sans`**: one font family, not three. If the prototype needs a serif, add `--font-serif` explicitly; don't overload sans.
- **`--space-*`**: optional but recommended. Without a scale, paddings drift to 7px / 13px / 19px and the result looks hand-poked.

### How agents should treat this contract

- A prototype that ignores `--color-*` and uses `#000` everywhere is a quality-check failure.
- A prototype that adds *additional* tokens (e.g. `--color-success`) is fine and encouraged — just don't drop the required ones.
- When pre-filling tokens from a `DESIGN.md` (see `scripts/new-prototype.sh`), the script reads the brand's color section and maps Primary→`--color-accent`, Background→`--color-bg`, Heading→`--color-text`, etc. Anything unmapped stays at the defaults above.

---

## 3. `evals/evals.json` schema

Used for the qualitative eval suite (3–5 cases today, expandable). The full spec lives in `skill-creator/references/schemas.md`; what follows is the subset XDesign actually uses.

```json
{
  "skill_name": "x-design",
  "evals": [
    {
      "id": 1,
      "prompt": "User's natural-language task (full sentence, file paths, real names).",
      "expected_output": "One-paragraph description of what success looks like.",
      "files": [],
      "expectations": [
        "Verifiable statement about output (e.g. 'HTML opens in browser without a build step')",
        "Another verifiable statement (e.g. 'Uses tokyo-night theme for the tech sharing tone')"
      ]
    }
  ]
}
```

| Field | Type | Required | Notes |
|---|---|---|---|
| `skill_name` | string | yes | Must match the frontmatter `name` |
| `evals[].id` | integer | yes | Unique within the file |
| `evals[].prompt` | string | yes | Concrete, story-driven, never abstract (see skill-creator's "Good / Bad prompt" examples) |
| `evals[].expected_output` | string | yes | Human-readable success description |
| `evals[].files` | string[] | no | Paths to inputs, relative to skill root |
| `evals[].expectations` | string[] | yes | Each line is a check the grader can verify mechanically or by short string match |

> The skill-creator `grading.json` (`text` / `passed` / `evidence` fields) consumes these directly — don't rename them.

---

## 4. Trigger eval query schema

For the description-trigger optimization loop (`scripts/run_loop.py` from skill-creator). Stored as a separate JSON next to the qualitative evals — keep them apart so updating one doesn't break the other.

```json
[
  { "query": "full natural-language user request", "should_trigger": true  },
  { "query": "another full request",              "should_trigger": false }
]
```

### Mix rules (target 20 total, 8–12 each way)

- **Should trigger (positive)**: 4–5 explicit deck asks ("做一份 PPT"), 2–3 prototype asks ("design a landing page"), 1–2 animation asks, 1–2 vague-but-visual ("make this look better"), 1–2 from non-English-speaking personas.
- **Should not trigger (negative)**: near-misses that share keywords but need a different tool — "extract text from this PDF", "write me a Python script that does X", "review my resume", "summarize this paper", "set up a Postgres schema", "I need a brand name" (that's a naming skill), "fix this CSS bug" (that's a debugging skill).

Both directions must be **concrete and story-driven** (real names, file paths, jobs, industries). One-line abstract queries like "create a chart" test nothing.

---

## 5. Mode 1 deck HTML output contract

Every Mode 1 deliverable is a self-contained HTML file (or folder of related files) that renders correctly in any modern browser with **no build step**.

Required pieces:

| Piece | Why |
|---|---|
| `<!doctype html>` + viewport meta | Mobile/responsive sanity |
| `<link rel="stylesheet" href="…/deck-studio/assets/base.css">` | Token primitives |
| `<link rel="stylesheet" href="…/deck-studio/assets/fonts.css">` | Webfont imports |
| `<link id="theme-link" rel="stylesheet" href="…/deck-studio/assets/themes/<theme>.css">` | One theme, swappable with T |
| `<script src="…/deck-studio/assets/runtime.js"></script>` | Keyboard, presenter, theme cycle |
| One `<section class="slide">` per logical page | Runtime toggles `.is-active` |

Forbidden:

- Any external JS framework (no React, no Vue, no Svelte)
- Inline `<style>` blocks defining colors — use tokens
- CDN scripts beyond webfont CSS
- `file://` blockers (no `fetch()` of local files; pre-bundle or inline)
- Speaker notes outside `<div class="notes">`

A complete minimal starter lives at `deck-studio/templates/deck.html`. New decks should copy it, not author from a blank file.

---

## 6. Mode 2 prototype HTML output contract

Required pieces:

| Piece | Why |
|---|---|
| `<!doctype html>` + viewport meta | Mobile sanity |
| All 6 `--color-*` tokens declared on `:root` | Design contract (section 2) |
| `<script crossorigin src="https://unpkg.com/react@18.3.1/umd/react.development.js">` etc. (pinned with integrity hashes — see `references/mode-2-prototype.md`) | Interactivity |
| Component code in `<script type="text/babel" data-presets="env,react">` | No build step |
| A single `root` div + `ReactDOM.createRoot(...).render(<App />)` | Standard mount point |

Forbidden:

- Multiple font families without naming them in `--font-*` tokens
- A `--radius` of 0 (looks unfinished) and a `--radius` of 9999 (looks like a pill, almost always wrong)
- A prototype that hard-codes a brand's hex values inline instead of via tokens
- Importing from npm without a pinned version + integrity hash

---

## 7. Versioning

XDesign follows semver loosely:

- **Patch**: typo fixes, asset re-bundling, theme file additions
- **Minor**: new mode, new token, new script, new template
- **Major**: routing change, removal of a resource, breaking schema change

The bundled `deck-studio/` submodule tracks its own version in its README. Don't bump XDesign's version when only the submodule changes — note it in the `references/integration-guide.md` "Fused versions" table instead.
