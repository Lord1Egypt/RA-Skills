---
name: "SEO & GEO (Generative Engine Optimization) Playbook"
version: 1.0.2
description: |
  Rank on Google AND get cited by ChatGPT, Perplexity, and Claude. A dual SEO + GEO strategy built from 30+ Product Hunt #1 launches and 10k+ GitHub stars campaigns — so your product shows up whether users search or ask AI.

  This playbook covers: GEO fundamentals including IndexNow instant push and Schema markup (FAQPage, Article, Organization), the E-E-A-T writing voice system with founder authenticity signals, SEO article templates using the QAE pattern (Question → Answer → Evidence), keyword funnel strategy (TOFU/MOFU/BOFU), content marketing for startups and developers, AI SEO tactics for Perplexity and ChatGPT search, perplexity SEO optimization, seo article template creation, seo writing best practices, seo checklist and seo audit workflows, seo tools for developers, seo for startups, and multi-platform distribution via Dev.to and Hashnode with canonical URLs.

  Unique content: The "founder voice" writing system that injects authenticity signals into AI-generated content — the key to being cited by AI engines like Perplexity and ChatGPT. Includes actionable seo checklist, seo article template prompts, seo writing prompts, schema markup generators, GEO audit checklist, and real case studies from GitHub stars growth and Product Hunt launches.

  Keywords: seo, geo, generative engine optimization, ai seo, perplexity seo, chatgpt seo, perplexity seo guide, e-e-a-t, indexnow, schema markup, seo article template, seo writing, content marketing, content marketing for startups, search engine optimization, seo strategy, seo checklist, seo audit, seo tools, seo tools for developers, seo for startups, seo for developers, perplexity optimization, bing copilot seo, chatgpt search optimization, seo playbook, seo guide, seo tutorial
---

# SEO & GEO Playbook

> Built from 30+ Product Hunt #1 launches and 10k+ GitHub stars campaigns
> by Iris (@gingiris) — AFFiNE former COO, 2022-2026

---

## TL;DR

- **GEO ≠ SEO** — AI engines cite differently than Google ranks
- **Structure beats keywords** — tables, FAQ, direct answers get cited
- **Founder voice > AI voice** — authenticity signals are the #1 GEO factor
- **IndexNow** — push URLs to Bing instantly, Bing trains AI on fresh content
- **Build TOFU→BOFU content funnels** — high-intent pages convert 10x better

---

## 📊 GEO vs SEO: Two Games, One Content

| Dimension | SEO (Traditional) | GEO (AI Search) |
|-----------|------------------|-----------------|
| **Goal** | Rank on Google/Bing | Be cited in AI answers |
| **Core Signal** | Backlinks + keywords | Structure + E-E-A-T |
| **Content Format** | H2/H3 + long-tail | Direct answers + tables + FAQ |
| **Technical** | Sitemap + Core Web Vitals | IndexNow + Schema + robots.txt |
| **Measurement** | GA4 traffic + ranking | Manual AI citation check |
| **Speed** | Weeks to months | Hours with IndexNow |

**Key insight**: Structure your content for BOTH. Schema markup and tables serve both games simultaneously.

---

## 🎯 The GEO Core Three (Your Technical Stack)

### 1. IndexNow — Real-Time Bing Push

Bing uses IndexNow to train AI models on fresh content. Every new article → push immediately.

```bash
# Push new URL to Bing (and Bing shares with AI engines)
curl "https://www.bing.com/indexnow?url=YOUR_URL&key=YOUR_KEY"

# Batch push (multiple URLs)
curl -X POST "https://www.bing.com/indexnow" \
  -H "Content-Type: application/json" \
  -d '{"host":"your-site.com","key":"YOUR_KEY","urlList":["url1","url2"]}'
```

**Setup**: Get your key from Bing Webmaster Tools → IndexNow → Generate Key

**When to push**:
- New article published
- Significant content update
- Product launch / major announcement

### 2. Schema Markup — Structured Data

```html
<!-- Article Schema -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Your Article Title",
  "author": {"@type": "Person", "name": "Your Name"},
  "datePublished": "2026-04-09",
  "dateModified": "2026-04-09",
  "publisher": {"@type": "Organization", "name": "Your Brand"}
}
</script>

<!-- FAQPage Schema (HIGH citation rate) -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What is GEO?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "GEO (Generative Engine Optimization) is the practice..."
      }
    }
  ]
}
</script>
```

**Schema priority for citation**:
1. FAQPage (highest — AI loves Q&A format)
2. Article/BlogPosting
3. SoftwareApplication (for tools/products)
4. Organization + Person (brand authority)

