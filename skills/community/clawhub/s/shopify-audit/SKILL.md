---
name: shopify-audit
description: Audit Shopify store pages for conversion blockers including slow load, weak copy, missing trust signals, and friction in the add-to-cart flow. Use when add-to-cart or checkout conversion is low, before major sales events (BFCM, launches), after a redesign or theme change, or when paid traffic converts poorly despite good CTR.
---

# Shopify Audit

Your Shopify store may look polished, but hidden conversion blockers could be costing you 20–40% of potential sales. This skill conducts a structured audit of your storefront — homepage, collection pages, product detail pages, and checkout — identifying friction points in copy, design, trust, and performance that prevent browsers from becoming buyers, then outputs a prioritized fix list your team can implement in Shopify's theme editor or app ecosystem, in most cases without a developer.

## Quick Reference

| Decision | Strong | Acceptable | Weak |
|---|---|---|---|
| Audit order | Funnel sequence: homepage → collection → PDP → cart → checkout | PDP-first when one product dominates traffic | Random page-by-page notes |
| Prioritization | Sorted by estimated revenue impact × implementation effort | Sorted by funnel position | Unordered list of 50 observations |
| Copy assessment | Benefit-led headline ≤8 words, scannable bullets, objection-handling | Clear feature descriptions | "Welcome to our store" headlines |
| Trust signals | Reviews near ATC button, payment badges at checkout, visible return policy | Reviews somewhere on PDP | No reviews, policy buried in footer |
| Mobile audit | Separate pass — thumb reach, sticky ATC, image weight on 4G | Spot-check key pages on mobile | Desktop-only audit |
| Performance | LCP <2.5s on PDP, hero image optimized, apps audited for script bloat | Image compression done | "Theme feels fast" with no measurement |
| Fix specification | Exact rewrite or theme-editor step provided per finding | Direction + example | "Improve your product copy" |

## Solves

- Add-to-cart rate below ~5% with traffic arriving but no diagnosis of why
- Checkout abandonment from surprise costs, forced accounts, or missing payment methods
- Paid traffic that clicks but doesn't convert, burning ad spend on a leaky funnel
- Pre-BFCM/launch readiness with no structured way to find friction before the spike
- Post-redesign conversion drops nobody can explain
- Audit reports full of observations but no prioritized, executable fixes
- Mobile experience failures invisible to a desktop-working team

## Workflow

### Step 1: Collect inputs and baseline metrics

Required: store URL and the top product or collection URL (primary audit target). Strongly recommended: current conversion rate, add-to-cart rate, device split, and top traffic source — these calibrate what "good" looks like and where to weight the audit. A store with 80% mobile paid-social traffic gets audited differently than one with desktop search traffic.

### Step 2: Homepage first impression (5-second test)

Assess above-the-fold: can a stranger answer "what do they sell, for whom, why here" in 5 seconds? Check: benefit-led headline (≤8 words), hero image showing product in use, single primary CTA, load weight of the hero, announcement-bar clarity (shipping threshold beats vague slogans), and nav depth (≤6 top-level items).

### Step 3: Collection page browsability

Check: product card info sufficiency (price, variant cues, review stars on cards), filter and sort presence for catalogs >12 items, image consistency across cards, dead-end prevention (empty filter states), and pagination vs. infinite scroll fit for catalog size.

### Step 4: Product page persuasion (the core of the audit)

Audit in order of visual hierarchy: title and price clarity (including any compare-at framing), image set (≥5, zoomable, lifestyle + scale reference), benefit-led description with scannable structure, social proof placement (review count + stars visible without scrolling on mobile), shipping/returns visibility near the ATC button, variant picker usability, sticky ATC on mobile, urgency honesty (no fake timers), and cross-sell placement below the fold.

### Step 5: Cart and checkout friction

Check: cart accessibility (slide-out vs. page), surprise-cost prevention (shipping calculator or threshold messaging before checkout), express payment options (Shop Pay, Apple Pay, Google Pay), guest checkout enabled, form field count, trust badges at payment step, and order-summary clarity. Shopify checkout is largely fixed — the wins are in what enters it: shipping expectations, payment options, and cart add-ons.

### Step 6: Performance and mobile pass

Measure (PageSpeed Insights or Lighthouse): LCP <2.5s target on PDP, image formats (WebP/AVIF), app script audit (each review/upsell/chat app adds JS — uninstall dead apps, lazy-load the rest), font weight count. Then a mobile-only pass: thumb-reachable ATC, readable type without zoom, tap-target spacing, sticky elements not covering content.

