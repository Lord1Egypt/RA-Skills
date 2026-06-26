---
name: Size Guide Builder
description: Create accurate, visual product sizing guides for apparel, footwear, and accessories that reduce size-related returns by including measurement instructions, fit notes, brand-specific conversion tables, and body-type recommendations.
---

# Size Guide Builder

Build comprehensive, accurate product sizing guides that reduce size-related returns, improve customer confidence, and increase conversion rates for apparel, footwear, and accessory ecommerce stores.

## Quick Reference

| Decision | Strong | Acceptable | Weak |
|----------|--------|------------|------|
| Measurement system | Dual units (in/cm) with toggle | Single system matching store locale | Only one system, no locale awareness |
| Size conversion | Brand-specific tables with source attribution | Generic international conversion chart | No conversion or unsourced tables |
| Fit description | Quantified fit notes ("runs 0.5 size small") | Qualitative fit guidance ("runs small") | No fit guidance at all |
| Body-type guidance | 3+ body types with specific recs | General "if between sizes, size up" | No body-type consideration |
| Measurement instructions | Step-by-step with landmark references | Text-only instructions | "Measure yourself" with no detail |
| Visual aids | Illustrated measurement diagrams described | Text with measurement point names | No visual guidance |
| Return-rate impact | Tracks return reasons and updates guide | Static guide reviewed quarterly | Published once, never updated |
| Mobile presentation | Responsive tables, swipeable comparisons | Readable on mobile | Desktop-only layout |

## Solves

1. **High return rates from size mismatches** — Customers order wrong sizes because product pages lack detailed measurement data, costing 20-30% in avoidable returns.
2. **Inconsistent sizing across brands** — Multi-brand stores confuse customers when a Medium from Brand A fits like a Large from Brand B.
3. **Missing international conversions** — Global customers cannot translate US/UK/EU sizes, leading to abandoned carts.
4. **No fit context for different body types** — Generic size charts ignore that the same measurements fit differently on different body shapes.
5. **Poor measurement instructions** — Customers measure incorrectly (e.g., measuring over clothes, using wrong landmarks), producing inaccurate size selections.
6. **Incomplete category coverage** — Stores have guides for tops but not bottoms, shoes, or accessories like rings and hats.
7. **Static guides that drift from inventory** — Size guides are published once and never updated when new brands or product lines are added.

## Workflow

### Step 1: Gather Product and Category Context

Collect the following from the user:

- **Product category**: Apparel (tops, bottoms, dresses, outerwear), footwear, accessories (hats, belts, rings, gloves)
- **Brand(s)**: Single brand or multi-brand store
- **Target market**: Primary regions for international conversion (US, UK, EU, JP, KR, AU)
- **Known fit issues**: Any existing customer feedback about sizing ("runs small," "narrow fit")
- **Existing size data**: Current size charts, manufacturer specs, or fit sample measurements
- **Store platform**: Shopify, WooCommerce, custom — affects output format

If the user provides a product URL or product data, extract sizing information from it directly.

### Step 2: Define Measurement Points

For each product category, identify the critical measurement points:

**Tops & Outerwear:**
- Chest/Bust (measured at fullest point, arms relaxed at sides)
- Waist (natural waistline, narrowest point of torso)
- Hip (fullest point, approximately 7-9 inches below waist)
- Shoulder width (seam to seam across back)
- Sleeve length (shoulder seam to wrist bone)
- Body/torso length (highest point of shoulder to hem)

**Bottoms:**
- Waist (where the garment sits — may differ from natural waist)
- Hip (fullest point)
- Inseam (crotch seam to hem)
- Outseam (waistband to hem)
- Thigh (measured at widest point, 1 inch below crotch)
- Rise (front rise: waistband center to crotch seam)

**Footwear:**
- Foot length (heel to longest toe, in mm)
- Foot width (ball of foot, widest point)
- Width designation (Narrow/N, Medium/M, Wide/W, Extra Wide/XW)

**Accessories:**
- Hats: Head circumference (measured 1 inch above ears)
- Belts: Waist measurement + 2-inch add rule
- Rings: Inner circumference or diameter (mm)
- Gloves: Hand circumference at knuckles (exclude thumb)

### Step 3: Build the Size Table

Construct the size table with these requirements:

1. **Row structure**: One row per size (XS, S, M, L, XL, XXL — or numeric sizes)
2. **Column structure**: Size label | each measurement point | fit notes
3. **Dual units**: Show both inches and centimeters — format as "38 in / 96.5 cm"
4. **Range tolerance**: Use ranges for stretch or relaxed-fit items ("36-38 in")
5. **Brand-specific**: If multi-brand, create separate tables per brand with a comparison note
6. **Garment vs. body**: Clearly label whether measurements are "garment flat lay" or "body measurement" — this is the #1 source of confusion

