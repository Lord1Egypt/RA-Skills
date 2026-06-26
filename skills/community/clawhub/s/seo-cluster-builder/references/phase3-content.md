# Phase 3 — Content Writing

Run after Phase 2 design is complete. Write all articles before moving to Phase 4.

---

## Step 3.1 — Article Content Rules

### Language and tone
- Write in the same language as the client's site (Vietnamese if pinata.vn)
- Match brand voice: helpful, practical, expert but approachable
- No generic AI phrases: "tóm lại", "nhìn chung", "không thể phủ nhận"
- Every paragraph must add value — no filler sentences

### Keyword placement
```
Primary keyword: H1 + first 100 words + meta title + meta description + 1–2 H2s
Secondary keywords: sprinkled naturally in H2/H3 and body text
Keyword density: 1–2% — write naturally, not mechanically
```

### Content depth per type
| Type | Min words | Required sections |
|---|---|---|
| Pillar | 2,000 | Intro, 6+ H2 sections, comparison table, FAQ, CTA |
| How-to | 1,500 | Intro, prerequisites, numbered steps, safety/tips, FAQ, CTA |
| Informational | 1,200 | Intro, 4+ H2 sections, table/comparison, FAQ, CTA |
| Commercial | 1,200 | Intro, comparison table, price table, pros/cons, FAQ, CTA |
| Theme/long-tail | 1,000 | Intro, 3–4 H2 sections, checklist/table, CTA |

---

## Step 3.2 — Internal Links: Placement Rules

**CRITICAL: Links must appear in the article body, not just in the link map.**

### When to place internal links
- After introducing a subtopic that has its own cluster article → link to that article
- When mentioning a related concept covered elsewhere → link contextually
- At the end of a section → "Xem thêm: [related article]"
- In the CTA box → always link to product/category page

### Anchor text rules
```
✅ GOOD — descriptive, keyword-rich:
   <a href="/cach-choi-pinata/">cách chơi pinata đúng cách</a>
   <a href="/pinata-sinh-nhat-cho-be-trai/">15 mẫu pinata sinh nhật cho bé trai</a>

❌ BAD — generic:
   <a href="/cach-choi-pinata/">xem thêm tại đây</a>
   <a href="/pinata-sinh-nhat-cho-be-trai/">bài viết này</a>
```

### Minimum links per article (in body only, excluding CTA box)
- Pillar: links to ALL cluster articles + 1 bridge link to previous cluster
- Each cluster article: ≥ 3 links (1 back to pillar + 2 to other articles/pages)

---

## Step 3.3 — SEO Meta Tags Template

```
Title tag (≤60 chars):
[Primary Keyword]: [Brief Subtitle] | [Brand Name]

Meta description (150–160 chars):
[Primary keyword in first 5 words]. [Value proposition]. [Secondary keyword]. [CTA with phone/contact].

URL slug: [primary-keyword-slug]
Category: [blog category name]
Tags: [keyword1], [keyword2], [keyword3]
Featured image alt: [primary keyword] – [description] – [brand name]
```

---

## Step 3.4 — Schema Templates

### Article (required for ALL articles)
```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "@id": "https://[domain]/[slug]/#article",
  "headline": "[Title tag text]",
  "description": "[Meta description text]",
  "url": "https://[domain]/[slug]/",
  "datePublished": "YYYY-MM-DD",
  "dateModified": "YYYY-MM-DD",
  "author": {
    "@type": "Organization",
    "name": "[Brand Name]",
    "url": "https://[domain]"
  },
  "publisher": {
    "@type": "Organization",
    "name": "[Brand Name]",
    "url": "https://[domain]",
    "logo": {
      "@type": "ImageObject",
      "url": "https://[domain]/logo.svg",
      "width": 200,
      "height": 60
    }
  },
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "https://[domain]/[slug]/"
  },
  "keywords": "[kw1], [kw2], [kw3], [kw4]",
  "inLanguage": "vi-VN"
}
```

