# Post Extraction Rules (v1.0.0)

Reference guide for identifying post/article entries inside arbitrary HTML pages.

---

## Step 1 — Candidate Block Detection

Look for the **largest repeating group** of semantically similar elements.
Evaluate in this priority order:

| Priority | Element / Pattern                                         | Notes                            |
|----------|-----------------------------------------------------------|----------------------------------|
| 1        | `<article>` tags                                          | Semantic HTML5 — most reliable   |
| 2        | `<li>` inside `<ul class="posts|articles|entries|feed…">` | Common blog list pattern         |
| 3        | `<div class="post|entry|article|card|item|blog-post…">`   | Framework-generated classes      |
| 4        | `<section>` with heading + link inside                    | Less common but valid            |
| 5        | Manually specified selector (user-provided)               | Fallback / override              |

**Minimum threshold:** Accept a pattern only if it repeats ≥ 2 times.

---

## Step 2 — Title Extraction

Within each candidate block, search for the **title** using this cascade:

1. `<h1>`, `<h2>`, or `<h3>` (first occurrence inside block)
2. `<a>` with class matching `/title|heading|post-title|entry-title/i`
3. `<meta property="og:title">` (page-level fallback — only for single-post pages)
4. First `<strong>` or `<b>` if no heading found

Strip HTML tags; decode HTML entities; trim whitespace.

---

## Step 3 — Link Extraction

1. `<a href>` on or wrapping the title element → **canonical URL**
2. `<a rel="bookmark">` within the block
3. `<a class="read-more|continue|permalink">` within the block
4. If multiple links found, prefer the one whose text matches the title

**Normalise all URLs:**
```
base_url = page origin (scheme + host)
base_href = <base href="…"> if present, else base_url
item_url  = urljoin(base_href, href)
```

---

## Step 4 — Date Extraction

| Source                              | Parser                                                   |
|-------------------------------------|----------------------------------------------------------|
| `<time datetime="YYYY-MM-DD…">`     | Use `datetime` attribute directly                        |
| `<time>` inner text                 | Parse as human date (see patterns below)                 |
| `<span class="date|published|…">`   | Parse inner text as human date                           |
| `<meta property="article:published_time">` | ISO 8601 meta tag                               |
| JSON-LD `datePublished`             | ISO 8601 value in embedded script tag                    |
| URL path segment                    | e.g. `/2024/03/15/` → 2024-03-15                         |
| No date found                       | Use scrape timestamp (UTC); add `<!-- date-estimated -->` |

### Human Date Patterns (regex hints)

```
\b(\d{1,2})\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w*\s+(\d{4})\b
\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w*\s+(\d{1,2}),?\s+(\d{4})\b
\b(\d{4})-(\d{2})-(\d{2})\b
\b(\d{1,2})/(\d{1,2})/(\d{2,4})\b
```

Relative expressions ("3 days ago", "yesterday") → subtract from scrape time.

### RFC 822 Output (for RSS 2.0)
```
Mon, 01 Jan 2024 00:00:00 +0000
```

### ISO 8601 Output (for Atom 1.0)
```
2024-01-01T00:00:00Z
```

---

## Step 5 — Description / Summary Extraction

1. `<meta name="description">` (page-level; usable only for single-item pages)
2. `<p class="excerpt|summary|description|lede|lead">` inside block
3. First `<p>` inside the block (trim to ≤ 280 characters + "…")
4. `<meta property="og:description">` as final fallback

Always strip HTML tags for plain-text `<description>`.
If embedding HTML, wrap in `<![CDATA[…]]>`.

---

## Step 6 — Author Extraction

1. `<address rel="author">` or `<a rel="author">` inside block
2. `<span class="author|byline|by-line|post-author">` inside block
3. `<meta name="author">` (page-level fallback)
4. JSON-LD `author.name`
5. Omit field if not found (optional in both RSS and Atom)

---

## Step 7 — Full-Text Fetch (optional, `/fulltext` mode)

When the user requests full text:
1. Collect all item URLs from the list page.
2. Fetch each URL individually.
3. Extract `<article>` or main content area using `<main>`, `[role="main"]`,
   or the largest block of `<p>` tags.
4. Embed as `<content:encoded>` (RSS) or `<content type="html">` (Atom).
5. Warn if fetching more than 20 items (performance + rate-limit risk).

---

## Common Site Patterns

| Platform       | Post container              | Title selector        | Date selector                   |
|----------------|-----------------------------|-----------------------|---------------------------------|
| WordPress      | `article.post`              | `.entry-title a`      | `time.entry-date`               |
| Ghost           | `article.post-card`         | `.post-card-title`    | `time[datetime]`                |
| Hugo (default) | `article` or `.summary`     | `h2 a`                | `.date`, `time`                 |
| Jekyll Minima  | `li.post`                   | `a.post-link`         | `span.post-meta`                |
| Substack       | `div.post-preview`          | `.post-preview-title` | `time[datetime]`                |
| Medium         | `article`                   | `h2`                  | `span` with date text           |
| Custom/unknown | Largest repeating structure | First heading + link  | First date-pattern text or time |
