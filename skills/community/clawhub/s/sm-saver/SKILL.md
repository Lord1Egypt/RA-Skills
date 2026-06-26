---
name: sm-saver
description: Save and digest resources from social media posts (X/Twitter, LinkedIn) or any URL. Use when the user shares a tweet URL, a LinkedIn post, or any link they want to keep and understand. Extracts linked resources, fetches their content, and appends a structured entry to the resource log.
metadata: {"openclaw":{"requires":{"bins":["xurl"]}}}
---

# SM Saver

Extracts, summarizes, and logs resources from social media posts or direct URLs.

## Output log

Append all saved entries to `~/workspace/resources.md` (create if missing).

## Workflow

### 1. Detect source type

| Pattern | Type |
|---------|------|
| `x.com/*` or `twitter.com/*` | Twitter/X post |
| `linkedin.com/*` | LinkedIn post |
| Anything else | Direct URL |

### 2. Fetch content

**Twitter/X** — use `xurl`:

```json
{
  "tool": "exec",
  "command": "xurl read <tweet_url>"
}
```

Parse the JSON response:
- Extract `data.text` (tweet body)
- Extract `data.entities.urls[].expanded_url` (linked resources, skip `t.co` self-references and pic.twitter.com)
- Extract `data.author_id` or author handle if available

**LinkedIn / Direct URL** — skip to step 3 directly with the URL itself as the resource.

### 3. Summarize each resource

For each extracted URL (or the URL itself if direct):

```json
{
  "tool": "exec",
  "command": "summarize \"<url>\" --length short"
}
```

If `summarize` is not installed, fall back to:

```json
{
  "tool": "exec",
  "command": "python3 -c \"\nimport urllib.request, sys\nreq = urllib.request.Request('<url>', headers={'User-Agent': 'Mozilla/5.0'})\nwith urllib.request.urlopen(req, timeout=10) as r:\n    html = r.read().decode('utf-8', errors='ignore')\nimport re\ntitle = re.search(r'<title>(.*?)</title>', html, re.I)\nprint(title.group(1).strip() if title else '<url>')\n\""
}
```

If a URL is inaccessible (auth wall, timeout), note it as `[inaccessible]` and continue.

### 4. Append to resources.md

Format — **strict, no deviation**:

```markdown
## {YYYY-MM-DD} · {source_label}
> {tweet text or first sentence of post — max 120 chars, truncate with …}

{For each resource:}
- [{title}]({url}) — {1-line summary, max 80 chars}

---
```

`source_label`:
- Twitter: `@{handle}` if extractable, else `X`
- LinkedIn: `LinkedIn`
- Direct: domain name (e.g. `github.com`)

### 5. Confirm to user

Respond with exactly:

```
💾 {N} resource(s) saved · {source_label}
{title of first resource, truncated to 60 chars}
```

If nothing was extractable: `⚠️ No resources found in this link.`

## Examples

| User says | Source type | Result |
|-----------|------------|--------|
| "https://x.com/karpathy/status/123456" | Twitter/X | Extract tweet text + linked URLs, summarize each, append to `resources.md` |
| "https://linkedin.com/posts/someone-123" | LinkedIn | Fetch page, summarize, append to `resources.md` |
| "Save this: https://github.com/anthropics/claude-code" | Direct URL | Fetch title + summary, append to `resources.md` |
| "https://x.com/elonmusk/status/789 garde ça" | Twitter/X | Extract tweet + linked resources, summarize, append to `resources.md` |
