# Keyword optimization methodology

## Contents
1. Search intent taxonomy
2. Five evaluation dimensions
3. Long-tail theory
4. Pillar–cluster content architecture
5. Keyword cannibalization
6. Zero-click search and SERP features
7. Keyword signals in the AI era (GEO/AEO)

---

## 1. Search intent taxonomy

**Sources**: Google *Search Quality Evaluator Guidelines* (2023); Andrei Broder, “A Taxonomy of Web Search” (*ACM SIGIR Forum*, 2002).

Broder’s original three-way split (Informational / Navigational / Transactional) was extended by Google’s guidelines to four classes used in quality evaluation and algorithm training.

| Type | Code | User goal | Typical patterns | Content format |
|-----|-----|---------|---------|---------|
| Informational | I | Learn or answer a question | how to, what is, why, guide, tips, explained | Blog, FAQ, tutorial |
| Navigational | N | Reach a specific site or brand | brand name, “official site”, login | Homepage, brand hub |
| Commercial investigation | C | Compare options before deciding | best, vs, compare, review, top, worth it | Comparisons, reviews, roundups |
| Transactional | T | Complete a purchase or conversion | buy, hire, book, price, near me, contact | Service, product, landing pages |

**Practical notes**:
- The most reliable intent check is **inspect the SERP**: Google the term and look at positions 1–5; dominant content types reflect the intent Google rewards.
- The same term can imply different intent by market/language—judge each locale separately.
- Commercial-investigation terms (including best/compare) see roughly **+156%** higher AI citation rates vs generic terms (Semrush GEO Report 2024).

---

## 2. Five evaluation dimensions

**Sources**: Rand Fishkin (Moz founder), *The Art of SEO*, 3rd ed. (O’Reilly, 2015); Ahrefs methodology docs.

### 2.1 Search volume

Average monthly searches. Caveats:
- **Volume ≠ traffic**: position 1 CTR ≈ 27.6% (Sistrix, 2020); zero-click searches ≈ 58.5% (SparkToro, 2019).
- Long-tail terms are lower volume but often higher intent—do not chase only high-volume head terms.
- Tools are approximate (GKP ranges; Ahrefs/Semrush modeled volumes)—use for direction, not false precision.

### 2.2 Keyword difficulty (KD)

0–100 score blending how much topical/off-site authority is needed. Algorithms differ—the same term can diverge a lot between Ahrefs and Semrush.

**Practical bands** (new/small sites):
- KD 0–20: quickest wins—prioritize.
- KD 21–40: needs strong content + some links—medium term.
- KD 41–60: needs authoritative site—long term.
- KD > 60: defer for new sites; build authority first.

### 2.3 Intent–business fit

How well the query intent matches your business and the target URL. Highest-weight dimension—even with high volume and low KD, wrong intent drives bouncy, low-value traffic.

### 2.4 Conversion potential

From intent plus commercial cues:
- Strong purchase/hire signals (hire/buy/price/contact) > comparison signals (best/vs) > informational (how/what).

### 2.5 SERP feature opportunity

Check whether the SERP offers:
- **Featured snippet**: gap or weak structure → opportunity.
- **People Also Ask (PAA)**: question-led terms → FAQ opportunity.
- **Local pack**: local-service terms → Google Business Profile opportunity.
- **Image / video packs**: visual content opportunity.

---

## 3. Long-tail theory

**Sources**: Chris Anderson, “The Long Tail” (*Wired*, 2004); Ahrefs, “How Many Keywords Does a Webpage Rank For?” (2017).

- ~91.8% of queries have fewer than 10 searches/month (long tail; Ahrefs, 2019).
- In aggregate, long-tail demand exceeds head terms.
- Traits: lower competition, clearer intent, often higher conversion (HubSpot: ~2.5× vs head terms).

**How to spot long-tail**:
- Phrases of 3+ words are often long-tail.
- Geo modifiers (“in Singapore”), time (“2026”), qualifiers (“for elderly”).
- Question forms (“how to…”, “what is…”).

---

## 4. Pillar–cluster content architecture

**Sources**: HubSpot, “The Pillar Strategy” (2017); Semrush topic-cluster research.

Move from keyword stuffing to topical authority:

```
Pillar page
├── Broad overview of one theme
├── Targets higher-volume umbrella terms
└── Cluster pages (spokes)
    ├── Each page goes deep on one subtopic
    ├── Targets mid/low-volume specific long-tails
    └── Bidirectional internal links to/from the pillar
```

**Why it works**:
- Builds topic authority—algorithms favor sites that comprehensively cover a subject.
- Internal links pass PageRank; the pillar accumulates strength.
- Reduces cannibalization (one primary URL per subtopic).

**Practice**: Pick 3–5 pillar themes, then plan 5–10 cluster articles/pages per pillar.

---

## 5. Keyword cannibalization

**Sources**: Semrush blog; early Bruce Clay work.

When multiple URLs on the same site compete for one keyword, Google struggles to pick a canonical winner—often both URLs underperform.

**Detection**:
- Search `site:yourwebsite.com [keyword]`; multiple distinct URLs → risk.
- In GSC, filter a query and see if multiple URLs earn impressions for it.

**Fixes**:
- Merge overlapping content (301 redirects to the winner).
- Assign one primary URL per keyword and reinforce with internal links.

---

## 6. Zero-click search and SERP features

**Sources**: SparkToro zero-click studies (Rand Fishkin, 2019, 2022); Sistrix CTR research.

- ~58.5% of Google searches in 2022 ended without an organic click (SparkToro).
- Position 1 organic CTR ≈ 27.6% (Sistrix, 2020).

**Implications**:
- Target featured snippets and PAA—even with zero clicks you gain visibility.
- Measure SEO with impressions and branded search growth, not clicks alone.
- AI Overviews (Google AIO) compress organic clicks further; structuring content for AIO citation is increasingly important.

---

## 7. Keyword signals in the AI era (GEO/AEO)

**Sources**: BrightEdge 2024 AI Search Report; Semrush GEO Report 2024; Ahrefs GEO research 2024.

What AI search (ChatGPT, Perplexity, Google AIO) tends to cite:

| Content type | Lift in AI citation |
|---------|--------------|
| Original data / research reports | +340% |
| Commercial investigation terms (best/compare) | +156% |
| Step-by-step guides | +89% |
| FAQ / direct Q&A format | +40% |
| Concrete stats (numbers, percentages) | +37% |

**Takeaway**: Keyword strategy affects both classic rankings and AI citation odds—favor terms that let you produce the content types above.
