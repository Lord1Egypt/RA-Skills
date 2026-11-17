# Section recipe library

Reusable, brand-token-driven build sequences for the sections a studio site needs
again and again. **Before building a section, find its recipe here, follow the
structure, and bind everything to the brand tokens by name** (see
[`brand-kit.md`](brand-kit.md)). Build **classic-first**; apply the recipe's **Pro**
or **Atomic/V4** variant note only when those engines are active.

Recipes reuse — they do not restate — the rest of the skill's rules:

- Native widgets, **never** an HTML-dump of a whole section.
- `duplicate-element` for a **fixed** set of cards; **Loop Grid** (Pro) when the cards
  are driven by posts/CPT/products.
- Flat-param widget convention; set `typography_typography: "custom"` before sizing.
- Tokens by name (bind the widget's color to the global, or use the recorded token
  value) — no ad-hoc hex.

Every section follows the same shell: an **outer container** (full-width, a token
background, vertical padding ~80–120px) wrapping an **inner container** (boxed,
max-width ~1200–1360px, centered) that holds the content. Recipes only describe what
differs inside.

Type-scale steps referenced below: `h1 48 / h2 36 / h3 28 / h4 22 / body-lg 18 /
body 16 / small 14` (px desktop; scale down ~15–20% on mobile).

---

## Hero

**When:** the first screen of a landing/home page.

**Structure:**
- outer container — bg `bg`, padding ~120px top / ~96px bottom
  - inner boxed container — max-w ~1100, centered, `align-items: center`, text-align center, gap 20
    - eyebrow — Heading, `small`, color `accent`, uppercase, letter-spacing
    - title — Heading h1, color `heading`
    - lead — Text, `body-lg`, color `text`, max-w ~640
    - button row — container, `flex-direction: row`, gap 12, justify center
      - primary Button — bg `brand`, text on-brand (white/`bg`)
      - secondary Button — transparent bg, `border` outline, text `brand`

**Tokens & scale:** bg `bg`; eyebrow `accent`/small; title `heading`/h1; lead
`text`/body-lg; primary `brand`.

**Key settings:** container `min-height` optional (e.g. 70vh); gap 20; button padding ~16×28.

**Responsive:** title → ~32–36px; button row stacks (column, full-width buttons).

**Variants:** *Pro* — add a Sticky transparent→solid header above. *Atomic/V4* —
outer/inner → `e-flexbox`; title → `add-atomic-heading` (font_size 48, color `heading`),
buttons → `add-atomic-button` (background `brand`).

---

## Services grid

**When:** 3–6 services/features as cards.

**Structure:**
- outer container — bg `surface`, padding ~100px
  - inner boxed — gap 48
    - heading block — Heading h2 (`heading`) + Text body (`muted`), centered
    - cards row — container `flex-direction: row`, wrap, gap 24, 3 per row
      - card container ×N — bg `bg`, border 1px `border`, radius 12, padding 28, gap 12
        - icon — Icon, color `brand`
        - title — Heading h3 (`heading`)
        - body — Text body (`text`)

**Tokens & scale:** section `surface`; cards `bg`+`border`; icon/accents `brand`;
titles `heading`/h3; body `text`.

**Key settings:** card `flex-basis` ~32% (3-col) → 100% mobile; equal heights via
`align-items: stretch`.

**Responsive:** cards → 1 per row (column).

**Variants:** *Pro + dynamic* (cards from a CPT/posts) — build one card as a Loop
template, then `add-loop-grid` pointing at it instead of duplicating. *Atomic/V4* —
containers → `e-flexbox`; per-card styling via the atomic style props.

---

## Split (image + text)

**When:** an alternating image-beside-text block (about, feature deep-dive).

**Structure:**
- outer container — bg `bg`, padding ~100px
  - inner boxed — container `flex-direction: row`, gap 56, `align-items: center`
    - media half — Image (or container), flex-basis 50%
    - text half — container, gap 16, flex-basis 50%
      - title — Heading h2 (`heading`)
      - body — Text body (`text`)
      - button — Button, bg `brand` (optional)

**Tokens & scale:** bg `bg` (alternate `surface` on every other split); title
`heading`/h2; body `text`.

**Key settings:** swap child order for the next split (image left → image right) by
reversing the row or moving the media child.

**Responsive:** row → column; media first, max-width 100%.

**Variants:** *Atomic/V4* — row container → `e-flexbox` (`flex-direction: row`),
halves → nested `e-flexbox`.

---

## Stats band

**When:** 3–4 headline metrics.

**Structure:**
- outer container — bg `brand` (inverted band), padding ~72px
  - inner boxed — container `flex-direction: row`, justify space-between, gap 32
    - stat ×N — container, text-align center, gap 4
      - number — Heading h1/h2, color on-brand (`bg`/white)
      - label — Text `small`, color on-brand at ~80% opacity

**Tokens & scale:** band bg `brand`; text inverted (use `bg`/white on `brand`, NOT
`text` which would be low-contrast); numbers h1/h2; labels small.

**Key settings:** even distribution; thin divider (`border` at low opacity) between
stats optional.

**Responsive:** row → 2×2 grid (wrap) on mobile.

**Variants:** *Atomic/V4* — band → `e-flexbox` with `background` = `brand`; numbers →
`add-atomic-heading` color `bg`.

---

## Testimonials

**When:** client quotes / social proof.

**Structure:**
- outer container — bg `surface`, padding ~100px
  - inner boxed — gap 40
    - heading block — Heading h2 (`heading`), centered
    - quote card(s) — container, bg `bg`, border 1px `border`, radius 12, padding 32, gap 16
      - quote — Text `body-lg`, color `text`
      - name — Text body, color `heading`, weight 600
      - role — Text `small`, color `muted`

