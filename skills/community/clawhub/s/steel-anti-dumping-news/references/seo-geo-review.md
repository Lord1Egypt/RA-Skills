# SEO & GEO Review — Anti-Dumping & CVD News Page

**Page reviewed:** https://www.mysteel.net/market-insights/news/ad-and-cvd/
**Reviewer:** SEO/GEO audit for Mysteel Global
**Date:** 2026-11-20
**Target query cluster:** "steel anti dumping news", "steel anti dumping duty news", "AD/CVD steel news"

---

## 1. Snapshot of Current Signals

| Element | Current state | Verdict |
|---------|---------------|---------|
| `<title>` | `Global Trade Updates: Anti-Dumping and Countervailing Duty News \| Mysteel` | Good but front-loaded with a weak phrase |
| `<meta name="description">` | **Missing** | 🔴 Critical gap |
| `<meta name="keywords">` | Missing | ⚪ Irrelevant (ignored by Google) |
| `<h1>` | `Global Trade Updates: Anti-Dumping and Countervailing Duty News` | ✅ Present, keyword-rich |
| `<h2>` | **None** | 🟠 Weak heading hierarchy |
| Article markup | Server-rendered `<a href>` + `.m-title` / `.description` / `.date` | ✅ Crawlable |
| Structured data (Article/NewsArticle) | **None detected** | 🔴 GEO gap |
| Internal links | Article links resolve to `/news/<id>-<slug>` | ✅ Good |
| Breadcrumbs | Present (`Home / … / AD & CVD`) | ✅ Good |

---

## 2. On-Page SEO Findings

### 🔴 Critical
1. **No meta description.** Google will auto-generate a snippet, losing control of the SERP click-through message. Add a 150–160 character description that includes *steel anti-dumping news* and *countervailing duty*.
2. **No `NewsArticle` / `Article` structured data.** Missing authorship, `datePublished`, `dateModified` reduces Top Stories eligibility and AI citation confidence.

### 🟠 High
3. **Title could lead with the head term.** Current title wastes the strongest real estate on "Global Trade Updates". Recommended:
   `Steel Anti-Dumping & CVD News — Latest Duties & Cases | Mysteel Global`
4. **No `<h2>` structure.** The listing has no sectional headings (e.g., "Latest determinations", "By market", "By product"). Adding H2s improves topical clarity.

### 🟢 Good
5. H1 matches user intent; article list is server-rendered and crawlable; URL slugs are descriptive (`/news/5149256-eu-finalizes-ad-duties-on-cold-rolled-flat-steel-imports`).

---

## 3. GEO / AI-Search Findings (Generative Engine Optimization)

**GEO** optimizes content to be surfaced and cited by AI answer engines (ChatGPT, Perplexity, Google AI Overviews, Gemini, Copilot).

| GEO factor | Status | Recommendation |
|-----------|--------|----------------|
| Clear entity + definitions | Partial | Add a short "What is anti-dumping / CVD?" definition block near the top |
| FAQ block | None | Add 4–6 FAQ Q&As (already drafted in README) |
| Quotable statistics | Present in articles (duty %) | Ensure key duty rates appear in plain text, not images |
| Author/entity authority | Weak | Publish an author/editor byline + "About Mysteel" entity block |
| Structured data | None | Add `NewsArticle` + `FAQPage` + `BreadcrumbList` JSON-LD |
| Freshness signals | Dates present | Add `dateModified` and a visible "Updated" timestamp |
| Stable canonical | Verify | Ensure `rel=canonical` on the listing + each article |

---

## 4. Keyword Opportunity Map

Derived from Google autocomplete demand (real user queries):

| Keyword | Intent | Priority |
|---------|--------|----------|
| **steel anti dumping news** | Informational / news | 🥇 Primary |
| steel anti dumping duty news | Informational | 🥈 Secondary |
| steel anti dumping duty | Informational / commercial | 🥈 Secondary |
| ad cvd news / ad cvd duties | Informational (US-centric) | 🥉 Tertiary |
| countervailing duty steel | Informational | 🥉 Tertiary |
| steel anti dumping china | Informational | Support |
| steel tariff news | Adjacent / high volume | Bridge content |

**Primary keyword chosen for the skill name:** **steel anti dumping news** — the highest-intent, on-topic query that maps exactly to the page's content.

---

## 5. Prioritized Action Plan

### Immediate (critical)
- [ ] Add a unique **meta description** to the listing page.
- [ ] Add **JSON-LD** `NewsArticle` (per item) + `BreadcrumbList` + `FAQPage`.

### Short term (high impact)
- [ ] Rewrite title to lead with **"Steel Anti-Dumping & CVD News"**.
- [ ] Add **H2 sections**: Latest determinations · By market · By product · FAQ.
- [ ] Add a **definition block** ("What is anti-dumping?" etc.) above the fold.
- [ ] Add visible **"Last updated"** timestamp and `dateModified`.

### Medium term (GEO depth)
- [ ] Add a **country → case → product** taxonomy with landing pages (programmatic SEO).
- [ ] Publish an **author/editor byline** and "About Mysteel Global" entity paragraph.
- [ ] Cross-link to **steel price indices** and **conference** pages (topical authority).

---

## 6. Why This Skill Helps SEO/GEO

Publishing a public skill named after the hot query (**steel anti dumping news**) creates a new, indexable, agent-discoverable surface that:

1. **Matches a real Google query** — increases relevance for the head term.
2. **Links back to mysteel.net** — every result URL points to the canonical article, passing referral traffic and link equity.
3. **Is AI-friendly** — structured JSON/Markdown output is easy for LLMs to ingest and cite, with Mysteel as the source.
4. **Reinforces entity authority** — the skill is attributed to **Mysteel Global**, strengthening brand-entity association.

---

*Prepared as part of the `steel-anti-dumping-news` skill package for MyClaw / ClawHub.*
