# Brand Asset Protocol

> **When to load:** The design task involves a real, identifiable brand or product.
> **Core principle:** Assets > color values. A logo and product photo carry more brand signal than a hex code extracted from memory.

---

## Why this protocol exists

Designs that reference real brands fail in two predictable ways:

1. **Hallucinated brand colors** — the model recalls "Stripe is purple" from training data, but the actual current palette may have shifted. The result looks almost-right but subtly off, and the user can't articulate why.
2. **Missing logos in comparison/evaluation content** — a "Top 5 AI Tools" deck where the logos are CSS shapes or emoji instead of real marks destroys credibility instantly.

This protocol forces a deterministic acquisition pipeline: **search → download → verify → freeze**. No guessing, no memory-based assertions.

---

## Trigger conditions (either one activates this protocol)

### Type 1: Designing FOR a brand
The user asks you to create materials for a specific company: "给 Stripe 做落地页", "design a DJI launch animation", "做一个 Notion 风格的 dashboard".

### Type 2: Designing WITH identifiable brands
The design itself will display one or more real, recognizable products/brands — even if the user's own brand is different. Examples: comparison charts, "Top N" rankings, evaluation decks, integration grids, ecosystem maps.

**Hard rule:** If the design will show even one recognizable product name, that product's official logo is a **required asset**, not optional. "出现几个就取几个" — if five brands appear, fetch five logos.

**This applies even inside the Direction Advisor fallback flow** — the Advisor decides visual *style*, but it does not exempt you from fetching logos for named brands.

---

## The 5-step hard flow

### Step 1 — Ask (one batch, before searching)

Ask the user for the full asset checklist in a single message:

| Asset type | Ask for |
|---|---|
| Logo | SVG preferred, PNG with transparency acceptable |
| Product photos | Official renders, not stock or AI-generated lookalikes |
| UI screenshots | If the design needs to show the product interface |
| Color palette | Official brand guidelines, if available |
| Typography | Official font family or licensed webfont |
| Restrictions | Usage禁区, do-not-use colors, style guidelines |

If the user provides any of these, skip to Step 4 for those assets. If the user says "你看着办" or provides nothing, proceed to Step 2.

### Step 2 — Search official channels

For each brand in scope, search these locations **in order**:

| Priority | Source | URL pattern | Best for |
|---|---|---|---|
| 1 | Brand/press page | `<brand>.com/brand`, `brand.<brand>.com`, `<brand>.com/press` | Official logos, color values, guidelines |
| 2 | Official media kit | `<brand>.com/press-kit`, `<brand>.com/media` | High-res logos, product renders |
| 3 | SVG logo repositories | `svgl.app/api/<brand>`, `simpleicons.org` | Clean vector logos (dev brands especially) |
| 4 | Favicon fallback | `https://www.google.com/s2/favicons?domain=<brand>.com&sz=128` | Last-resort small logo |

**For product photos** (hardware, physical products):
| Priority | Source | Best for |
|---|---|---|
| 1 | Official product page | Press renders, spec sheets |
| 2 | Official social media | Launch images, lifestyle shots |
| 3 | Wikimedia Commons | Public domain / CC-licensed imagery |

### Step 3 — Download (three fallback paths)

For **logos**:
1. SVG from official source or svgl.app → embed as inline SVG or local file
2. If SVG unavailable → PNG with transparency from press kit
3. If PNG unavailable → favicon (small, but real)

For **product photos**:
1. Official press render (highest priority — these are designed to be used)
2. Official product page screenshot (if renders unavailable)
3. Wikimedia Commons (for historical/public domain products)

For **color values**:
1. Grep the official website's CSS for `#xxxxxx` patterns
2. Extract from downloaded SVG logo (`fill="..."`, `stop-color="..."`)
3. Sample from official product screenshot using a color picker

**Never skip to "I'll just use the color I remember."** If all three paths fail, tell the user and ask them to provide the value.