### Step 4: Add Fit Context and Recommendations

Layer qualitative guidance on top of the raw numbers:

- **Fit type label**: Slim Fit / Regular Fit / Relaxed Fit / Oversized — with a one-line definition
- **"Between sizes" rule**: Specific advice (e.g., "If between sizes, size up for layering; stay true for a fitted look")
- **Body-type guidance**: At minimum address 3 common scenarios:
  - Athletic/muscular build → may need to size up in chest/thigh
  - Petite frame → check garment length, may need shorter inseam
  - Plus size → check that hip measurement is covered, not just waist
- **Fabric/stretch note**: "This item has 5% elastane — measurements reflect un-stretched garment. Fabric stretches approximately 1-2 inches."
- **Model reference** (if available): "Model is 5'10", 155 lbs, wearing size M"

### Step 5: Create Measurement Instructions

Write clear, step-by-step self-measurement instructions:

1. Use a flexible measuring tape (not a ruler or metal tape)
2. Measure over light undergarments, not over bulky clothing
3. Stand naturally — do not suck in or puff out
4. Have someone help for back measurements (shoulder width, back length)
5. Measure each point 2 times and use the larger number
6. For each measurement point, specify the anatomical landmark precisely

### Step 6: Format International Conversions

Create a conversion section covering:

- US, UK, EU standard size equivalents
- JP and KR sizes (if target market includes Asia)
- AU/NZ sizes (offset from UK by specific rules per category)
- Note any brand-specific deviations from standard conversions
- Clearly mark "approximate" — no international standard is perfectly uniform

### Step 7: Compile and Quality-Check the Guide

Assemble all sections and verify:

- Every size in the product catalog is represented
- Measurements are internally consistent (e.g., M is between S and L in all dimensions)
- Dual units are mathematically correct (1 inch = 2.54 cm)
- Fit notes match known customer feedback
- Conversion tables are sourced and attributed
- Guide is complete enough that a customer can self-select the right size without contacting support

## Example 1: Women's Casual T-Shirt

**User input:** "I need a size guide for our women's relaxed-fit cotton t-shirts. We sell in US, UK, and EU. Customers say they run slightly large. The fabric is 100% cotton, pre-shrunk, no stretch."

**Output:**

### Women's Relaxed Fit Tee — Size Guide

**Fit:** Relaxed — designed to drape loosely with 2-3 inches of ease through the body. If you prefer a more fitted look, consider sizing down one size.

**Fabric note:** 100% pre-shrunk cotton. No stretch. Measurements reflect garment laid flat, doubled for circumference.

| Size | US | UK | EU | Chest | Waist | Body Length | Shoulder |
|------|----|----|-----|-------|-------|-------------|----------|
| XS | 0-2 | 4-6 | 32-34 | 34-35 in / 86-89 cm | 26-27 in / 66-69 cm | 24.5 in / 62 cm | 14 in / 35.5 cm |
| S | 4-6 | 8-10 | 36-38 | 36-37 in / 91-94 cm | 28-29 in / 71-74 cm | 25 in / 63.5 cm | 14.5 in / 37 cm |
| M | 8-10 | 12-14 | 40-42 | 38-39 in / 96.5-99 cm | 30-31 in / 76-79 cm | 25.5 in / 65 cm | 15 in / 38 cm |
| L | 12-14 | 16-18 | 44-46 | 40-42 in / 101.5-107 cm | 32-34 in / 81-86 cm | 26 in / 66 cm | 15.5 in / 39.5 cm |
| XL | 16-18 | 20-22 | 48-50 | 43-45 in / 109-114 cm | 35-37 in / 89-94 cm | 26.5 in / 67 cm | 16 in / 40.5 cm |
| XXL | 20-22 | 24-26 | 52-54 | 46-48 in / 117-122 cm | 38-40 in / 96.5-101.5 cm | 27 in / 68.5 cm | 16.5 in / 42 cm |

**Fit note:** This style runs slightly large. If you are between sizes or prefer a less oversized look, we recommend sizing down.