### Step 7: Compile the prioritized report

Sort findings by estimated revenue impact (traffic to that page × severity) against implementation effort. Deliver per `references/output-template.md`: each finding gets location, evidence, estimated impact, and an executable fix (exact copy rewrite or theme-editor steps). Cap the list at 15 items — a 50-item audit is a backlog, not a plan. Verify with `assets/audit-quality-checklist.md`.

## Example 1: Skincare DTC store, 2.1% ATC rate

**Inputs:** glowlab.com (Dawn theme), top PDP = Vitamin C serum, 78% mobile, paid social traffic, ATC 2.1%.

**Output (excerpt):**

> **Finding 1 (PDP, high impact / low effort):** Review stars render below the fold on mobile; first visible social proof is at scroll depth 3. Fix: enable the star-rating block in the Dawn product template header area, directly under the title. Evidence: 78% mobile traffic; heatmap-typical drop-off before scroll 2.
>
> **Finding 2 (PDP, high impact / low effort):** Description opens with "Our story began…" — brand story before benefits. Fix (exact rewrite provided): "Visibly brighter skin in 14 days — 15% stabilized Vitamin C, zero stickiness. 4,200+ five-star reviews." Story moves to an accordion.
>
> **Finding 3 (cart, high impact / medium effort):** Shipping cost first appears at checkout ($6.95) — classic surprise-cost abandonment. Fix: announcement bar "Free shipping over $45" + cart progress meter (native in Dawn settings).
>
> **Finding 5 (performance):** Hero video 8.2MB autoplay on 4G; LCP 4.9s. Fix: replace with 180KB poster + tap-to-play; compress PDP images to WebP. Expected LCP <2.5s.

## Example 2: Pre-BFCM readiness, home goods store

**Inputs:** 340-SKU catalog, desktop-heavy email traffic, checkout completion 38%, BFCM in 3 weeks.

**Output (excerpt):**

> **Checkout findings:** Guest checkout disabled (account required) — single highest-impact fix available; express payments not enabled (Shop Pay toggle off in Payments settings); discount-code field prominent but most codes invalid → switch BFCM pricing to automatic discounts so the field doesn't send buyers off-site hunting codes.
>
> **Collection findings:** No "Gifts under $50" collection despite email promoting gift angles; filters missing price ranges; sale-price display shows discount only on PDP, not cards → enable compare-at on cards before sale starts.
>
> **Load-test flag:** 14 apps injecting scripts; 3 unused (uninstall), chat widget defer-loaded. BFCM traffic spike at current LCP (3.8s) projected to cost measurable revenue; fix before, not during.

## Common Mistakes

1. **Auditing aesthetics instead of friction.** "The font feels dated" is a redesign note, not a conversion finding. Every finding must name the buyer behavior it blocks.
2. **Desktop-only audits for mobile-majority stores.** Most Shopify stores see 70%+ mobile sessions; an audit without a dedicated mobile pass misses the majority experience.
3. **Unprioritized finding dumps.** 50 unranked observations get zero implemented. Impact × effort ranking, capped at 15, gets fixed.
4. **Vague fixes.** "Strengthen your value proposition" helps nobody. Provide the rewritten headline, the theme-editor path, or the app setting to change.
5. **Ignoring what feeds checkout.** Teams obsess over Shopify's locked checkout while the real losses are surprise shipping costs and missing express payments — both fixable.
6. **Trusting fake urgency.** Countdown timers that reset destroy trust and risk consumer-protection issues; flag them for removal, not optimization.
7. **Skipping the app audit.** Conversion apps accumulate; each adds scripts. The audit must list installed apps against their measurable value.
8. **No baseline metrics.** Without current ATC/conversion rates, the audit can't prioritize or prove improvement. Insist on the numbers, even rough ones.
9. **One-time audits.** Themes update, apps change, catalogs grow. Schedule the re-audit (quarterly or pre-peak) as the report's final line item.

## Resources

- `references/output-template.md` — prioritized audit report structure
- `references/page-by-page-guide.md` — detailed checks per funnel stage (homepage, collection, PDP, cart, checkout)
- `references/trust-and-performance-guide.md` — trust-signal placement patterns and Core Web Vitals targets for Shopify themes
- `assets/audit-quality-checklist.md` — full audit coverage checklist (45+ items)
