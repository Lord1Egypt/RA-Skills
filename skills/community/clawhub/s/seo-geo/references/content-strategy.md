# Content Strategy for SaaS

How to structure your blog content so every article strengthens the whole. Random articles don't rank — clusters do.

---

## The cluster model

Every SaaS blog should be organized into **content clusters**. A cluster is:

```
Pillar page (broad topic, high volume)
├── Sub-page 1 (specific angle, lower KD)
├── Sub-page 2 (comparison, commercial intent)
├── Sub-page 3 (guide, informational)
└── Sub-page 4 (review, bottom-of-funnel)
```

All pages in a cluster interlink. The pillar links down to sub-pages. Sub-pages link up to the pillar and across to each other. This builds topical authority — Google sees you as an expert on this topic.

**For a typical SaaS, start with 3 clusters.** Expand once you've filled the first three.

---

## Cluster types for SaaS

### 1. Product cluster
Your core product category. Every SaaS has this.

```
Pillar: "Best {category} tools in 2026"
├── {competitor-1} vs {your product}
├── {competitor-2} review
├── Best {competitor-3} alternatives
├── {product category} comparison
├── How to choose a {product category}
└── {your product} features guide
```

### 2. Use case cluster
The problem your product solves.

```
Pillar: "How to {solve problem}"
├── {Problem} for beginners
├── {Problem} tutorial step by step
├── {Problem} tools and software
├── {Problem} examples
├── Free {problem} solution
└── {Problem} vs {alternative approach}
```

### 3. Industry/niche cluster
The world your customers live in.

```
Pillar: "{Industry} guide 2026"
├── {Industry} trends
├── {Industry} tools
├── {Industry} examples
├── How to start {industry activity}
└── {Industry} resources
```

### 4. Competitor cluster (high ROI for SaaS)
Every major competitor gets their own mini-cluster.

```
{Competitor} review
{Competitor} alternatives
{Competitor} vs {your product}
{Competitor} pricing
```

This is often the highest-converting content for SaaS. People searching for competitor names are actively evaluating solutions.

---

## Building a cluster from scratch

### Step 1: Pick the cluster topic
Based on keyword research, choose a topic where:
- Combined search volume > 3,000/month
- Average KD < 30 (for new sites) or < 50 (for established sites)
- Clear commercial intent for at least some keywords
- You have genuine expertise or product fit

### Step 2: Map all keywords to pages
One page per primary keyword. Group related keywords together.

### Step 3: Create the pillar page first
The pillar is the broadest page in the cluster. It:
- Targets the highest-volume keyword
- Links to every sub-page
- Gets updated as sub-pages are published
- Is the "homepage" of the cluster

### Step 4: Publish sub-pages in priority order
1. Competitor comparisons (highest intent, easiest to template)
2. "Best X" / "Top X" listicles (good internal linking opportunities)
3. Guides and tutorials (builds authority)
4. Long-tail / FAQ content (fills gaps)

### Step 5: Internal linking pass
After publishing 3+ sub-pages:
- Pillar links to all sub-pages
- Each sub-page links to the pillar
- Sub-pages link to 2-3 related sub-pages
- Add relevant links from older content outside the cluster

---

## Content gap analysis

A content gap is a keyword that:
1. Your competitors rank for AND you don't, OR
2. You rank for poorly (pos 10+) AND the keyword has decent volume

**How to find gaps:**

**SemRush:** Keyword Gap tool → your domain vs 3 competitors → filter "Missing" and "Weak"

**DataForSEO:**
```python
labs_domain_intersection(
    ["your-domain.com", "competitor1.com", "competitor2.com"],
    location_name="United States",
    limit=200
)
```

**GSC:** Performance → filter position > 10 → sort by impressions descending. These are keywords Google already associates with your site but you're not ranking well for.

**Prioritize gaps by:**
1. Commercial intent (will this drive signups?)
2. Volume / KD ratio (easy wins first)
3. Cluster fit (does it strengthen an existing cluster?)

---

## When to create a new cluster

Add a new cluster when:
- You've published 70%+ of planned content in existing clusters
- You've identified 5+ keywords in a new topic with combined volume > 2,000/month
- The topic has clear product tie-in (you can naturally mention your SaaS)
- Average KD is manageable for your site's authority

Don't spread too thin. Three strong clusters beat six weak ones.

---

## Product screenshots as content assets

Every SaaS article should include real product screenshots — not stock images. They build trust, are unique content (better for SEO), and show prospects what they're getting.

**Setup:** During onboarding, the user creates `seo/screenshots/` and drops 10-20 screenshots of their app. These are reused across articles.

**What to screenshot:**
- Dashboard/main UI (most used)
- Key features in action
- Onboarding flow
- Pricing page
- Before/after results (if applicable)
- Integration screens (Shopify, Stripe, etc.)

**How to use in articles:**
- Competitor reviews: show your product as the alternative ("Here's what {Your Product} looks like instead")
- Guides: illustrate steps with real UI screenshots
- Comparison articles: side-by-side your product vs competitor
- Pillar pages: feature overview screenshots

**Image rules:**
- WebP format, under 200KB each
- Descriptive filenames: `dashboard-overview.webp`, not `IMG_001.png`
- Alt text includes the target keyword naturally
- 2-4 product screenshots per article minimum

When writing any article, ALWAYS check `seo/screenshots/` for relevant images before suggesting generic alternatives.

---

## Content refresh strategy

Existing content decays. Schedule refreshes when:
- A page drops 3+ positions over 30 days
- CTR drops below position-expected benchmark
- Content is >6 months old and references outdated info
- A new competitor enters the market (update comparison pages)
- Your product ships new features (update feature-related content)

**Refresh checklist:**
1. Update title tag with current year
2. Refresh statistics and data points
3. Add new competitors or alternatives
4. Improve internal links (link to new content)
5. Add FAQ section if missing
6. Check and fix broken external links
7. Re-submit to GSC for re-indexing
