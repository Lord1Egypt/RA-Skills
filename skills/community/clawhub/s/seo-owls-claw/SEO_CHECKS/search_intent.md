# SEOwlsClaw — Search Intent Detection Guide (v1.0)

**Purpose:** Detect the real meaning and intent behind a keyword BEFORE writing any content.
**Status:** CRITICAL — Wrong intent = wrong page format = no ranking. Run this first, always.
**When loaded:** Step 1 of the brain workflow (before persona, before template, before writing). ALWAYS use Search Intent Detection **BEFORE Writing Any SEO Content**

---

## Why This Matters

A keyword like `Meyer` could mean:
- **Meyer Optik** — a vintage lens brand (photography)
- **Meyer Watches** — a Swiss watch manufacturer
- **Meyer Bau** — a construction company in Germany

Without checking the actual SERP first, the agent is guessing. This file teaches the agent to
**look first, then decide** — using real search results to understand what Google (and users)
actually associate with any given keyword before scoring intent or choosing a format.

---

## The 5-Step Process

```
Step 1  SERP Lookup        Fetch real search results via Brave API
Step 2  Keyword Understanding   Disambiguate entity, topic, and market context
Step 3  Intent Scoring          Score the query for the 4 intent types
Step 4  Format Selection        Map dominant intent → page type + detect conflicts
Step 5  Output Planning Block   Produce the internal plan before writing begins
```

---

## Step 1 — SERP Lookup (Brave API)

**Run before any intent scoring. Always.**
** Make sure that the user has enabled the Brave API for web searches. If not you can point to the official Brave API Guide `https://brave.com/search/api/guides/use-with-openclaw/` for how-to.
You as agent need to fetch the top 5 real search results for the primary keyword and uses them to understand what the keyword actually means in the real world and in the target market.

**Tool scope:** READ-ONLY — fetches public search results only. No credentials, no authentication, no data submission. Never runs autonomously in the background.
Uses the OpenClaw built-in search tool (Brave Search works best and have been tested).
The skill does not store, transmit, or log any search results.
Trigger: only runs when the user issues /research, /write, /writehtml, or /checks.

### Tool Call

```yaml
name: search-regional
description: Perform web search with country/language targeting using Brave Search API and fetch top SERP results for keyword disambiguation and intent validation
parameters:
  query: <primary_kw from user prompt>
  type: Search query string
  count: 5
  country:  <from user prompt --lang flag → de=DE, fr=FR, es=ES, pt=PT, else US>
  language: <from user prompt --lang flag → de=de, fr=fr, es=es, pt=pt, else en>
output_format:
  results:
    - title
    - url
    - description
```

### Example Call

```bash
# User prompt: /write Productused "Meyer lens 50mm f1.8 used" --lang de
web_search(query="Meyer lens 50mm f1.8 used", count=5, country="DE", language="de")
```

### What to Extract From Results

Many keywords are not pure single-intent queries. Identify the dominant intent first, then satisfy the secondary intent in supporting sections.
For each of the 5 results, identify:

| Field | What to Look For |
|-------|-----------------|
| **Entity type** | Is this a brand? A product? A person? A topic? |
| **Page type** | Product page, blog post, brand homepage, category page, Wikipedia, news |
| **Domain pattern** | Shop (.de shop), informational (.org, wiki), brand official site |
| **Title pattern** | Does it contain "kaufen", "buy", "guide", "was ist", "review", "best"? |

### SERP Classification Table

After reading 5 results, classify the dominant SERP type:

| Dominant Result Type | What It Signals | Agent Action |
|---------------------|-----------------|--------------|
| Product pages / shop listings | Transactional — buying keyword | Proceed → Transactional scoring |
| Blog posts / guides / tutorials | Informational — learning keyword | Proceed → Informational scoring |
| Comparison / "best of" articles | Commercial — evaluation keyword | Proceed → Commercial scoring |
| Brand homepages / category pages | Navigational — destination keyword | Proceed → Navigational scoring |
| Wikipedia / encyclopedic pages | Informational — definition/reference keyword | Proceed → Informational scoring |
| FAQ pages / heavy PAA boxes | Informational — question-based keyword | Proceed → Informational, recommend FAQ page type |
| News articles / press releases | News intent — time-sensitive keyword | ⚠️ Warn user: evergreen content unlikely to rank here |
| Forum posts / Reddit / Quora | Community intent — experience/opinion keyword | ⚠️ Warn user: hard to compete, consider a different angle |
| YouTube / video results | Video intent — visual/tutorial keyword | ⚠️ Warn user: consider video content or video-embedded blog |
| Google Maps / local results | Local intent — "near me" or location keyword | ⚠️ Warn user: needs local SEO approach, not standard content |
| Knowledge Panel (entity card) | Navigational — specific known entity | Proceed → Navigational scoring |
| Mixed — same topic, different page types | Hybrid intent | Proceed → full scoring algorithm to decide |
| Mixed — completely different entities | Disambiguation needed | ⚠️ Ask user ONE clarifying question before proceeding |

