# Keyword Research Methodology

A systematic approach to finding keywords that actually drive signups for SaaS products. Not just traffic — revenue-relevant traffic.

---

## The SaaS keyword hierarchy

Not all keywords are equal for SaaS. Prioritize in this order:

### Tier 1: Bottom-of-funnel (highest intent)
- `{product} vs {competitor}` — people actively comparing
- `best {category} tool/software` — ready to buy
- `{competitor} alternative` — dissatisfied with current solution
- `{competitor} review` — evaluating options
- `{product} pricing` — already interested

### Tier 2: Middle-of-funnel (problem-aware)
- `how to {solve problem your product solves}` — knows the problem
- `{use case} tool/software` — looking for solutions
- `{industry} {function} automation` — exploring efficiency gains

### Tier 3: Top-of-funnel (awareness)
- `what is {concept}` — educational
- `{industry} guide/tutorial` — learning
- `{broad topic} examples` — research phase

**For SaaS, Tier 1 and 2 content converts. Tier 3 builds authority but don't prioritize it over conversion content.**

---

## Research process

### Step 1: Seed keywords

Start with:
1. The product's core feature (e.g., "ai store builder", "email automation")
2. The problem it solves (e.g., "build shopify store fast", "automate email sequences")
3. Direct competitors (e.g., "mailchimp", "pagepilot")
4. The category (e.g., "dropshipping tools", "crm software")

### Step 2: Expand with tools

**Using SemRush:**
```
Domain Overview → {competitor domain} → Organic Research → Top Keywords
Keyword Gap → {your domain} vs {competitor 1} vs {competitor 2}
Keyword Magic Tool → {seed keyword} → filter by KD < 30
```

**Using DataForSEO:**
```python
# Get keyword ideas from seed
keywords_for_keywords(["seed keyword 1", "seed keyword 2"], location_name="United States")

# Find what competitors rank for
labs_ranked_keywords("competitor.com", location_name="United States", limit=100)

# Gap analysis
labs_domain_intersection(["your-domain.com", "competitor.com"], location_name="United States")
```

**Using Google Search Console:**
- Performance → Queries → sort by impressions
- Look for queries where you appear but don't rank well (pos > 10)
- These are your "almost there" keywords

### Step 3: Evaluate and prioritize

For each keyword, score on:

| Factor | Weight | How to assess |
|--------|--------|--------------|
| Search volume | 20% | SemRush/DataForSEO data |
| Keyword difficulty | 25% | KD score — prefer < 30 for new sites |
| Commercial intent | 30% | Does this person want to buy software? |
| Cluster fit | 15% | Does it belong to an existing cluster? |
| Quick win potential | 10% | Are you already ranking 10-30? Just need a push? |

**Priority formula (simplified):**
```
Priority score = (volume * intent_weight) / (KD + 1)
```

Intent weights:
- Tier 1 (buying): 3x
- Tier 2 (problem-solving): 2x
- Tier 3 (educational): 1x

### Step 4: Map to clusters

Every keyword must belong to a cluster. If it doesn't fit an existing cluster, either:
1. Create a new cluster (if 5+ related keywords with combined volume > 2000/month)
2. Drop it (orphan keywords aren't worth the effort)

### Step 5: Assign to content

Each keyword maps to one page. One page can target 1 primary + 2-3 secondary keywords.

```
Primary keyword → H1, title tag, first paragraph
Secondary keywords → H2s, body content
Long-tail variations → FAQ section, subheadings
```

---

## CTR analysis

High impressions + low CTR = the fastest ROI in SEO.

**Benchmark CTR by position:**
| Position | Expected CTR |
|----------|-------------|
| 1 | 25-35% |
| 2 | 12-18% |
| 3 | 8-12% |
| 4-5 | 5-8% |
| 6-10 | 2-5% |

If a page's CTR is significantly below these benchmarks, the title/meta description needs work. Common fixes:
- Add the current year (2026)
- Add a number ("7 Best...", "Top 5...")
- Add a power word ("Free", "Complete", "Honest")
- Match search intent better (informational vs commercial)
- Add your brand name for branded queries

---

## Competitor keyword intelligence

For each competitor, gather:
1. Their top 20 organic keywords (what drives their traffic)
2. Keywords where they rank #1-3 (their strong positions)
3. Keywords where they rank #4-10 (vulnerable — you can overtake)
4. Content types they publish (reviews? guides? comparisons?)
5. Their cluster structure (how is their blog organized?)

**The gap is your roadmap.** Keywords your competitors rank for that you don't = your content plan.
