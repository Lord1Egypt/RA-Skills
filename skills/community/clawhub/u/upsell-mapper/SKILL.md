---
name: Upsell Mapper
description: Map product relationships and purchase sequence patterns to identify the best cross-sell triggers at checkout, post-purchase, and in creator content.
---

# Upsell Mapper

Map product relationships and purchase sequence patterns to identify the best cross-sell triggers at checkout, post-purchase, and in creator content. This skill turns a flat product catalog into a structured upsell and cross-sell matrix that increases average order value and customer lifetime value without increasing acquisition cost.

## Quick Reference

| Decision | Strong | Acceptable | Weak |
|----------|--------|------------|------|
| Cross-sell price ratio | 15–35% of original item price | 35–60% | >60% or <10% |
| Upsell timing | At cart / checkout (highest intent) | Post-purchase email (day 1) | Days later without trigger |
| Product relevance | Directly complements primary purchase | Same category | Unrelated |
| Recommendation type | "Frequently bought together" (data-driven) | "You might also like" (curated) | Generic "related products" |
| Bundle discount | 10–20% savings vs. individual prices | 5–10% | No discount or >30% |
| Cross-sell placement | Cart drawer + checkout page | Product page only | Homepage only |
| Creator content angle | "What I use with my [Product]" (natural) | Dedicated "bundle" content | Direct sales pitch only |

## Solves

1. **Low AOV (average order value)** — Customers buying one item and leaving; no prompts to add complementary products
2. **High acquisition cost with single-purchase customers** — Every sale must be profitable on first purchase; cross-sells fund the acquisition cost
3. **Underutilized post-purchase window** — The moment after checkout is highest-intent for a second purchase; most brands send only an order confirmation
4. **Creator content not converting to full basket** — Creators promote one SKU; viewers don't know the brand has related products
5. **Bundle assembly guesswork** — Brands create bundles based on intuition, not purchase sequence data; this skill surfaces data-backed natural pairings
6. **Repeat purchase rate below category benchmark** — No structured re-order nudge at the right moment (product depletion cycle)
7. **Subscription opportunity missed** — Consumable products with no subscription offer leave recurring revenue on the table

## Workflow

### Step 1 — Gather Inputs
Collect:
- Full product catalog with prices, categories, and descriptions
- Order history export (if available) — minimum 3 months, ideally 12 months
- Platform: Shopify, WooCommerce, TikTok Shop, Amazon, or brand site
- Current AOV and repeat purchase rate (benchmark context)
- Any existing bundles or cross-sell setups (to audit and improve)

### Step 2 — Build the Product Relationship Matrix

For each product, identify:
| Relationship type | Definition | Example |
|------------------|-----------|---------|
| **Essential add-on** | Required or near-required accessory | Phone case → screen protector |
| **Natural complement** | Enhances the primary product's use | Face serum → moisturizer |
| **Same-occasion pairing** | Used in the same moment or routine | Coffee → coffee grinder |
| **Upgrade path** | Better version of the same product | Basic → Pro version |
| **Consumable replenishment** | Product the customer will need to replace | Device → replacement filters |
| **Cross-category discovery** | Different category; same customer need | Skincare → body care |

### Step 3 — Identify Upsell vs. Cross-sell

| Type | Definition | Placement | Price ratio |
|------|-----------|-----------|-------------|
| **Upsell** | Upgrade within same product line | Product page, before add-to-cart | +20–50% of base price |
| **Cross-sell** | Add a complementary product | Cart drawer, checkout | 15–35% of cart value |
| **Bundle** | 2–3 products at combined discount | Product page + cart | 10–20% discount |
| **Post-purchase upsell** | Offer shown after payment confirmed | Thank-you page, day-1 email | Any price if friction-free |

### Step 4 — Sequence the Recommendation Flow
Map the customer journey and insert triggers:

1. **Product page** → Show the upsell (same category, higher tier) + "frequently bought together"
2. **Cart** → Show 1–2 cross-sell add-ons (essential add-ons or natural complements)
3. **Checkout** → One-click upsell (bundle or premium version at reduced click cost)
4. **Thank-you page** → Post-purchase offer (different category; 20–30% discount to convert while intent is high)
5. **Day 1 email** → "Complete the set" — what pairs with what they just bought
6. **Day 7–14 email** → "How are you using [Product]?" + "Customers who bought [Product] also loved [X]"
7. **Replenishment email** → Sent at estimated product depletion date (30/60/90 days based on product type)

