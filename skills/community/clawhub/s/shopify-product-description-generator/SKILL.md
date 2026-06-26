---
name: shopify-product-description-generator
description: Build Shopify-ready product descriptions that turn raw product facts into clearer PDP copy with stronger benefits, objections handling, and conversion intent.
---

# Shopify Product Description Generator

Turn raw product facts into Shopify-ready PDP copy that is clearer, more persuasive, and easier to publish.

This skill goes beyond generic AI copywriting. It applies a structured conversion-copywriting workflow — buyer motive analysis, feature-to-benefit translation, objection handling, proof integration, and Shopify-native HTML formatting — to produce descriptions that sell, not just describe.

---

## Quick Reference

| Decision | Key Signal | Strong | Acceptable | Weak |
|---|---|---|---|---|
| Benefit clarity | Benefits vs features ratio | ≥ 3 benefits per feature block | 1–2 benefits per block | Features only, no benefits |
| Objection handling | Objections addressed | Top 3 objections surfaced | 1–2 addressed | None addressed |
| Proof integration | Trust signals included | Reviews + certifications + specifics | 1–2 proof points | No proof, vague claims |
| Scannability | Structure & formatting | H2s + bullets + bold benefits | Some structure | Wall of text |
| CTA strength | Action clarity | Specific, benefit-driven CTA | Generic "Buy now" | No CTA |
| SEO alignment | Keyword integration | Primary + 2–3 secondary natural | Primary keyword only | No keyword strategy |

---

## Solves

Most Shopify product descriptions fail not because sellers lack product knowledge, but because:

- **Feature dumping** — listing specs without explaining why they matter to the buyer
- **Missing objections** — ignoring the reasons people hesitate (price, durability, sizing, etc.)
- **No proof** — making claims without reviews, certifications, numbers, or specifics
- **Wall-of-text formatting** — long paragraphs that don't scan on mobile
- **Generic AI copy** — bland, interchangeable descriptions that could describe any product
- **Weak CTAs** — no clear next step or urgency after the description
- **SEO afterthought** — keywords stuffed in awkwardly or missing entirely

Goal: **Produce a description that a Shopify merchant can paste directly into their product page — with benefits, objections, proof, and formatting already handled.**

---

## Use when

- You need a new Shopify product description from messy notes, specs, or bullets
- A PDP has traffic but weak conversion because the copy is feature-heavy and benefit-light
- You want multiple product-description angles for A/B testing
- A team needs faster first drafts without publishing generic AI copy
- Rewriting supplier-provided descriptions into brand-voice copy
- Launching a new product and need conversion-focused copy from day one
- Optimizing existing descriptions that rank but don't convert

## Do not use when

- You need a full landing page, email sequence, or ad campaign
- The main task is regulated claim review or legal compliance
- Product facts, proof, or audience are still unknown
- You only want proofreading with no structural rewrite
- The product is in a heavily regulated category requiring legal review (supplements, medical devices)

---

## Inputs

Gather these inputs — mark any gaps explicitly:

**Product basics:**
- Product name
- Product type / category
- Price point and positioning (budget / mid / premium)
- Key specs and features (materials, dimensions, weight, etc.)
- What makes this product different from competitors

**Audience & context:**
- Target customer (demographics, psychographics, pain points)
- Primary use case / scenario
- Where the customer is in their buying journey
- What they're comparing against (competitors, alternatives, doing nothing)

**Proof & trust:**
- Customer reviews, testimonials, or ratings
- Certifications, awards, or third-party validation
- Specific numbers (units sold, satisfaction %, years in market)
- Media mentions or expert endorsements

**Brand & voice:**
- Brand voice guidelines (casual / professional / luxe / technical)
- Tone keywords (e.g., "confident but not pushy", "warm and approachable")
- Words or phrases to use or avoid
- Existing product descriptions for voice matching

**SEO inputs:**
- Primary keyword (the main search term to rank for)
- Secondary keywords (2–3 related terms)
- Competitor URLs for reference (optional)

See `references/buyer-psychology-guide.md` for conversion psychology frameworks.

---

## Workflow

### 1. Identify buyer motive and purchase context

Before writing a single word, understand WHY someone buys this product:

```
Primary motive: [Functional / Emotional / Social / Identity]
Purchase trigger: What event or need starts the search?
Decision factors: What 3 things determine the final choice?
Hesitations: What makes them almost leave without buying?
```

This drives every word choice. A $15 phone case buyer has different motivations than a $200 skincare buyer.

