# Feed Validation Checklist (v1.0.0)

Run this checklist before presenting any generated feed to the user.
Mark each item ✅ (pass), ⚠️ (warning — proceed with note), or ❌ (fail — fix before output).

---

## RSS 2.0 Checklist

### Structure
- [ ] Root element is `<rss version="2.0">`
- [ ] Exactly one `<channel>` child of `<rss>`
- [ ] Channel has `<title>`, `<link>`, and `<description>` (all required)
- [ ] `<atom:link rel="self">` present with correct MIME type `application/rss+xml`

### Per-Item
- [ ] Every `<item>` has `<title>` OR `<description>` (at least one required)
- [ ] Every `<item>` has `<link>` (absolute URL)
- [ ] Every `<item>` has `<guid>` equal to the post URL
- [ ] `<guid isPermaLink="true">` set when GUID is a URL
- [ ] `<pubDate>` is valid RFC 822 format (`Mon, 01 Jan 2024 00:00:00 +0000`)
- [ ] Items with estimated dates have `<!-- date-estimated -->` comment

### Content
- [ ] All `&` in text nodes escaped as `&amp;` (or in CDATA)
- [ ] All `<` in text nodes escaped as `&lt;` (or in CDATA)
- [ ] HTML content wrapped in `<![CDATA[…]]>`
- [ ] No `<item>` has an empty `<title>` and empty `<description>`
- [ ] No duplicate `<guid>` values across items

### URLs
- [ ] `<channel><link>` is an absolute URL (https://)
- [ ] All `<item><link>` values are absolute URLs
- [ ] `<atom:link href>` points to intended feed hosting location

---

## Atom 1.0 Checklist

### Structure
- [ ] Root element is `<feed xmlns="http://www.w3.org/2005/Atom">`
- [ ] Feed has `<title>`, `<id>`, and `<updated>` (all required)
- [ ] `<link rel="self">` with `type="application/atom+xml"` present
- [ ] `<link rel="alternate">` pointing to the source page present

### Per-Entry
- [ ] Every `<entry>` has `<title>`, `<id>`, and `<updated>` (all required)
- [ ] `<entry><id>` is an absolute URI (use canonical post URL)
- [ ] `<updated>` is valid ISO 8601 with timezone (`2024-01-01T00:00:00Z`)
- [ ] `<link rel="alternate">` present per entry
- [ ] Entries with estimated dates have `<!-- date-estimated -->` comment

### Content
- [ ] `<summary>` or `<content>` present per entry (strongly recommended)
- [ ] `<content type="html">` uses CDATA or proper entity escaping
- [ ] No duplicate `<id>` values across entries

### URLs
- [ ] Feed `<id>` is stable (page URL is acceptable)
- [ ] All `<link href>` values are absolute URLs

---

## General Checks (both formats)

- [ ] XML declaration present: `<?xml version="1.0" encoding="UTF-8"?>`
- [ ] Encoding is UTF-8 throughout
- [ ] No items have placeholder text (e.g., `{{item_title}}`)
- [ ] Item count ≤ configured maximum (default 20)
- [ ] Items sorted newest-first
- [ ] `<generator>` tag identifies this as a synthetic feed
- [ ] Feed parses without errors (mental well-formedness check: all tags closed,
      attributes quoted, no stray `<` or `&` outside CDATA)

---

## Automatic Fixes

Apply silently before output:

| Issue                         | Fix                                              |
|-------------------------------|--------------------------------------------------|
| Relative `<link>` URL         | Resolve to absolute using page origin            |
| Missing `<guid>`              | Set equal to `<link>` with `isPermaLink="true"`  |
| HTML entities in title        | Decode, then re-encode safely                    |
| Trailing whitespace in text   | Strip                                            |
| `pubDate` in wrong timezone   | Convert to `+0000`                               |
| Duplicate items               | Deduplicate by URL                               |

---

## Validator Tools (for user reference)

| Tool                        | URL                                      |
|-----------------------------|------------------------------------------|
| W3C Feed Validator           | https://validator.w3.org/feed/           |
| RSS Board Validator          | https://www.rssboard.org/rss-validator   |
| Atom Feed Validator          | https://validator.w3.org/feed/#validate_by_input |
