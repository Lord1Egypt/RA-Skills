# Markdown to HTML Conversion Rules

Rules for converting AI-generated markdown content to WordPress-compatible HTML.

## Pre-Processing Steps

### 1. Strip YAML Front-Matter
Remove everything between opening and closing `---` delimiters. Extract these values for WP API fields; do not include in HTML body.

### 2. Remove H1 Title
The `# Title` becomes the WP `title` field. Remove from body to prevent double-title display.

---

## Core Conversion Rules

| Markdown | HTML Output |
|----------|-------------|
| `# H1` | Extract as title, remove from body |
| `## H2` | `<h2>` |
| `### H3` | `<h3>` |
| `**bold**` | `<strong>` |
| `*italic*` | `<em>` |
| `[text](url)` | `<a href="url">text</a>` |
| `![alt](url)` | `<img src="url" alt="alt">` (then upload & rewrite) |
| `` `code` `` | `<code>` |
| Code fence | `<pre><code class="language-X">` |
| `---` | `<hr>` |
| `> blockquote` | `<blockquote>` |
| `- list item` | `<ul><li>` |
| `1. list item` | `<ol><li>` |

---

## Edge Cases

### Tables
Convert to proper HTML tables:
```html
<table>
  <thead><tr><th>Col1</th><th>Col2</th></tr></thead>
  <tbody><tr><td>Val1</td><td>Val2</td></tr></tbody>
</table>
```

### Code Fences with Language Hint
Becomes:
```html
<pre><code class="language-python">def hello():
    return "world"
</code></pre>
```

If Prism.js or Highlight.js is installed, the `language-X` class triggers syntax highlighting.

### Line Breaks
- Single newline within a paragraph: ignore (same paragraph)
- Double newline: new `<p>` tag
- Trailing spaces + newline: `<br>` tag

---

## WP Block Editor (Gutenberg) vs. Classic Editor

**Classic Editor**: Standard HTML works fine, no block markup needed.

**Block Editor**: Plain HTML via API still renders correctly — WP adds block wrappers on next edit. For precise block control:

```html
<!-- wp:paragraph -->
<p>Your content here.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":2} -->
<h2>Your heading</h2>
<!-- /wp:heading -->
```

For batch publishing, plain HTML via API is acceptable unless the site uses custom blocks.

---

## Image Handling

### External URL Images
1. Download image to temp location
2. Upload to WP: `POST /wp-json/wp/v2/media`
3. Get `source_url` from response
4. Replace original `src` with `source_url`

### Generated Images `![prompt](gen:<prompt>)`
1. Generate image using configured image generator
2. Upload to WP media library
3. Replace `gen:<prompt>` src with uploaded `source_url`

### Featured Image
- First image: optionally use as `featured_media` (upload separately, set ID)
- Remaining images: inline within content HTML

---

## What NOT to Convert

- Do not convert HTML already in the markdown (pass through as-is)
- Do not strip `<iframe>` embeds (YouTube, etc.)
- Do not add `<html>`, `<head>`, or `<body>` wrappers

---

## Validation Checklist

- [ ] All `<img>` src attributes point to WP media library URLs
- [ ] No `# H1` heading remains in body content
- [ ] Code blocks have correct `<pre><code>` wrapping
- [ ] Tables are valid HTML (thead/tbody structure)
- [ ] No unclosed HTML tags
- [ ] No raw markdown syntax visible in HTML output
