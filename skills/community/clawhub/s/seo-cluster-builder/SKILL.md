---
name: seo-cluster-builder
description: >
  Build complete SEO topic clusters with full article content, schema markup,
  and internal linking. Use this skill whenever the user wants to create a
  content cluster, write SEO blog articles for a keyword group, build topical
  authority for a website, create pillar pages with supporting articles,
  generate WordPress-ready content with schema markup, research keyword
  competition before writing, or audit existing cluster structure.
  Triggers on phrases like: tao cluster, viet bai SEO, xay dung cluster,
  content cluster, pillar page, bai viet chuan SEO, build topic cluster,
  write cluster articles, loat bai SEO, chuan bi noi dung SEO.
  Always use this skill for multi-article SEO content creation tasks.
  Do not attempt to generate clusters without following this skill workflow.
---

# SEO Cluster Builder

Skill for building complete, production-ready SEO topic clusters. Each cluster includes: competition research, article content with natural internal links, schema markup per article, SEO meta tags, and a copy-paste–ready HTML output file.

This skill encodes the exact workflow used to build the "Pinata Sinh Nhật" and "Tổ Chức Tiệc Sinh Nhật" clusters for pinata.vn — two real-world clusters that demonstrate the full pattern.

---

## Workflow Overview

```
PHASE 1 — RESEARCH (always first)
  └── Fetch live site + competitor data
  └── Identify content gaps and keyword angles

PHASE 2 — CLUSTER DESIGN
  └── Choose pillar topic and angle
  └── Map 6–8 cluster articles with intent groups
  └── Design internal link graph

PHASE 3 — CONTENT GENERATION
  └── Write all articles with inline links
  └── Generate schema per article
  └── Write SEO meta tags

PHASE 4 — OUTPUT
  └── Produce single HTML file (copy-paste ready)
  └── Validate all schema JSON + internal links
  └── Generate summary table
```

Read `references/phase1-research.md` before starting Phase 1.
Read `references/phase2-design.md` before designing the cluster.
Read `references/phase3-content.md` before writing articles.
Read `references/phase4-output.md` before generating the final file.

---

## Critical Rules (apply to every cluster)

### R1 — Research before writing
ALWAYS fetch the client's site and top 3 competitor pages before writing a single word. Never design a cluster based on assumptions.

### R2 — Audit existing content first
Search `site:[domain]` for existing articles on the topic. Flag:
- Cannibalization risk (2+ articles targeting same keyword)
- Redirect opportunities (old thin articles → new pillar)
- Bridge opportunities (existing articles that can link INTO the new cluster)

### R3 — Angle selection
Never compete head-on against sites with DA 50+. Always find a specific angle the domain can win:
- Product-specific angle (e.g., "trò chơi tiệc sinh nhật" instead of "tổ chức tiệc sinh nhật")
- Long-tail angle (e.g., "tiệc sinh nhật chủ đề khủng long" instead of "trang trí sinh nhật")
- Local angle (e.g., city-specific landing pages)

### R4 — Internal links must be IN the article body
Every article must have ≥ 3 internal links placed naturally within the content — NOT only in a sidebar, footer, or link map note. Validate programmatically before output.

### R5 — Schema validation
All JSON-LD blocks must parse as valid JSON before inclusion. Run validation; never output unchecked schema.

### R6 — No duplicate content between clusters
When adding a new cluster to a site that already has clusters, check for topical overlap. Add bridge links between clusters; do not rewrite the same content twice.

---

## Cluster Architecture

### Standard structure (6–8 articles)
```
PILLAR (1 article)
│  Intent: Informational overview — answers "what is X" + summarizes all subtopics
│  Word count: 2,000–3,000 words
│  Internal links: OUT to every cluster article (minimum)
│
├── INFORMATIONAL CLUSTER (1–2 articles)
│   Intent: Deep-dive on background, history, "why"
│   Word count: 1,200–1,800 words
│
├── HOW-TO CLUSTER (1–2 articles)
│   Intent: Step-by-step guides
│   Schema: HowTo (required)
│   Word count: 1,500–2,000 words
│
├── COMMERCIAL CLUSTER (1–2 articles)
│   Intent: Price, where to buy, comparison
│   Schema: FAQPage + ItemList
│   Word count: 1,200–1,500 words
│   Note: These articles must link directly to product/service pages
│
└── THEME/LONG-TAIL CLUSTER (2–3 articles)
    Intent: Specific use cases, characters, locations
    Word count: 1,000–1,500 words each
    Note: Highest conversion — user has specific intent
```

### Internal link minimum requirements
| Article type | Min links OUT | Must link TO |
|---|---|---|
| Pillar | All cluster articles | Product/category page |
| Informational | 2 | Pillar + 1 other cluster |
| How-to | 3 | Pillar + commercial + 1 other |
| Commercial | 3 | Pillar + product page + 1 cluster |
| Theme/long-tail | 3 | Pillar + 2 related clusters |

---

## Schema Matrix

Each article type requires specific schema blocks:

| Article type | Article | FAQPage | HowTo | BreadcrumbList | ItemList |
|---|---|---|---|---|---|
| Pillar | ✅ required | ✅ ≥4 Q&A | — | ✅ required | — |
| Informational | ✅ | ✅ ≥3 Q&A | — | ✅ | — |
| How-to guide | ✅ | ✅ ≥3 Q&A | ✅ ≥4 steps | ✅ | — |
| List/Top-N | ✅ | ✅ ≥3 Q&A | — | ✅ | ✅ ≥5 items |
| Commercial/Price | ✅ | ✅ ≥3 Q&A | — | ✅ | ✅ optional |
| Theme/character | ✅ | ✅ ≥2 Q&A | — | ✅ | — |

See `references/phase3-content.md` for complete schema templates.

---

## Output File Format

The final deliverable is a single HTML file that:
1. Renders in browser — agent/user can preview each article
2. Has a **Copy button** for each section (meta tags, schema, article body)
3. Contains an audit box at the top flagging pre-existing issues
4. Contains an internal link map per article showing which URLs to link to
5. Contains a summary table at the bottom with publish order

File naming: `cluster-[topic-slug].html`
CSS: Use the shared stylesheet in `assets/cluster-style.css` (inline into `<style>` tag)

See `references/phase4-output.md` for the full HTML template and component library.

---

## Validation Checklist (run before finalising output)

```python
# Pseudo-code — implement with actual Python in bash_tool
for each article:
    assert schema_blocks >= minimum_for_type       # R5
    assert json_valid(all_schema_blocks)           # R5
    assert internal_links_in_body >= 3             # R4
    assert internal_links_not_only_in_ilmap        # R4
    assert pillar_links_to_all_clusters            # architecture
    assert no_city_name_leaks_from_other_cities    # for geo clusters
    assert breadcrumb_present                      # schema matrix
    assert faq_present                             # schema matrix
```

---

## Quick Reference: Cluster Examples

| Cluster | Domain | Angle | Articles | Status |
|---|---|---|---|---|
| "Pinata sinh nhật" | pinata.vn | Commercial — product-specific | 6 | ✅ Live reference |
| "Tổ chức tiệc sinh nhật" | pinata.vn | How-to + theme — avoid DA60+ head terms | 8 | ✅ Live reference |
| "Pinata là gì" | pinata.vn | Informational — topical authority | 6 | ✅ Live reference |

Full content of these reference clusters is in the session history. When in doubt about format or depth, refer to those examples.