### Step 5 — Map for Creator Content
For each hero product a creator promotes, provide:
- **"My full routine" products** — The 2–3 products creators can authentically reference alongside the hero
- **Bundle video angle** — How to frame the bundle without it feeling like a pitch ("Everything I used in this transformation")
- **Cross-sell call-to-action** — Specific phrase: "I have the link for the [CROSS-SELL] in my bio too — that's what I used before this"

### Step 6 — Build the Upsell Matrix Output
Deliver a table per product with recommendations, placements, and copy suggestions (see output template).

## Examples

### Example 1 — Skincare Brand (6 Products)

**Product catalog:** Vitamin C serum ($45), Hyaluronic moisturizer ($38), SPF 50 sunscreen ($32), Eye cream ($55), Gentle cleanser ($28), Retinol night cream ($65)

**Upsell Matrix (Vitamin C serum as anchor):**

| Trigger point | Recommended product | Type | Placement | Suggested copy |
|--------------|--------------------|----|-----------|----------------|
| Product page | Retinol night cream ($65) | Upsell | "Complete your routine" | "Vitamin C in the AM + Retinol at night = the duo dermatologists recommend" |
| Cart | Hyaluronic moisturizer ($38) | Cross-sell | "Frequently bought together" | "Layer this after your Vitamin C — seals in the glow" |
| Checkout | AM + PM Bundle ($83, save $10) | Bundle | One-click add | "Grab your complete AM/PM routine at once" |
| Thank-you page | SPF 50 ($32) | Post-purchase | 20% off offer | "Vitamin C works harder when you protect it with SPF — here's 20% off" |
| Day 7 email | Eye cream ($55) | Cross-sell email | "Add to your routine" | "Your skin is starting to adjust — week 2 is when most people notice results. Want to target the eye area too?" |

**GMV impact estimate:** Adding the cross-sell in cart increases AOV from $45 to $67 for buyers who add (+49% AOV lift)

---

### Example 2 — Electronics Store (Wireless Earbuds)

**Anchor product:** Wireless earbuds ($79)

**Natural upsell/cross-sell chain:**
1. **Product page upsell:** Pro version with ANC ($119) — "Want noise cancellation?"
2. **Cart cross-sell:** Carry case ($18) — "Protect your investment — case fits in any pocket"
3. **Checkout cross-sell:** 2-year extended warranty ($12) — "One-click add — covers drops and water damage"
4. **Thank-you page:** Wireless charging pad ($25, 15% off) — "One charger for all your devices"
5. **Day 30 email:** Replacement ear tips 3-pack ($14) — "Keep your audio quality at peak — tips wear over 3–6 months"

## Common Mistakes

1. **Cross-sells that are too expensive** — Recommending a $150 add-on to someone who bought a $30 item creates dissonance and is ignored; stay under 35% of cart value
2. **Too many recommendations at once** — 6 cross-sell suggestions paralyze the buyer; limit to 2 on-page, 1 in cart, 1 at checkout
3. **Ignoring the post-purchase window** — The confirmation page has 100% open rate and highest intent; most brands waste it with just order details
4. **Bundles with no discount** — A bundle at the same price as buying items separately offers no reason to bundle; minimum 10% discount to activate the mental shortcut
5. **Cross-selling unrelated products** — Recommending phone cases on a kitchen appliance page confuses buyers and increases exit rate
6. **No replenishment email for consumables** — For any product used up (supplements, skincare, filters, coffee), set a replenishment email at expected depletion date
7. **Creator content missing the cross-sell CTA** — Creator videos that mention only one product miss the chance to drive basket building; brief the creator on 1–2 natural companion products to mention
8. **Not A/B testing placement** — Cross-sell performance varies widely by placement; test cart drawer vs. checkout page vs. post-purchase before scaling

## Resources

- [Product Relationship Matrix Template](references/product-matrix-template.md)
- [Post-Purchase Email Sequence Guide](references/post-purchase-emails.md)
- [Output Template](references/output-template.md)
- [Upsell Quality Checklist](assets/upsell-checklist.md)