**Tokens & scale:** section `surface`; card `bg`+`border`; quote `text`/body-lg; role
`muted`/small.

**Key settings:** single centered card (max-w ~760), or 2–3 cards in a row.

**Responsive:** multi-card row → column.

**Variants:** *Pro* — multiple quotes → a carousel (Loop Carousel / testimonial
widget) instead of duplicated cards.

---

## CTA band

**When:** a focused conversion prompt between/below content.

**Structure:**
- outer container — bg `brand`, padding ~72px (compact band)
  - inner boxed — max-w ~720, centered, text-align center, gap 16
    - title — Heading h2, color on-brand (`bg`/white)
    - body — Text body, color on-brand ~85%
    - button — Button, bg `bg`/white, text `brand` (contrast against the band)

**Tokens & scale:** band `brand`; text inverted; button inverted (`bg` bg / `brand`
text); title h2.

**Key settings:** keep it short — one heading, one line, one button.

**Responsive:** title → ~28px; button full-width.

**Variants:** *Atomic/V4* — band → `e-flexbox` (`background` `brand`), button →
`add-atomic-button` (background `bg`, color `brand`).

---

## Contact

**When:** a contact section with details + a form.

**Structure:**
- outer container — bg `bg`, padding ~100px
  - inner boxed — container `flex-direction: row`, gap 56
    - left — container, gap 16: Heading h2 (`heading`) · Text body (`text`) · detail
      lines (email/phone) `body`, links `brand`
    - right — the form

**Tokens & scale:** bg `bg`; heading `heading`/h2; body/details `text`; links `brand`;
field borders `border`.

**Key settings:** form fields name/email/message + submit; submit button bg `brand`.

**Responsive:** row → column (text above form).

**Variants:** *Pro* — right side = native **Form** widget (see the Forms section).
*Free* — **Fluent Forms** shortcode/widget (see Forms fallback). Bind submit-button
color to `brand` either way. *Atomic/V4* — the native Pro **Form** widget isn't
V4-ready (it's a classic island that may not render on an atomic page — see
[`atomic-v4.md`](atomic-v4.md)), so even on a Pro site drop a **Fluent Forms
shortcode** via `add-atomic-widget` (a shortcode/HTML atomic type) and wrap the two
halves in `e-flexbox`. Flag to the user that the Pro Form widget is skipped because it
isn't V4-ready.

---

## FAQ

**When:** common questions in an accordion.

**Structure:**
- outer container — bg `bg`, padding ~100px
  - inner boxed — max-w ~820 (narrow), gap 32
    - heading — Heading h2 (`heading`), centered
    - accordion — Toggle/Accordion widget
      - item ×N — question (h4, `heading`) / answer (body, `text`), divider `border`

**Tokens & scale:** bg `bg`; question `heading`/h4; answer `text`/body; separators
`border`.

**Key settings:** first item open optional; icon color `brand`.

**Responsive:** unchanged (already narrow/stacked).

**Variants:** *Free* — Elementor's base Accordion/Toggle is available without Pro.
*Atomic/V4* — there is no atomic accordion, and a classic Accordion/Toggle dropped on
a V4 page **won't persist** (classic writes don't survive on an atomic page — see
[`atomic-v4.md`](atomic-v4.md)). Build the accordion the atomic way: one `add-div-block`
per item wrapping a native `<details>`/`<summary>` (question in `<summary>`, answer in
the body) via an atomic HTML/shortcode widget. This div-block + `<details>` pattern is
the **only** V4 path here — do not leave a classic accordion on a V4 page.

---

## Pricing

**When:** 3 plan/tier cards.

**Structure:**
- outer container — bg `surface`, padding ~100px
  - inner boxed — gap 40
    - heading block — Heading h2 (`heading`), centered
    - plans row — container `flex-direction: row`, gap 24, 3 per row, `align-items: stretch`
      - plan card ×3 — bg `bg`, border 1px `border`, radius 12, padding 32, gap 16
        - name — Heading h3 (`heading`)
        - price — Heading h2 (`brand`)
        - features — Text body (`text`), one per line
        - button — Button, bg `brand`
      - **featured card** — accent the middle one: border `brand`, subtle raise/scale,
        a `accent` ribbon

**Tokens & scale:** section `surface`; cards `bg`+`border`; price/featured `brand`;
names `heading`/h3; features `text`.

**Key settings:** equal heights (`align-items: stretch`); featured card visually lifted.

**Responsive:** 3-col → 1-col; featured loses scale, keeps border.

**Variants:** *Atomic/V4* — cards → `e-flexbox`; featured border/emphasis via atomic
style props.

---

## Logos strip

**When:** a row of client/partner logos for trust.

**Structure:**
- outer container — bg `bg`, padding ~56px (slim)
  - inner boxed — gap 24, centered
    - caption — Text `small`, color `muted`, centered (optional, e.g. "Trusted by")
    - logos row — container `flex-direction: row`, justify space-between/center, wrap, gap 40
      - Image ×N — logos, grayscale/`muted` tint, uniform height ~32–40px

**Tokens & scale:** bg `bg`; caption `muted`/small.

**Key settings:** uniform logo height; grayscale by default, color on hover optional.

**Responsive:** wrap to 2–3 per row; reduce gaps.

**Variants:** *Pro* — many logos → a Loop Carousel for an auto-scrolling marquee.
*Atomic/V4* — row → `e-flexbox` (wrap), logos → `add-atomic-image`.