### 3. AI-Friendly Content Format

AI engines extract "citation-ready" content blocks. Structure your articles for extraction:

**The QAE Pattern** (Question → Answer → Evidence):
```markdown
## How to launch on Product Hunt?

**[Direct answer in 1-2 sentences]**
The best time to launch is Tuesday–Thursday, 9 AM GMT. The key is having 50+ upvotes in the first 2 hours.

**[Then evidence/data]**
Based on analyzing 30 Product Hunt launches:
- Tuesday launches: avg 280 upvotes
- Thursday launches: avg 260 upvotes
- Weekend launches: avg 80 upvotes

**[Then action]**
Prepare your hunter outreach list 2 weeks before launch...
```

**Table format increases citation ~35%**:
```markdown
| Platform | Traffic Share | Citation Rate |
|----------|--------------|---------------|
| YouTube | High | +25% cited by AI |
| GitHub | Very High | Highest AI citation |
| Reddit | Medium-High | AI summarizable |
```

---

## ✍️ The Founder Voice System (E-E-A-T Secret)

AI engines prioritize content with **authenticity signals**. Generic AI content gets penalized. The fix: inject "founder voice."

### Voice Elements That Signal Realness

1. **Time + Place Anchoring** — "It was 2 AM on a Thursday in August 2022..."
   - Instead of: "In my experience..."
2. **Parenthetical Aside** — "(I made this mistake once. Not twice.)"
   - Shows personal accountability
3. **Em-dash Contrast** — "Reddit gave us volume — HN gave us trust."
   - Creates rhythm and depth
4. **Specific Numbers** — "28 appearances on GitHub Trending"
   - Instead of: "appeared many times"
5. **Mistakes + Lessons** — "We tried X. It failed. Here's why."
   - Shows lived experience

### Key Stats Table (Every Article)

Every article should have this near the top:

```markdown
| Metric | Value |
|--------|-------|
| Results achieved | [Specific number] |
| Timeframe | [Specific period] |
| Cost | [$X or "free"] |
| Team size | [N people] |
| Win rate | [% or ratio] |
```

AI engines love extracting and citing these.

### The Pattern: Specific → General

```
WRONG: "Many startups struggle with launch strategy."

RIGHT: "When AFFiNE launched on Product Hunt in August 2022, 
we got 180 upvotes on day one. Most startups get 20-40. 
The difference wasn't luck — it was a specific sequence of 
actions that we refined across 30 subsequent launches."
```

---

## 📝 SEO Article Template

### Frontmatter
```yaml
---
title: "[Target Keyword]: [Specific Benefit] in 2026"
description: "[100-160 chars, include keyword + CTA]"
date: YYYY-MM-DD
tags: [tag1, tag2]
canonical: https://original-url.com
---
```

### Article Structure

```markdown
<!-- TL;DR block — AI engines love these -->
## TL;DR
- Key point 1
- Key point 2
- Key point 3

<!-- Key Stats table — place early -->
| Metric | Value |
|--------|-------|

## [H2: Question/Problem Form]

[Direct answer — 2 sentences max]
[Evidence/data/case study]
[Action step]

## [H2: Next Topic]

... (repeat pattern)

## Key Takeaways
1. 
2. 
3.

## Related Tools / Resources
- [Tool 1](link) — 1-sentence description
- [Tool 2](link) — 1-sentence description
```

### SEO Title Formulas

| Type | Formula | Example |
|------|---------|---------|
| How-to | "How to [Task] in 2026: [N] [Methods]" | "How to launch on Product Hunt in 2026: 5 Proven Strategies" |
| Comparison | "[Product A] vs [Product B]: Which is Better in 2026?" | "Notion vs AFFiNE: Which is Better in 2026?" |
| List | "[N] [Category] Tools for [Use Case] in 2026" | "15 Open Source Alternatives to Notion in 2026" |
| Problem | "How to Solve [Problem]: [Solution] Guide" | "How to Solve Content Marketing: The 2026 Playbook" |

---

## 🔍 Keyword Funnel Strategy

### TOFU (Awareness) → MOFU (Consideration) → BOFU (Decision)

```
TOFU: "how to improve team collaboration"
  → Blog posts, guides, educational content
  → Low intent, high volume

MOFU: "best collaboration software 2026"  
  → Comparison articles, list posts, category pages
  → Medium intent

BOFU: "[Product] pricing / reviews / vs [competitor]"
  → Product pages, pricing, reviews
  → High intent, lowest volume, highest conversion
```

**Priority: Build BOFU pages first.**