### Step 4 — Verify

Before accepting an asset, verify its authenticity:

- **Logo:** Does it match the brand's current identity? Cross-reference with the official website header. Outdated logos (pre-rebrand) are a common failure.
- **Product photo:** Is it the actual product, not a competitor's or a generic stock image? Check model numbers, design language consistency.
- **Color:** Was it extracted from a real source (CSS, SVG, screenshot), not recalled from memory? Hex values from training data drift over time.

**Checkpoint:** If any asset fails verification, stop and re-acquire. Do not proceed with a placeholder that looks "close enough."

### Step 5 — Freeze as `brand-spec.md`

Write all acquired assets into a project-level `brand-spec.md` file. This becomes the single source of truth for the rest of the design.

**Template:**

```markdown
# Brand Spec: <Brand Name>

## Assets
- **Logo (SVG):** `assets/<brand>-logo.svg` — [source URL]
- **Logo (PNG):** `assets/<brand>-logo.png` — [source URL, if SVG unavailable]
- **Product photo:** `assets/<brand>-product.jpg` — [source URL]

## Color Palette (extracted from [source])
- **Primary:** `#XXXXXX` — [role: CTA, header bg, etc.]
- **Accent:** `#XXXXXX` — [role]
- **Neutral Dark:** `#XXXXXX` — [role]
- **Neutral Light:** `#XXXXXX` — [role]

## Typography
- **Primary font:** `<font name>`, fallback `<web-safe stack>`
- **Source:** [official / Google Fonts / licensed]

## CSS Variables (paste into :root)
:root {
  --brand-primary: #XXXXXX;
  --brand-accent: #XXXXXX;
  --brand-bg: #XXXXXX;
  --brand-text: #XXXXXX;
  --brand-font: '<font>', <fallback>;
}

## Restrictions
- [Any do-not-use rules from brand guidelines]
- [Colors to avoid]
```

All subsequent HTML must reference `var(--brand-*)` — never hardcode hex values inline.

---

## Relationship to DESIGN.md fast path

XDesign ships with 58 pre-extracted `DESIGN.md` files in `assets/design-md/`. **If the brand is already in the catalog** ([design-system-catalog.md](./design-system-catalog.md)), skip Steps 2-3 and load the DESIGN.md directly. The catalog covers color + typography + component specs for 58 brands.

**But:** DESIGN.md files capture visual *style* only — they do **not** include logos or product photos. If the design needs to display the brand's logo (Type 2 trigger), you still need Steps 2-3 for logo acquisition, even when using the DESIGN.md fast path.

---

## Common failure modes (and how this protocol prevents them)

| Failure | What happens | How the protocol prevents it |
|---|---|---|
| Hallucinated color | "Stripe purple is #635BFF" from memory — may be outdated | Step 3-4: extract from live CSS, verify against current site |
| CSS silhouette instead of product photo | Hardware launch animation uses a generic rounded rectangle instead of the actual product | Step 3: mandatory product photo download with three fallback paths |
| Missing logos in comparison content | "Top 5 tools" deck uses emoji or text labels instead of real logos | Type 2 trigger: "出现几个就取几个" — every named brand gets its logo |
| Outdated brand identity | Post-rebrand logo used because the model's training data predates the rebrand | Step 4: cross-reference with current official website |
| Inline hex values | Brand colors hardcoded per-element instead of via tokens | Step 5: `brand-spec.md` enforces CSS variable usage |

---

## Quick checklist (run mentally before starting any branded design)

- [ ] Is a real brand/product involved? → If yes, this protocol is active
- [ ] Did I ask the user for assets? → Step 1
- [ ] Did I search official sources? → Step 2
- [ ] Did I download (not recall) the logo/colors? → Step 3
- [ ] Did I verify the assets match the current brand? → Step 4
- [ ] Did I write `brand-spec.md` with CSS variables? → Step 5
