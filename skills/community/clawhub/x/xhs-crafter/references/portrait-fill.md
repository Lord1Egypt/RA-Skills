# Portrait Fill Rules

3:4 social images have much more vertical space than a horizontal PPT slide. A layout that works in 16:9 often becomes a thin strip in 3:4. Solve that at the planning stage.

## Vertical Zones

Think of a 1080×1440 Rednote image as five zones:

| Zone | Typical Height | Role |
|------|---------------|------|
| Header/meta | 56-90px | issue label, category, page |
| Title/lead | 240-420px | hook and claim |
| Evidence/body | 520-760px | image, ledger, diagram, comparison |
| Bottom strip | 90-180px | captions, checklist, summary |
| Footer | 52-86px | issue/page metadata |

Not every page needs all five, but every page needs an intentional vertical composition.

## Density Hard Rules

These are non-negotiable:

1. **Active composition must cover ≥78% of page height** (≈1123px of 1440px)
   - This includes: large type, images/screenshots, ledger rows, background atmosphere on hero pages, caption bands, marginalia columns
   - Whitespace is good only when it is designed. Empty leftover space is not.

2. **4-Band density check**: Divide 1440px canvas into 4 horizontal bands (360px each). Every band should have content or an intentional whitespace reason.

3. **Pure blank band >15% (216px) must have a design reason** — e.g., atmospheric hero page with WebGL/ink background.

4. **No page should have only 2 content elements** — minimum 3 (e.g., title + body + data/quote/image).

## Underfilled Page Smells

Revise if:
- A table or ledger occupies less than 45% of the canvas height
- The lower 25% of the page is empty without being an atmospheric hero page
- Four list items are rendered as short rows with large blank space below
- A screenshot is small even though it is the evidence
- Body copy is centered in the middle with no top/bottom rhythm

## Fixes For Thin Tables

When a table is too short:
1. Increase row height to 118-170px
2. Add a left marginal column with large numbers, keywords, or category labels
3. Add a pull quote column beside the table
4. Add a top or bottom issue strip with 2-3 consequences
5. Convert the table to M08 Tall Ledger
6. If there are only 2-3 points, use M04 Pull Quote or M09 Atmospheric Thesis instead of a table

## Fixes For Sparse Text

If a page has only one core sentence:
- Use M09 Atmospheric Thesis with visible ink/wash background
- Make the sentence the hero, not a small paragraph
- Add one small source/context row
- Use dark/ink page if the package needs rhythm

## Fixes For Screenshot Pages

If screenshot content matters:
- Give it 45%-65% of the page height
- Put only one key sentence above it
- Use a bottom caption band instead of a side paragraph
- Crop carefully; preserve readable UI labels

## Page Rhythm

For a 7-page Rednote set, use at least 5 distinct shapes:
- Cover / feature image
- Essay split
- Tall ledger
- Evidence screenshot
- Pull quote or atmospheric thesis
- Checklist/comparison
- Closing note

**Avoid repeating `title + lead + 3 rows` more than twice in one set.**

### Three-Layer Rhythm System

A set of cards that all look the same brightness and density is monotonous. Magazine editing uses three rhythm layers to keep readers engaged:

#### Layer 1: Light-Dark Rhythm (Editorial only)

The most powerful rhythm tool. Insert **1-2 dark pages** in a 5+ page set to create visual punctuation.

**How it works:**
- Dark pages use Midnight Ink theme (paper/ink colors inverted) while keeping the same accent color
- This is NOT switching themes — it's using Midnight Ink as a **rhythm tool within the same package**
- The accent color bridges light and dark pages, maintaining visual unity

**Where to place dark pages:**

| Position | Best for | Why |
|----------|---------|-----|
| Pull Quote page (middle) | Key quote / thesis | Dark background makes the quote feel weighty and important |
| Closing page (last) | Final takeaway | Dark ending creates a sense of conclusion, like the last page of a magazine |
| Chapter divider | Section transition | Dark page signals "new chapter" like a magazine section break |

**Rules:**
- 5-6 pages: at least 1 dark page
- 7-9 pages: at least 1-2 dark pages
- Never place 2 dark pages adjacent (they cancel each other's contrast)
- Dark pages must still pass the density rules — they are not permission to be empty
- For Swiss mode: use a full-bleed image page or a solid accent-color page instead of Midnight Ink

**Implementation:**
```html
<!-- Light page (default theme) -->
<section class="poster xhs" id="xhs-01">
  <div class="paper-wash"></div>
  <div class="grain"></div>
  ...
</section>

<!-- Dark page (Midnight Ink for rhythm) -->
<section class="poster xhs" id="xhs-04" data-theme="midnight-ink">
  <div class="paper-wash"></div>
  <div class="grain"></div>
  ...
</section>
```

#### Layer 2: Atmosphere Rhythm

Vary the strength of background atmosphere (grain, ink wash, WebGL) across pages.

| Page type | Atmosphere strength | What to show |
|-----------|-------------------|-------------|
| Cover | **Strong** | Visible grain + ink wash + possible WebGL canvas |
| Pull quote / thesis | **Strong** | Visible grain + ink wash, dark or light |
| Closing page | **Strong** | Visible grain + ink wash |
| Data / ledger / checklist | **Subtle** | Only faint grain, no ink wash |
| Screenshot evidence | **Minimal** | Almost no atmosphere, let screenshot breathe |
| Essay / body text | **Medium** | Light grain + subtle wash |

**Rules:**
- Never make all pages the same atmosphere strength
- After a strong-atmosphere page, the next page should be subtle (eye needs rest)
- Screenshot pages should have minimal atmosphere — background must not compete with the screenshot

#### Layer 3: Layout Rhythm

Already covered above (5 distinct shapes in 7 pages). Additional rules:
- **Never use the same layout recipe for 2 consecutive pages**
- Alternate between text-heavy and image/data-heavy pages
- After a dense ledger page, follow with a spacious essay or pull quote page

### Rhythm Planning Template

When creating the Content Plan (Step 2), annotate each page with its rhythm profile:

```text
01 Cover (M01) — Light / Strong atmosphere / Image-led
02 Opening (M04) — Light / Subtle atmosphere / Text+data
03 Expansion (M08) — Light / Medium atmosphere / Pipeline
04 Quote (M05) — DARK / Strong atmosphere / Pull quote ← rhythm break
05 Starship (M03) — Light / Subtle atmosphere / Essay
06 Finale (M07) — DARK / Strong atmosphere / Closing ← dark ending
```

### Anti-Patterns

- **All-light monotony**: 6 pages of identical beige paper with no dark break. Cure: insert 1 Midnight Ink pull quote page
- **Atmosphere flatline**: every page has the same grain/wash intensity. Cure: vary atmosphere strength per the table above
- **Layout repetition**: 3 pages in a row with "title + body + stat cards". Cure: swap one to a different recipe
- **Dark pages adjacent**: two Midnight Ink pages back-to-back lose contrast impact. Cure: always separate dark pages with at least one light page

## Padding Guidelines

Default padding for `.pad` container:

| Element | Current | Recommended | Reason |
|---------|---------|-------------|--------|
| Top padding | 96px | 72px | Release 24px for content |
| Bottom padding | 96px | 64px | Footer needs less space |
| Left/Right padding | 80px | 64px | More horizontal space for body text |

These values give approximately 15% more canvas area for content while maintaining magazine breathing room.