**Body-type tips:**
- *Athletic/broad shoulders:* Match your shoulder measurement first; the relaxed body will accommodate a larger chest.
- *Petite (under 5'4"):* Consider XS or S regardless of normal size — check body length to ensure the hem hits at the right point.
- *Fuller bust:* Size to your chest measurement; the relaxed waist will not be restrictive.

**How to measure:**
1. **Chest:** Wrap the tape around the fullest part of your bust, keeping the tape level and snug but not tight. Arms at your sides.
2. **Waist:** Measure at your natural waistline — the narrowest point of your torso, usually just above your belly button.
3. **Shoulder:** Have someone measure across your back from the tip of one shoulder bone to the other.

## Example 2: Men's Running Shoes

**User input:** "We need a size guide for our men's running shoes. We sell globally. The shoes are true to size with a medium-width last. Available in sizes US 7-14, including half sizes."

**Output:**

### Men's Performance Running Shoe — Size Guide

**Fit:** True to size on a medium-width (D) last. If you have wide feet, consider our Wide (2E) option or sizing up 0.5 size.

**Measuring your foot:**
1. Stand on a piece of paper against a wall, heel touching the wall
2. Mark the tip of your longest toe (this may not be your big toe)
3. Measure from the wall to the mark in millimeters
4. Measure both feet — use the larger measurement
5. Measure at the end of the day when feet are slightly swollen

| US | UK | EU | JP (cm) | KR (mm) | Foot Length (mm) |
|----|----|----|---------|---------|-----------------|
| 7 | 6 | 40 | 25.0 | 250 | 248-252 |
| 7.5 | 6.5 | 40.5 | 25.5 | 255 | 253-257 |
| 8 | 7 | 41 | 26.0 | 260 | 258-262 |
| 8.5 | 7.5 | 42 | 26.5 | 265 | 263-267 |
| 9 | 8 | 42.5 | 27.0 | 270 | 268-272 |
| 9.5 | 8.5 | 43 | 27.5 | 275 | 273-277 |
| 10 | 9 | 44 | 28.0 | 280 | 278-282 |
| 10.5 | 9.5 | 44.5 | 28.5 | 285 | 283-287 |
| 11 | 10 | 45 | 29.0 | 290 | 288-292 |
| 11.5 | 10.5 | 45.5 | 29.5 | 295 | 293-297 |
| 12 | 11 | 46 | 30.0 | 300 | 298-302 |
| 13 | 12 | 47.5 | 31.0 | 310 | 308-312 |
| 14 | 13 | 48.5 | 32.0 | 320 | 318-322 |

**Width guide:**

| Width | Description | Ball of Foot |
|-------|-------------|-------------|
| B (Narrow) | For narrow feet | < 95 mm |
| D (Medium) | Standard width — this shoe | 95-105 mm |
| 2E (Wide) | For wide feet | 106-115 mm |
| 4E (Extra Wide) | For extra-wide feet | > 115 mm |

**Tips:**
- Running shoes should have a thumb's width (~10-12 mm) of space between your longest toe and the front of the shoe.
- If you wear thick running socks, measure your foot while wearing them.
- Orthotics users: remove the insole, place your orthotic inside, and check that your foot does not hang over the edges.

## Common Mistakes

1. **Confusing garment measurements with body measurements.** Always label which you are providing. A "38-inch chest" garment is designed for a body with a 36-inch chest (2 inches of ease). Mixing these up causes universal mis-sizing.

2. **Using only one measurement system.** International customers leave if they see only inches. Always provide dual units and verify the math (1 in = 2.54 cm, not 2.5).

3. **Providing a single generic chart for multiple brands.** A size M from one manufacturer is not the same as another. Multi-brand stores must provide brand-specific tables or at minimum note deviations.

4. **Ignoring the "between sizes" scenario.** Most customers fall between sizes. Without explicit guidance, they either buy two sizes (increasing returns) or abandon the cart.

5. **Skipping measurement instructions.** Customers who measure incorrectly will choose the wrong size even with a perfect chart. Always include how-to-measure steps.

6. **Forgetting to specify fit type.** "Regular fit" and "slim fit" produce completely different size recommendations from the same body measurements. Always state the intended fit.

7. **Not updating guides when products change.** Manufacturers adjust patterns and fabrics between seasons. A size guide from last year may be wrong for this year's inventory.

8. **Ignoring accessories.** Ring sizes, hat sizes, and belt sizes have their own measurement systems that are frequently omitted from stores that sell these alongside apparel.

9. **No mobile optimization.** Large tables are unreadable on phones. Recommend responsive table format or measurement-lookup tools.

10. **Omitting stretch/fabric composition.** A garment with 5% elastane fits dramatically differently from one with 0%. Always note fabric composition and its impact on fit.

## Resources

- [Output Template](references/output-template.md) — Structured template for delivering size guides
- [Sizing Standards Guide](references/sizing-standards-guide.md) — International sizing standards and conversion references
- [Measurement Best Practices](references/measurement-best-practices.md) — Detailed measurement techniques and accuracy tips
- [Quality Checklist](assets/quality-checklist.md) — Pre-delivery verification checklist