See `references/buyer-psychology-guide.md` for motive analysis frameworks.

### 2. Convert features to benefits

Every feature must answer: **"So what? Why should the buyer care?"**

| Feature (What it is) | Benefit (Why it matters) | Proof (How we know) |
|---|---|---|
| [Spec or attribute] | [Outcome for the buyer] | [Evidence or specificity] |

```
Feature: Made from 18/10 stainless steel
→ Benefit: Won't rust, stain, or pick up flavors — even after years of daily use
→ Proof: Same grade used in professional restaurant kitchens

Feature: 2,400mAh battery
→ Benefit: Lasts a full 8-hour workday on a single charge
→ Proof: Tested across 500+ charge cycles with < 5% capacity loss
```

**Rule: Never include a feature without its benefit. If you can't articulate the benefit, the feature doesn't belong in the description.**

### 3. Surface and handle objections

Every product has objections. The best descriptions address them before the buyer has to ask:

| Objection | Evidence / Counter | Where to Place |
|---|---|---|
| "Is it worth the price?" | [Value comparison, cost-per-use, longevity] | Near price / CTA |
| "Will it work for me?" | [Use cases, sizing guide, compatibility] | Benefit blocks |
| "Can I trust this brand?" | [Reviews, certifications, guarantee] | Proof section |
| "What if I don't like it?" | [Return policy, guarantee, trial] | Near CTA |

See `references/objection-handling-templates.md` for common objection patterns by product category.

### 4. Write the description structure

Follow this proven PDP structure:

```
1. HEADLINE (H1)
   - Benefit-driven, not feature-driven
   - Include primary keyword naturally
   - 6–12 words

2. OPENING HOOK (1–2 sentences)
   - Lead with the buyer's problem or desire
   - Create recognition: "Yes, that's me"

3. BENEFIT BLOCKS (3–5 blocks)
   - Each block: Bold benefit headline → 1–2 supporting sentences
   - Feature → Benefit → Proof pattern
   - Most important benefit first

4. SOCIAL PROOF / TRUST
   - Pull quote from review
   - Certification badges or stats
   - "Join X+ customers" or similar

5. USAGE / SCENARIO SECTION
   - Paint a picture of the product in use
   - Help buyer visualize ownership
   - Address "Will this work for MY situation?"

6. SPECS / DETAILS (collapsible or below fold)
   - Clean, scannable format
   - Only specs that matter to the buyer

7. CTA
   - Specific, benefit-driven
   - Address final objection (guarantee, free shipping, etc.)
   - Create gentle urgency if appropriate
```

### 5. Apply Shopify-native formatting

Format for Shopify's rich text editor:

