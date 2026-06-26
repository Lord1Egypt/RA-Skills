---
name: web-fetch
description: Fetch a known URL and return the page as markdown, plain text, raw HTML, or a downloaded image file using the local fetch.js helper. Use this whenever the user gives or implies a specific URL and wants you to retrieve, inspect, quote, summarize, convert, or save that page or asset. Prefer this skill over web-search when discovery is not needed, including for docs pages, blog posts, raw HTML inspection, and direct image downloads.
compatibility: opencode
metadata:
  runtime: node
  transport: fetch
---

# Web Fetch

Use this skill when the target URL is already known and the job is retrieval, not search.

Common cases:
- fetch a documentation page the user already linked
- pull an article into readable markdown or plain text before summarizing it
- inspect raw HTML to debug markup, metadata, or page structure
- download a remote image to a local path for later inspection or processing

If the user needs help finding the right page first, use `web-search` before this skill.

## Command

Run:

```bash
node ./fetch.js --url "https://example.com"
```

Optional flags:
- `--format markdown|text|html`
- `--timeout <seconds>`
- `--output <path>` for image responses

## Choose the right format

Default to `markdown` unless the user clearly wants something else.

- `markdown`: best for readable docs, articles, and summarization
- `text`: best when the user wants the cleanest plain-text extraction
- `html`: best when inspecting source markup, metadata, links, embeds, or page structure
- `--output <path>`: use when the response is an image and you want a stable saved file path instead of a temp file

Examples:

```bash
node ./fetch.js --url "https://example.com/docs" --format markdown
```

```bash
node ./fetch.js --url "https://example.com/page" --format text --timeout 20
```

```bash
node ./fetch.js --url "https://example.com/page" --format html
```

```bash
node ./fetch.js --url "https://example.com/logo.png" --output /tmp/logo.png
```

## How to work with the result

The CLI prints a `<web_fetch>` block.

For text-like responses it includes:
- `title`
- `url`
- `mime`
- `format`
- `content`

For image responses it includes:
- `title`
- `url`
- `mime`
- `image`

After fetching:
1. Read the returned fields carefully.
2. Use only the parts relevant to the user's request.
3. Summarize or quote concise excerpts instead of dumping the whole page unless the user asked for the full content.
4. If you fetched HTML, explain notable structure or metadata rather than pasting large raw blobs unless needed.
5. If you downloaded an image, tell the user the saved file path.

## Behavior and limits

Keep these in mind while using the tool:
- `http://` URLs are tried as `https://` first, then retried as plain HTTP if needed.
- Default timeout is 30 seconds; maximum is 120 seconds.
- Responses larger than 5MB are rejected.
- Browser-like headers are used, with a retry path for some Cloudflare 403 challenge responses.
- SVG is treated as text, not as a binary image attachment.

## Failure handling

If the fetch fails:
- verify the URL is complete and starts with `http://` or `https://`
- retry with a different format only if the user's goal changed
- if the page is too large, blocked, or times out, tell the user plainly and suggest a narrower target URL or an alternate source