---

## Step 2 — Keyword Understanding (Disambiguation)

After the SERP lookup, you must answer these 3 questions before scoring:

**Q1 — What is this keyword about?**
Identify the entity, topic, product, brand, or concept the keyword refers to.
Use SERP titles and descriptions — not internal knowledge alone.

```
Keyword: "Meyer"
SERP result 1: "Meyer Optik Görlitz — Trioplan 100mm Lens"       → Photography brand
SERP result 2: "Meyer & Friends Uhren — Schweizer Qualität"       → Watch brand
SERP result 3: "Meyer Bau GmbH — Ihr Baupartner in Bayern"        → Construction company
→ DISAMBIGUATION REQUIRED ⚠️
```

```
Keyword: "Meyer Optik Trioplan kaufen"
SERP result 1-5: All lens/photography product pages
→ Clear. Entity = Meyer Optik (lens brand). No disambiguation needed. ✅
```

**Q2 — What market/context does this keyword belong to?**
Use the `--lang` flag country code to confirm the regional market context.
A keyword can have different dominant meanings in different countries.

**Q3 — Is the entity clear enough to proceed?**

```
IF SERP results show 2+ completely different entity types with no overlap:
  → Ask user ONE clarifying question before proceeding
  → Example: "I found results for Meyer Optik (lenses), Meyer Watches, and Meyer Bau
    (construction). Which Meyer are you writing about?"

IF SERP results show a clear dominant entity (4-5 results same topic):
  → Proceed to Step 3 with confirmed entity context
```

---

## Step 3 — Intent Scoring

Now score the keyword using both the SERP data (Step 1) and the query text.
The SERP result acts as a validation layer on top of the text-based scoring.

### The Intent Types

---

### 3.1 Informational — User Wants to Learn

**Goal:** Learn, understand, or solve a question
**Mindset:** Curious, early research stage, not ready to buy yet

**Trigger words:** how, what, why, when, where, who, guide, tutorial, tips, explained,
learn, overview, meaning of, Erklärung, Anleitung, was ist, wie funktioniert

**SERP signals:** Blog posts dominate, FAQ boxes visible, People Also Ask prominent,
Wikipedia or .org sites in top 5, explainer-style titles

**Examples:**
- `how to break in new hiking boots` → guide
- `what is a rangefinder camera` → explainer article
- `why do trail running shoes wear out fast` → informational guide
- `gore-tex explained` → glossary / explainer
- `best time to hike the Dolomites` → informational guide (despite "best")

**Best formats:** Blogpost, FAQ page, Guide, Tutorial, Glossary entry
**Tone:** Educational, neutral, clear, step-by-step
**CTA:** Read related guide · Explore category · See recommended products

---

### 3.2 Navigational — User Wants a Specific Destination

**Goal:** Reach a known brand, store, page, or destination directly
**Mindset:** Already knows where they want to go, wants fast access

**Trigger words:** [brand name], [shop name], official site, homepage, login,
contact, store, category + brand name, model + store name

**SERP signals:** One brand/domain dominates all 5 results, sitelinks appear
under a brand result, official pages only, Knowledge Panel visible

**Examples:**
- `Salomon hiking boots official site` → brand homepage
- `Deuter backpacks` → brand/category page
- `TrailPro shop contact` → contact/store page
- `JBV Foto Leica` → brand category page

**Best formats:** Homepage, Brand page, Category page, Store locator, Contact page
**Tone:** Direct, brand-led, trust-oriented, minimal friction
**CTA:** Visit page · Browse products · Contact store · Go to category

---

### 3.3 Commercial Investigation — User is Comparing Options

**Goal:** Research and compare options before making a purchase decision
**Mindset:** Interested in buying, needs evidence and recommendations first

**Trigger words:** best, top, review, vs, versus, comparison, compare, worth it,
pros and cons, recommended, test, Vergleich, Empfehlung, lohnt sich

**SERP signals:** "Best of" lists dominate, comparison articles rank, affiliate/review
sites in top 5, star ratings visible, multiple brand names in titles

**Examples:**
- `best hiking boots for wide feet 2026` → buying guide
- `Salomon vs Merrell trail shoes` → comparison page
- `trail running shoes review` → review article
- `hiking boot brands worth buying` → buying guide / round-up
- `waterproof hiking boots pros and cons` → comparison article

