# Worked Example — vivianvoss.net/blog

This example shows the skill applied to `https://vivianvoss.net/blog/the-graphql-tax`.

---

## Step 1 — Fetch & Inspect

```bash
curl -sL "https://vivianvoss.net/blog/the-graphql-tax" | head -200
```

The page is a **single blog post**, not a post-list page.
Navigate up to `https://vivianvoss.net/blog` to find the index.

---

## Step 2 — Feed Discovery

```bash
curl -sL "https://vivianvoss.net/blog" | grep -i 'link.*alternate\|type.*rss\|type.*atom'
```

Expected result: **no feed link found** → proceed with generation.

---

## Step 3 — Post Block Detection

Inspect `https://vivianvoss.net/blog` HTML. Typical Hugo/Gatsby static blog pattern:

```html
<!-- Likely repeating structure (illustrative): -->
<article class="post-card">
  <h2 class="post-card-title">
    <a href="/blog/the-graphql-tax">The GraphQL Tax</a>
  </h2>
  <time datetime="2024-02-10">February 10, 2024</time>
  <p class="post-card-excerpt">GraphQL promises flexibility…</p>
</article>
```

Extraction selectors:
- **Title**: `article.post-card h2 a` (inner text)
- **URL**: `article.post-card h2 a[href]` (resolve to absolute)
- **Date**: `article.post-card time[datetime]`
- **Summary**: `article.post-card p.post-card-excerpt` (first 280 chars)

---

## Step 4 — Generated RSS 2.0 Output

```xml
<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"
     xmlns:atom="http://www.w3.org/2005/Atom"
     xmlns:dc="http://purl.org/dc/elements/1.1/">
  <channel>
    <title>Vivian Voss — Blog</title>
    <link>https://vivianvoss.net/blog</link>
    <description>Writing on software engineering, APIs, and distributed systems.</description>
    <language>en</language>
    <lastBuildDate>Fri, 01 Mar 2024 00:00:00 +0000</lastBuildDate>
    <generator>RSS Feed Generator Skill v1.0 (synthetic feed)</generator>
    <atom:link href="https://example.com/feeds/vivianvoss-net-feed.xml"
               rel="self" type="application/rss+xml"/>

    <item>
      <title><![CDATA[The GraphQL Tax]]></title>
      <link>https://vivianvoss.net/blog/the-graphql-tax</link>
      <guid isPermaLink="true">https://vivianvoss.net/blog/the-graphql-tax</guid>
      <pubDate>Sat, 10 Feb 2024 00:00:00 +0000</pubDate>
      <description><![CDATA[GraphQL promises flexibility and precise data
        fetching, but at what cost? Every abstraction layer introduces overhead
        — here is what your GraphQL gateway is actually taxing you for.]]>
      </description>
    </item>

    <!-- … additional items … -->
  </channel>
</rss>
```

---

## Step 5 — Validation Run

Against `references/validation-checklist.md`:

| Check                              | Result |
|------------------------------------|--------|
| `<rss version="2.0">` root         | ✅     |
| Channel required fields            | ✅     |
| `<atom:link rel="self">`           | ✅     |
| Items have title + link + guid     | ✅     |
| `<pubDate>` RFC 822 format         | ✅     |
| CDATA wraps HTML description       | ✅     |
| All URLs absolute                  | ✅     |
| No duplicate GUIDs                 | ✅     |
| `<generator>` tag present          | ✅     |

**Result: PASS** — ready to present to user.

---

## Output Files

- `vivianvoss-net-feed.xml` → RSS feed
- `vivianvoss-net-feed-page.html` → HTML discovery wrapper