Even with 10 monthly searches, a BOFU page converts 10x better than TOFU.

### Keyword Research Framework

1. **Seed keywords** — your product category, use case
2. **Expand with** — competitor names, tool alternatives, "[product] vs"
3. **Long-tail gems** — KD 30-50, specific use cases, "for [audience]"
4. **Filter** — must have commercial or informational intent (not navigate)

---

## 🚀 Multi-Platform Distribution SOP

### Step 1: Publish to Main Site
- Jekyll/GitHub Pages, Hugo, or any static site
- Include Article Schema + FAQ Schema
- Verify: `https://search.google.com/test/rich-results`

### Step 2: IndexNow Push (immediately)
```bash
curl "https://www.bing.com/indexnow?url=NEW_URL&key=YOUR_KEY"
```

### Step 3: Dev.to Cross-Post
```bash
curl -X POST "https://dev.to/api/articles" \
  -H "api-key: $DEVTO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "article": {
      "title": "...",
      "body_markdown": "...",
      "canonical_url": "https://your-site.com/post-slug",
      "tags": ["tag1", "tag2"],
      "published": true
    }
  }'
```
**Critical**: Set `canonical_url` to your main site — this passes SEO value to your domain.

### Step 4: Hashnode (optional, for tech audience)
- Same canonical_url strategy

### Step 5: GitHub README Update (for tools)
- Add article link to README "Related Content" section
- This creates a backlink + signals active maintenance

---

## ✅ GEO Audit Checklist

Before publishing any page, verify:

### Technical
- [ ] robots.txt allows AI crawlers:
  ```
  User-agent: GPTBot
  User-agent: ChatGPT-User
  User-agent: OAI-SearchBot
  Allow: /
  ```
- [ ] IndexNow key registered and tested
- [ ] sitemap.xml includes this page
- [ ] Canonical URL set correctly

### Content
- [ ] FAQPage Schema added (5+ questions)
- [ ] Article Schema added (author, date, publisher)
- [ ] Key Stats table in first 100 words
- [ ] H2 headings are questions or benefit statements
- [ ] Each H2 section starts with 2-sentence direct answer
- [ ] Internal links to 2+ related pages
- [ ] External links to 2+ high-authority sources

### Distribution
- [ ] IndexNow push executed
- [ ] Dev.to cross-posted with canonical_url
- [ ] GitHub README updated (if tool/product)

---

## 📚 Prompt Templates

### Prompt: GEO Article Writer

```
You are a SEO + GEO content writer for [brand]. 

Write an article targeting: "[target keyword]"

Requirements:
1. Opening: Time + place anchor, then Key Stats table
2. Structure: H2 = questions, first 2 sentences = direct answers
3. Include FAQPage Schema (5+ questions)
4. Include Article Schema
5. Founder voice: parenthetical asides, specific numbers, lessons from mistakes
6. Internal links to [related pages]
7. External links to 2 high-authority sources
8. Key Takeaways section at end

Output: Full markdown article ready to publish.
```

### Prompt: GEO Audit

```
Audit [URL] for GEO optimization. Check:
1. robots.txt — AI bots allowed?
2. FAQPage Schema — present + valid?
3. Article Schema — present + complete?
4. Opening 100 words — Key Stats table present?
5. H2 structure — questions, direct answers first?
6. Table count — at least 1 comparison table?
7. Internal/external links — balanced?
8. Canonical URL — set correctly?

For each issue: severity (high/medium/low) + fix recommendation.
```

### Prompt: Keyword Research

```
Research keywords for [product/category]:
- Find 10 MOFU keywords (KD 30-50, monthly volume 100-500)
- Find 5 BOFU keywords (product comparisons, pricing, "[product] vs")
- For each: search volume, KD, intent type, content angle

Prioritize keywords where [product] has clear differentiation.
```

---

## 📊 Real Results

This methodology produced:
- **30+ Product Hunt daily #1** launches
- **10k+ GitHub stars** for open source projects (0 → 33k in 18 months)
- **GitHub Trending** 28+ appearances
- **Top 3 rankings** on Google for competitive terms like "github marketing playbook"

---

## 🔗 Resources

**Free Playbooks (GitHub):**
- gingiris-launch: https://github.com/Gingiris/gingiris-launch
- gingiris-opensource: https://github.com/Gingiris/gingiris-opensource
- gingiris-b2b-growth: https://github.com/Gingiris/gingiris-b2b-growth

**Growth Tools:**
- https://gingiris.github.io/growth-tools/

**Author**: Iris (@gingiris) — AFFiNE former COO, open source growth consultant