- Use `<h2>` for section headers (not H1 — that's the product title)
- Use `<strong>` for benefit headlines within blocks
- Use `<ul>` / `<li>` for scannable benefit lists
- Keep paragraphs to 2–3 sentences max (mobile readability)
- Use `<em>` sparingly for emphasis
- Include line breaks between sections for visual breathing room

See `references/output-template.md` for the complete HTML template.

### 6. SEO integration

Weave keywords naturally — never stuff:

- Primary keyword in first 100 words
- Primary keyword in at least one H2
- Secondary keywords distributed across benefit blocks
- Product name used naturally 2–3 times
- Alt-text suggestions for product images (if applicable)

```
Bad: "Our stainless steel water bottle is the best stainless steel water bottle for stainless steel water bottle lovers"
Good: "Built from 18/10 stainless steel, this bottle keeps drinks cold for 24 hours — no metallic taste, no condensation on the outside"
```

### 7. Quality-check the description

Before delivering, verify with `assets/pdp-checklist.md`:

- Does every feature have a corresponding benefit?
- Are the top 3 objections addressed?
- Is there at least one proof point (review, stat, certification)?
- Does it scan well on mobile (short paragraphs, bullets, bold)?
- Is the CTA specific and benefit-driven?
- Are keywords integrated naturally?
- Does it match the brand voice?

---

## Output

Return a structured package (see `references/output-template.md`):

1. **Buyer analysis**
   - Motive, trigger, decision factors, hesitations

2. **Feature-benefit-proof map**
   - Every feature translated with benefit and evidence

3. **Objection handling plan**
   - Top objections with counters and placement

4. **Product description (Shopify-ready HTML)**
   - Full description formatted for paste-into-Shopify
   - Mobile-optimized structure

5. **SEO notes**
   - Keywords used and placement
   - Meta description suggestion (155 chars)

6. **Review notes**
   - Any assumptions made
   - Suggested A/B test angles
   - Manual review flags (claims that need verification)

---

## Quality bar

Strong output should:
- Lead with benefits, not features — in every section
- Address at least 3 buyer objections directly in the copy
- Include specific proof (numbers, reviews, certifications) — not vague claims
- Format for mobile-first scanning (short paragraphs, bullets, bold benefits)
- Sound like the brand, not like generic AI copy
- Be ready to paste into Shopify with no additional formatting needed

## What "better" looks like

Better output does not stop at "here's a product description."
It helps answer:
- Why would someone choose THIS product over the alternative?
- What would make someone hesitate, and how does the copy address it?
- What proof makes the claims believable?
- Does this description work on a phone screen?
- Can the merchant paste this directly into Shopify?
- What should they A/B test first?

---

## Examples

### Example 1: Premium insulated water bottle

**Inputs:**
- Product: ThermoFlask Pro 32oz Insulated Water Bottle
- Price: $34.99 (mid-premium)
- Features: 18/10 stainless steel, double-wall vacuum, 24hr cold / 12hr hot, BPA-free, powder-coated, leak-proof lid
- Audience: Health-conscious professionals, 25–45, gym + office use
- Voice: Confident, clean, active
- Primary keyword: "insulated water bottle"

**Output excerpt (Shopify HTML):**
```html
<h2>Stay Hydrated From Gym to Office — Without Refilling</h2>
<p>You shouldn't have to choose between a water bottle that keeps up at the gym and one that looks good on your desk. The ThermoFlask Pro does both.</p>

<p><strong>Ice-cold for 24 hours. Hot for 12.</strong> Double-wall vacuum insulation means your morning coffee stays hot through your commute, and your afternoon water stays cold through your workout. No lukewarm disappointment at 2pm.</p>

<p><strong>Built to last, not to replace.</strong> 18/10 stainless steel — the same grade used in professional kitchens — won't rust, dent, or pick up yesterday's coffee flavor. The powder-coated exterior grips without slipping, even with wet hands.</p>

<p><strong>Toss it in your bag without thinking twice.</strong> The leak-proof lid locks with a quarter turn. We've tested it upside-down in gym bags, backpacks, and laptop sleeves. Zero leaks.</p>
```

### Example 2: Handmade soy candle

**Inputs:**
- Product: Coastal Calm — Hand-Poured Soy Candle, 8oz
- Price: $22 (premium small-batch)
- Features: 100% soy wax, cotton wick, 45hr burn, phthalate-free, hand-poured in small batches
- Audience: Women 28–45, self-care focused, eco-conscious
- Voice: Warm, sensory, intimate
- Primary keyword: "soy candle"

**Output excerpt:**
```html
<h2>Your Evenings Deserve More Than Overhead Lighting</h2>
<p>Coastal Calm fills your space with sea salt, driftwood, and a hint of white tea — like opening a window to the coast, even on a Tuesday night.</p>

<p><strong>45 hours of slow, even burn.</strong> Hand-poured soy wax melts cleaner than paraffin — no black soot on your walls, no headache-inducing chemicals. Just the scent, nothing else.</p>

<p><strong>Small-batch. Actually small-batch.</strong> Every candle is poured by hand in batches of 30 or fewer. That's not marketing — it's how we control the scent throw and burn consistency that mass-produced candles can't match.</p>
```

---

## Common mistakes

1. **Leading with features** — "Made from 18/10 stainless steel" vs "Won't rust, stain, or absorb flavors — even after years of daily use"
2. **Ignoring objections** — Never mentioning price justification, sizing uncertainty, or trust
3. **No proof** — "Best quality" with zero reviews, stats, or specifics to back it up
4. **Writing for desktop** — Long paragraphs that become walls of text on mobile
5. **Generic voice** — Copy that could describe any product in the category
6. **Weak CTA** — "Add to cart" instead of "Start your morning routine upgrade — ships free today"
7. **SEO stuffing** — Keywords crammed in unnaturally instead of woven into benefit statements
8. **Skipping the opening hook** — Jumping into features without establishing relevance to the buyer

---

## Resources

- `references/output-template.md` — Shopify-ready HTML template with structure
- `references/buyer-psychology-guide.md` — Buyer motive analysis and conversion psychology
- `references/objection-handling-templates.md` — Common objection patterns by product category
- `assets/pdp-checklist.md` — Pre-delivery quality checklist
