# Page Type Interpretation Guide

How to interpret heatmap metrics for each page type. Read the relevant section based on the
classified page type before generating analysis.

## Cross-page-type analysis patterns

### impressionRate drop pattern (all page types)
When impressionRate drops sharply between consecutive blocks (e.g., block 4 at 75% → block 5 at
40%), this transition is a "scroll cliff" — a significant portion of users stopped scrolling at
that point. Note this in the narrative. The content transition at the cliff often reveals why
users decided the page was no longer worth scrolling: the preceding block may have answered their
question, lost their interest, or triggered an exit decision.

### Sample size awareness (all page types)
When total page visits are below ~100, or individual block impressions are very low, treat all
metric-based conclusions as directional signals rather than definitive findings. Use stronger
hedging language and flag the limited data in core_insight if page visits < 50.

---

## ad_lp (Advertising Landing Page)

**Primary user intents**: Quickly judge relevance → understand value/proof → resolve concerns → act

**Core blocks**: value props/effects, pain points, pricing/offer, trust/proof, CTA
**Utility blocks**: FAQ, shipping/returns, contact, footer

**High dwell hints**:
- Re-checking proof ("does it really work / is it for me?")
- Calculating/comparing at pricing (if exit also high → concentrated hesitation)
- Pre-purchase verification at FAQ/rules

**High exit hints**:
- Relevance unclear / first view not intuitive → quick leave
- Insufficient proof / trust not established → read then leave
- Pricing/constraints/guarantees unclear → hesitate then leave
- CTA unclear / next step missing → arrive then leave

**Misread reminders**: High exit can be filtering, external comparison, or offline action. Always interpret with dwell, impression, CTA clicks, and context.

---

## sales_lp (Campaign / Sale Landing Page)

**Primary user intents**: Understand campaign value → learn rules → browse/select products → checkout

**Core blocks**: campaign value summary, rules/terms, product lists, category nav, urgency, CTA
**Utility blocks**: FAQ, support, footer

**High dwell hints**:
- Reading rules carefully (risk/eligibility check)
- Comparing deals or choosing products (normal)
- High dwell + high exit at terms/pricing → friction or confusion

**High exit hints**:
- Value unclear / rules confusing → quick leave
- Product selection difficult → browse then leave
- CTA timing/path unclear → arrive then leave

**Misread reminders**: Sale pages have scanning behavior; interpret with clicks to PDP/cart and conversion funnel.

---

## pdp (Product Detail Page)

**Primary user intents**: Confirm product fit → validate trust → decide and purchase

**Core blocks**: product title/price/variants, key benefits, images/video, specs, social proof, shipping/returns, guarantees, CTA
**Utility blocks**: recommendations, footer

**High dwell hints**:
- Comparing variants/specs and checking details
- Verifying reviews/proof before committing
- High dwell at shipping/returns → risk evaluation

**High exit hints**:
- Missing key info (price/specs/fit) → leave to compare
- Trust concerns not resolved → read then leave
- CTA unclear or purchase friction → arrive then leave

**Misread reminders**: Some exits can be "compare and come back"; interpret with click signals and downstream funnel.

---

## homepage

**Primary user intents**: Identify brand match → find next path → build trust

**Core blocks**: hero/FV, navigation hubs, category/product highlights, trust signals, primary CTA
**Utility blocks**: newsletter, footer links, policy links

**High dwell hints**:
- Scanning options, deciding where to go
- Verifying trust signals or differentiators

**High exit hints**:
- Positioning unclear / too many choices → quick leave
- Navigation weak / no obvious next step → arrive then leave
- Trust insufficient → leave after browsing

**Misread reminders**: Homepage behavior includes exploration; interpret with clicks, scroll reach, and downstream navigation.

---

## article_lp (Content / Article Landing Page)

**Primary user intents**: Obtain information / be persuaded → find next action (CTA, product, subscribe)

**Core blocks**: article structure, key conclusions, CTA, author/source credibility
**Utility blocks**: recommendations, comments, subscription, share, footer

**High dwell hints**:
- Content being read carefully (normal)
- High dwell + high exit → information load, weak credibility, or "read but no action"

**High exit hints**:
- Opening not engaging / weak relevance → quick leave
- Weak argument / insufficient credibility → read then leave
- CTA timing unnatural / path unclear → finish reading then leave

**Reading completion rate**: For article pages, the last content block's impressionRate is a proxy
for reading completion rate. If only 15% of visitors reach the final content block, the article
may be too long or loses interest midway. Track where impressionRate drops sharply to identify
the "reading cliff" — the point where most users stop scrolling.

**Misread reminders**: "High exit" may be a natural endpoint. Distinguish "read then leave" vs "read then act" using CTA clicks.

---

## other_content (Universal Content Page)

**Primary user intents**: Assess relevance → explore content → find information → identify next step

**Core blocks vary by sub-type**:
- Recruitment: job overview, requirements, culture, application CTA
- Corporate: brand intro, business overview, key messages
- FAQ/Help: question categories, answer body, search
- Blog: headline, body content, key takeaways
- Pricing: plan comparison, pricing table

**High dwell hints**:
- Reading carefully to assess relevance or make a decision — **positive** signal
- On FAQ: finding/verifying answer — expected
- High dwell + low exit → strong attention

**High exit hints**:
- Content doesn't match user expectations (relevance mismatch)
- No clear next step or CTA
- On FAQ: quick exit after reading may be **positive** (answer found)
- On recruitment: exit at requirements → self-screening (normal)

**E-commerce isolation rule (MUST)**: This is NOT an e-commerce page. NEVER frame analysis around "price concerns" or "persuasion failed" unless explicit checkout CTA is present.

---

## other_function (Universal Functional Page)

**Primary user intents**: Complete operation quickly → get past this step → recover from error

**Core blocks**: primary form/action (login, signup, checkout)
**Utility blocks**: header, help links, footer

**CRITICAL — Reversed interpretation**:

**High dwell = FRICTION (not engagement)**:
- Long dwell on form → confused by fields, encountering errors, unsure what to enter
- Long dwell on feedback → error/success state unclear
- NEVER interpret high dwell as "reading carefully" on functional pages

**Quick exit = possible SUCCESS**:
- Low dwell + high conversion = smooth task completion (ideal)
- Low dwell + low conversion = likely failure (gave up)
- High dwell + high exit = strongest friction signal (struggled and abandoned)

**E-commerce isolation rule (MUST)**: NEVER use "relevance", "resonance", "trust building", or "persuasion" frameworks. Functional pages facilitate, not persuade.

**Analysis focus**:
- Phase 1: Can users identify the function and where to act?
- Phase 2: Any signs of hesitation or error in the action zone?
- Phase 3: Are error/success states clearly communicated?
- Phase 4: Clear guidance to next destination after completing?