### FAQPage (required for ALL articles — minimum 3 Q&As for cluster, 5 for pillar)
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "@id": "https://[domain]/[slug]/#faq",
  "mainEntity": [
    {
      "@type": "Question",
      "@id": "https://[domain]/[slug]/#faq-[slug-of-question]",
      "name": "[Question text — use actual search query phrasing]",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "[Answer in plain text, no HTML. 2–4 sentences. Include primary keyword naturally.]"
      }
    }
  ]
}
```

**FAQ writing rules:**
- Questions must mirror actual search queries ("Pinata sinh nhật giá bao nhiêu?" not "Giá cả?")
- Answers must be self-contained (no "as mentioned above")
- Each answer: 2–4 sentences, 40–80 words
- No HTML tags inside answer text

### HowTo (required for step-by-step guides)
```json
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "@id": "https://[domain]/[slug]/#howto",
  "name": "[Action-oriented title: 'Cách [verb] [object]']",
  "description": "[1–2 sentence description of the process]",
  "totalTime": "PT[N]M",
  "estimatedCost": {
    "@type": "MonetaryAmount",
    "currency": "VND",
    "value": "[number]"
  },
  "tool": [
    {"@type": "HowToTool", "name": "[Tool name]"}
  ],
  "supply": [
    {"@type": "HowToSupply", "name": "[Supply name]"}
  ],
  "step": [
    {
      "@type": "HowToStep",
      "position": 1,
      "name": "[Step headline — 3–6 words]",
      "text": "[Full step description — 2–4 sentences with specific actions]",
      "url": "https://[domain]/[slug]/#buoc-1"
    }
  ]
}
```

### ItemList (required for "Top N" or comparison articles)
```json
{
  "@context": "https://schema.org",
  "@type": "ItemList",
  "@id": "https://[domain]/[slug]/#itemlist",
  "name": "[List title matching H1]",
  "numberOfItems": N,
  "itemListOrder": "https://schema.org/ItemListOrderDescending",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "[Item name]",
      "url": "https://[domain]/[product-or-article-url]",
      "description": "[1 sentence description]"
    }
  ]
}
```

### BreadcrumbList (required for ALL articles)
```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "@id": "https://[domain]/[slug]/#breadcrumb",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Trang chủ",
      "item": {
        "@type": "WebPage",
        "@id": "https://[domain]",
        "url": "https://[domain]",
        "name": "Trang chủ [Brand]"
      }
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "[Pillar title]",
      "item": {
        "@type": "WebPage",
        "@id": "https://[domain]/[pillar-slug]/",
        "url": "https://[domain]/[pillar-slug]/",
        "name": "[Pillar title]"
      }
    },
    {
      "@type": "ListItem",
      "position": 3,
      "name": "[This article title]",
      "item": {
        "@type": "WebPage",
        "@id": "https://[domain]/[slug]/",
        "url": "https://[domain]/[slug]/",
        "name": "[This article title]"
      }
    }
  ]
}
```
*Note: Pillar pages use only 2 breadcrumb levels (Home → Pillar).*

---

## Step 3.5 — Schema Validation (mandatory before Phase 4)

After writing all schema, run:

```python
import json, re

html = open('draft.html').read()
pre_blocks = re.findall(r'<pre[^>]*>(.*?)</pre>', html, re.DOTALL)
ok = 0; errors = []
for block in pre_blocks:
    import html as htmllib
    decoded = htmllib.unescape(block)
    scripts = re.findall(r'<script type=[^>]+>(.*?)</script>', decoded, re.DOTALL)
    for s in scripts:
        try:
            json.loads(s.strip())
            ok += 1
        except Exception as e:
            errors.append(str(e))

print(f"Schema: {ok} valid, {len(errors)} errors")
for e in errors: print(f"  ERROR: {e}")
```

**Also validate:**
- No `itemReviewed` inside `aggregateRating` (common Google error)
- No HTML tags inside FAQ `text` fields
- BreadcrumbList `item` must be `WebPage` object, not plain string
- `geo.latitude` and `geo.longitude` must be numbers, not strings

---

## Step 3.6 — Content Writing Checklist

Per article:
```
☐ H1 contains primary keyword
☐ First 100 words contain primary keyword
☐ Meta title ≤60 chars, keyword near start
☐ Meta description 150–160 chars, has CTA
☐ ≥3 internal links in body (not only in il-map)
☐ Anchor text is descriptive (not "click here")
☐ CTA box links to product/service page
☐ All schema JSON is valid
☐ Article, FAQPage, BreadcrumbList present
☐ HowTo present if step-by-step article
☐ ItemList present if Top-N article
```