**Best formats:** Buying guide, Comparison page, Review article, Best-of round-up
**Tone:** Expert, balanced, evidence-based, trust-building
**CTA:** View product · Check price · Compare models · Shop recommended options

---

### 3.4 Transactional — User is Ready to Buy

**Goal:** Complete a purchase, order, or action right now
**Mindset:** Decision made or nearly made, needs price/availability/trust confirmation

**Trigger words:** buy, kaufen, order, shop, price, preis, cheap, günstig, deal,
discount, in stock, shipping, available, used, mint condition, boxed, for sale

**SERP signals:** Product pages dominate, category pages rank, Google Shopping ads
visible, price and condition visible in snippets, checkout/cart pages present

**Examples:**
- `buy waterproof hiking boots size 43` → product page
- `Salomon X Ultra 4 GTX price` → product page
- `used trail running shoes for sale` → used product page
- `hiking boots sale free shipping` → category or landing page
- `Leica M6 TTL kaufen` → product page

**Best formats:** Productnew, Productused, Category page, Landingpage, Offer page
**Tone:** Direct, benefit-first, action-oriented, reassuring
**CTA:** Buy now · Add to cart · Check availability · Order today

---

## Step 3 — Scoring Algorithm

After reading SERP results and identifying the intent type, calculate a final score:

```
Weight breakdown:
  SERP dominant page type    →  40% of final score
  Primary keyword analysis   →  35% of final score
  Query trigger words        →  15% of final score
  Query modifiers            →  10% of final score
```

### Scoring Steps

**1. SERP Score (30%)**
Count the 5 SERP results. What type are most of them?

| SERP Dominant Type | Points |
|-------------------|--------|
| Product pages / shop listings | +4 → Transactional |
| Buying guides / best-of lists | +4 → Commercial |
| Blog posts / tutorials / explainers | +4 → Informational |
| Brand homepages / official pages | +4 → Navigational |
| Mixed (no dominant type) | +1 across all → trigger disambiguation |

**2. Primary Keyword Score (40%)**
What is the first strong signal in the keyword?

| Signal Found | Points |
|-------------|--------|
| Starts with buy / kaufen / order | +4 → Transactional |
| Contains vs / comparison / review | +4 → Commercial |
| Starts with how / what / why / guide | +4 → Informational |
| Brand name only, no modifiers | +3 → Navigational |

**3. Trigger Word Score (10%)**
Count matching trigger words from each category. Max +3 per category.

**4. Modifier Score (20%)**
Check for strong modifiers that override:

| Modifier | Override |
|----------|---------|
| "buy" anywhere in query | +3 Transactional |
| "official", "site", "login" | +3 Navigational |
| "how", "what" at query START | +2 Informational |
| price/cost/günstig/cheap | +2 Transactional |

### Scoring Example

```
Keyword: "best waterproof hiking boots 2026"

SERP results: 4 buying guide articles, 1 product category page
→ SERP score: +4 Commercial

Primary keyword: "best" → Commercial
→ Primary score: +4 Commercial

Trigger words: "best" → +1 Commercial
→ Trigger score: +1

Modifier: none overriding
→ Modifier score: 0

Final: Commercial dominates → Format: Buying Guide / Blogpost (comparison)
```

---

## Step 4 — Format Selection & Conflict Detection

### Intent → Page Type Mapping

| Dominant Intent | Secondary Intent | Best Page Type |
|----------------|-----------------|----------------|
| Transactional | Informational | `Productused` or `Productnew` (+ short explainer section) |
| Transactional | Commercial | `Productnew` or `Productused` (+ comparison with alternatives) |
| Commercial | Transactional | `Blogpost` (buying guide with product links) |
| Commercial | Informational | `Blogpost` (comparison + explainer) |
| Informational | Navigational | `Blogpost` (guide with internal links to category) |
| Navigational | Commercial | `Landingpage` or category page |
| Mixed (ambiguous) | — | ⚠️ Always ask user ONE clarifying question |

### Conflict Detection

If the user specifies a page type that conflicts with detected intent → flag it before writing:

```
⚠️ INTENT CONFLICT DETECTED

User requested: Blogpost
Detected intent: Transactional (SERP: 4 product pages, keyword: "buy hiking boots")

A blog post format will not match what Google is ranking for this keyword.
Suggestion: Use Productnew or Productused instead.

→ Should I proceed with the requested Blogpost anyway, or switch to Productused?
```
### Page Type → Intent Reference (Reverse Lookup)

Use this when you know the page type and need to confirm the expected intent and format approach.

