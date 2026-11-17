# SEOwlsClaw — Complete SEO Path Workflow (v0.9.2)

## Purpose
This document maps out the full SEO workflow for SEOwlsClaw: Research → Keyword Cluster → Content Gap Analysis → Persona-Driven Writing → Template Generation → Final Quality Checks.

**Use this guide to understand how all components work together before deployment.**

---

## Step 1: Research Phase — Keyword Discovery & SERP Analysis
**Command**: `research <topic>`

### What Gets Generated
```markdown
## Primary Keyword (High Intent, High Volume)
- Target: "best hiking water bottles Berlin"
- Volume: ~50 searches/month in Germany
- Difficulty: 42/100 (moderate competition)

## Long-Tail Variations (Lower Competition)
1. "Best sustainable hiking water bottles for winter hikes" — 35 m/mo, Diff: 18
2. "Water bottle capacity vs insulation comparison" — 22 m/mo, Diff: 31
3. "Refurbished water bottles Berlin discount" — 12 m/mo, Diff: 5

## SERP Features Detected (Page Type Guide)
- Featured Snippets opportunity (comparison table in #4)
- People Also Ask section (how to choose bottle?)
- Video results (product reviews on YouTube)
- Image pack (water bottle buying guide images)
```

### How It Works
1. Web search query for main topic + keywords from your content brief
2. Analyzes SERP structure (snippets, images, videos detected)
3. Identifies keyword clusters related to primary target
4. Flags competitive gaps and content opportunities

**Example Usage**:
```text
persona Researcher research best-hiking-water-bottles-berlin-2026
```

---

## Step 2: Content Gap Analysis — Compare vs Competitors
**Command**: `checks <url>` or manual analysis via SKILL.md variables

### What Gets Analyzed
```markdown
## Competitive Benchmark (Example)
URL: https://competitor.com/best-water-bottles-guide
Strengths: Comparison table, word count 2.5k+, video integration
Weaknesses: No schema markup, thin FAQ section, missing H1 keywords

## Our Opportunities
- Add comparison tables (SEO gold for featured snippets)
- Include schema.org Article + FAQ structure
- Expand FAQ section with Q&A format (People Also Ask optimization)
```

### How It Works
1. Identify main keyword + target audience intent
2. Find 2-3 competitor URLs for reference
3. Analyze what they have right (structure, schema, depth)
4. Spot gaps we can fill (unique angles, missing sections)

**Example Usage**:
```text
checks https://example.com/best-hiking-water-bottles-guide
persona Researcher /write Blogpost "Best Hiking Water Bottles for Berlin — Complete 2026 Guide"
```

---

## Step 3: Persona Selection & Writing Style Setup
**Command**: `persona <name>` (run BEFORE /write)

### Available Personas
| Persona | Best For | Style Profile |
|---------|----------|--------------|
| **E-Commerce Manager** | Product pages, sales campaigns | Persuasive, urgency-driven, benefit-focused |
| **Creative Writer** | Brand storytelling, emotional content | Story-driven, vivid imagery, relatable |
| **Blogger** | Educational guides, evergreen articles | Clear structure, actionable tips, professional yet approachable |
| **Researcher** | Data-driven content, competitor analysis | Fact-based, neutral tone, question-first format |
| **Travel Photographer** | Scenario-specific gear recommendations, travel photography guides, destination-based camera content |
| **Vintage Expert** | Vintage camera listings, collector guides, authenticity verification content, historical model deep-dives |

### How To Use
```text
# Step 3a: Set your writing persona
persona E-Commerce Manager --tone enthusiastic

# Step 3b: Write content with this persona
persona E-Commerce Manager write Landingpage "We're offering massive discounts on premium electronics — limited time only" --primary-kw summer-sale-electronics

# Or combine personas for complex tasks
persona Creative Writer --vocabulary "dream, journey, adventure" /write Blogpost "Sustainable Hiking Gear Guide"
```

---

## Step 4: Template Selection & Content Generation
**Command**: `write <type> "content_prompt"`

### Supported Page Types
| Type | When to Use | Word Count Target |
|------|-----|----------|
| `Landingpage` | Sale campaigns, newsletter launches, urgency-focused sales | 900-1,200 words |
| `Blogpost` | Organic SEO articles, storytelling content | 1500+ words |
| `Productnew` | New physical/digital products (tech specs focus) | 400-600 words + specs |
| `Productused` | Refurbished/second-hand items (condition reports) | 500-700 words + condition |
| `FAQ Page` | Organic SEO FAQ pages require 5+ Q&A pairs for Google's Featured Snippet eligibility! | 5 to 10 Questions and answers, total of 800-1200 words |
| `Socialphoto` | Visual posts + alt text optimization | 100-200 words |
| `Socialvideo` | YouTube/TikTok metadata + transcripts | 150-300 words |

