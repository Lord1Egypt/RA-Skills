# Phase 2 — Cluster Design

Run after Phase 1 research is complete.

---

## Step 2.1 — Define the Pillar Page

The pillar page is the hub. It must:
1. Target the broadest keyword in the cluster
2. Answer the "what is X + why + overview of all subtopics" question
3. Link OUT to every cluster article (at minimum)
4. Be linked to from every cluster article (at minimum)

**Pillar page URL pattern:**
```
/[primary-keyword-slug]/

Examples:
  /pinata-sinh-nhat/
  /tro-choi-tiec-sinh-nhat/
  /pinata-la-gi/
```

**Pillar page content structure:**
```
H1: [Primary keyword]: [Subtitle describing scope]
Intro: Answer the core question in first 100 words
H2: [Subtopic 1] → brief overview + link to cluster article 1
H2: [Subtopic 2] → brief overview + link to cluster article 2
...
H2: FAQ (5–6 questions covering all cluster topics)
CTA: Link to product/service page
```

---

## Step 2.2 — Design Cluster Articles

For each article (6–8 total), define:

| Field | Value |
|---|---|
| Title | Keyword-rich, ≤60 chars for title tag |
| URL slug | `/[keyword-slug]/` — no prefix for WordPress |
| Primary keyword | The exact search query to rank for |
| Secondary keywords | 2–3 variations to use naturally in body |
| Intent type | informational / how-to / commercial / theme |
| Schema required | Article + which others (see schema matrix in SKILL.md) |
| Priority | P1 (publish week 1) / P2 (week 2) |
| Notes | Merge from existing? Redirect? New? |

**Priority rules:**
- P1 = Pillar + Commercial articles (bottom-funnel, fastest conversion)
- P2 = Everything else (topical depth)

---

## Step 2.3 — Design Internal Link Graph

Map every link before writing. This prevents missing links and ensures bidirectional flow.

**Template:**
```
PILLAR /[pillar-slug]/
  → /[article-1]/  (anchor: "[descriptive text]")
  → /[article-2]/  (anchor: "[descriptive text]")
  → /[article-3]/  (anchor: "[descriptive text]")
  → /[product-page]/  (anchor: CTA text)

/[article-1]/
  → /[pillar-slug]/  (back to pillar)
  → /[article-3]/   (related cluster)
  → /[product-page]/  (CTA)

/[article-2]/
  → /[pillar-slug]/  (back to pillar)
  → /[article-4]/   (commercial — link here when content naturally fits)
  ...
```

**Rules:**
- Every cluster article must link back to pillar (1 link minimum)
- Pillar must link to every cluster article (1 link minimum each)
- Commercial articles must link to product/category pages
- Cross-links between clusters: link from current cluster → previous cluster's pillar or commercial article (1–2 bridge links per cluster)

---

## Step 2.4 — Breadcrumb Structure

Every article needs a BreadcrumbList. Design the structure:

```
Informational pillar:
  Home → [Pillar Title]

Single-level cluster:
  Home → [Pillar] → [Article Title]

For geo clusters:
  Home → [Category] → [City Article]
```

---

## Step 2.5 — Cluster Design Checklist

```
☐ Pillar defined with URL, keyword, content structure
☐ 5–7 cluster articles defined (title, URL, keyword, type)
☐ Internal link graph mapped (ALL directions)
☐ Priority P1/P2 assigned to each article
☐ Existing articles flagged for redirect → new pillar URL
☐ Bridge links to previous clusters noted
☐ Breadcrumb paths defined per article
```

**Output of Phase 2:**
→ Full cluster table (title, URL, keyword, type, priority, schema)
→ Internal link graph
→ Publish order (P1 first, always Pillar before cluster articles)