| Page Type | Primary Intent | Secondary Intent | Recommended Format |
|-----------|---------------|-----------------|-------------------|
| Homepage | Navigational | Commercial | Brand-led overview with clear category access |
| Brand page | Navigational | Commercial | Brand intro + listings + trust copy |
| Category page | Transactional | Commercial | Short SEO intro + filters + product grid |
| Productnew | Transactional | Commercial | Specs + features + trust + CTA |
| Productused | Transactional | Commercial | Condition + specs + trust + CTA |
| Blogpost | Informational | Navigational | Educational article with internal links |
| Buying guide | Commercial | Transactional | Comparison + recommendation + product links |
| Comparison page | Informational | Commercial | Side-by-side analysis + verdict |
| FAQ page | Informational | Navigational | Short answers + links to deeper pages |
| Landingpage | Transactional | Commercial | Offer-focused + urgency + single CTA |
| Socialphoto | Navigational | Informational | Visual-first + short caption + alt text |
| Socialvideo | Navigational | Commercial | Hook + description + tags + CTA |

### Fallback Rules (When Scores Are Tied)

```
1. SERP dominant type wins over text signals when scores are within 5%
2. If SERP is mixed + text signals tied → default to COMMERCIAL (safer for e-commerce)
3. Brand-only query + no modifiers + navigational SERP → default NAVIGATIONAL
4. Question word at start (how/what/why) → always lean INFORMATIONAL regardless of other signals
5. Price/condition/availability in query → always lean TRANSACTIONAL regardless of season
6. If disambiguation was required and user answered → re-run SERP lookup with full entity name
```

---

## Step 5 — Output Planning Block

Before writing a single word of content, output this internal planning block.
This block is visible to the user so they can confirm or correct before generation starts.

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 INTENT ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Keyword:              best waterproof hiking boots 2026
Entity confirmed:     Waterproof hiking boots (footwear category)
SERP dominant type:   Buying guide / comparison articles
Primary intent:       Commercial Investigation
Secondary intent:     Transactional

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📄 FORMAT DECISION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Page type:            Blogpost (buying guide)
Template:             blog_post_template.md
Conflict detected:    None

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✍️ WRITING PLAN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
H1 pattern:           Best [Product] for [Use Case] — [Year]
Recommended Tone:     Expert, balanced, trust-building
Target word count:    1,800–2,500w
CTA style:            View product · Check price
Primary keyword:      best waterproof hiking boots 2026
Essential sections:   Comparison table · Top picks by use case · FAQ
Internal link targets: Product pages · Category: hiking boots
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Proceeding to Step 2 (Load Persona)...
```

---

## Quick Reference

| Intent | Goal | SERP Signs | Best Format | CTA |
|--------|------|-----------|-------------|-----|
| Informational | Learn / understand | Blogs, guides, FAQ, wiki | Blogpost, FAQ | Read more, explore |
| Navigational | Reach known destination | Brand pages, sitelinks, knowledge panel | Homepage, Category | Browse, visit, contact |
| Commercial | Compare before buying | Best-of lists, reviews, comparison articles | Blogpost (buying guide) | View product, check price |
| Transactional | Buy / act now | Product pages, shopping ads, category pages | Productnew, Productused | Buy now, add to cart |

---

## Common Mistakes — Never Do These

| Mistake | Example | Fix |
|---------|---------|-----|
| Blog format for transactional keyword | Blog for "buy hiking boots size 43" | Use Productused or Productnew |
| Product page for informational keyword | Product page for "how to choose hiking boots" | Use Blogpost guide |
| Skipping SERP lookup for ambiguous keywords | Assuming "Meyer" = lenses without checking | Always run Step 1 first |
| Generic overview for commercial keyword | No shortlist for "best trail shoes" | Always include top picks + criteria |
| No trust signals on transactional pages | Missing condition, price, return policy | Add all four trust elements |
| Mixing intent in one piece | Educational intro on a transactional product page | Keep primary intent dominant throughout |

---

## Edge Case: Ambiguous Brand Names

When a brand name alone is used as the primary keyword and SERP results show 2+ unrelated businesses:

```
⚠️ DISAMBIGUATION REQUIRED

Keyword: "Meyer"
SERP results found:
  1. Meyer Optik Görlitz — Vintage lens manufacturer (photography)
  2. Meyer & Friends — Swiss watch brand
  3. Meyer Bau GmbH — Construction company, Bavaria

I found 3 completely different businesses named "Meyer".
Which one are you writing about?

→ Options:
  A) Meyer Optik (lenses / photography)
  B) Meyer Watches
  C) Meyer Bau (construction)
  D) Other — please describe
```

After user answers → re-run SERP lookup with full entity name (`Meyer Optik Trioplan`)
→ then proceed from Step 3 with confirmed entity context.

---

*Last updated: 07-04-2026 (v0.6)*
*Maintainer: Chris — SEOwlsClaw search intent detection, complete rebuild with SERP lookup*