### How It Works
1. Your prompt includes product details, keywords, personas, briefs
2. System selects appropriate template from `TEMPLATES/` folder
3. Applies persona style (vocabulary, tone) to content
4. Injects SEO variables (meta tags, schema, canonical URL)
5. Generates clean HTML ready for copy-paste deployment

**Example Usage**:
```text
persona E-Commerce Manager /write Landingpage "20% off premium electronics sale starting May 1st" --primary-kw summer-sale-electronics
persona Creative Writer /write Blogpost "Why Choose Sustainable Hiking Gear?" --primary-kw eco-friendly-hiking-gear
persona Researcher /write Productnew "EcoSmart Water Bottle with Lifetime Warranty" --primary-kw sustainable-water-bottle
```

---

## Step 5: Quality Checks — Validate Before Deployment
**Command**: `checks <url>` or `/checks <type>` (preview mode)

### Check Categories by Page Type

The full rule set per page type — required elements, recommended elements, keyword placement,
do's/don'ts — lives in `SEO_RULES/<type>.md` (`SEO_RULES/landingpage.md`,
`SEO_RULES/blogpost.md`, `SEO_RULES/productnew.md`, `SEO_RULES/productused.md`,
`SEO_RULES/faq.md`, `SEO_RULES/socialphoto.md`, `SEO_RULES/socialvideo.md`). `checks` audits the
generated page against those files via `SEO_CHECKS/page-type-specific-checks.md`.

### Check Example Output
```text
checks https://example.com/summer-sale-2026

SEOwlsClaw — SEO Checks Report (v0.1)
Date: 2026-03-20 | Type: Landingpage

✅ Title tag length (passed)
✅ Meta description length (passed)
✅ H1 tag exists + unique (passed)
✅ Schema.org Event/Offer JSON-LD (passed)
✅ Alt text on images (passed)
❌ Keyword density > 2% (failed — recommendation: Reduce repetition)

Issues Found: 1 | Pass Rate: 95%
```

---

## Full Workflow Example — Generate a Sale Landing Page End-to-End

### Start Here: Run This Sequence in Order

```text
# Step 1: Research the keyword cluster
persona Researcher /research 20% electronics sale Berlin May 2026

# Step 2: Set persona for conversion-focused writing
persona E-Commerce Manager --tone enthusiastic

# Step 3: Generate content with template
persona E-Commerce Manager /write Landingpage "We're offering massive discounts on our top X Y Z products starting May 1st where we give limited-time deals to early birds" --primary-kw summer-sale-electronics --secondary-kw limited-offer

# Step 4: Check quality before deployment
checks https://example.com/summer-sale-2026

# Step 5: Generate output HTML (system creates it in OUTPUT_EXAMPLES/)
```

### What Gets Created Automatically
- Clean text output in user chat ready for copy-paste into CMS/WordPress/custom host
- Schema.org JSON-LD markup included
- Internal linking section with H6 links
- SEO variables injected (canonical URL, meta tags)
- Quality check report (pass/fail list)

---

## Variable Injection System — How SEOwlsClaw Works Behind the Scenes

```json
{
  "siteStructure": {
    "url": "https://example.com",
    "canonicalUrl": "https://example.com/summer-sale-2026"
  },
  "metadata": {
    "titleLength": 60,
    "metaDescriptionLength": 160,
    "robots": "index,follow"
  },
  "keywords": {
    "primaryKw": "summer-sale-electronics",
    "secondaryKw": ["limited-offer", "flash-sale"],
    "longTailKw": [
      "20% electronics sale Berlin May 2026",
      "best discount electronics summer 2026"
    ]
  },
  "headersByPageType": {
    "landingpage": {
      "H1": "Exclusive Summer Sale: Save Up to 40% on Premium Electronics",
      "H2": "Why This Sale Is Your Best Chance to Save Big"
    }
  },
  "optimization": {
    "wordCountTarget": 1000,
    "imageRatio": 1.5,
    "loadSpeedGoal": "<3s"
  },
  "schemaTypes": ["Event", "Offer"]
}
```

---

*Last updated: 24-08-2026 (v0.9.2)*
*Adds: Step 5 points at SEO_RULES/<type>.md; Supported Page Types word counts reconciled with SEO_RULES/*
*Maintainer: Chris — complete SEO workflow from research to deployment*  
*Ready for testing with write command → See OUTPUT_EXAMPLES/ folder for reference outputs!*
