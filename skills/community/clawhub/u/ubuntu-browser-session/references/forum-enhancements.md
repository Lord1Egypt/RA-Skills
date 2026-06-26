# Forum/Search Result Enhancements

These helpers are optional add-ons for pages that behave like forums, topic lists, or search result pages.

Use them when the host browser is already on a page that lists many clickable topics or results and you want to:

- extract the main topic/result links instead of every navigation link
- click a result by visible text
- work with forum pages without falling back to OCR or manual tab scraping

They are generic heuristics for pages that expose topic/result links in repeated containers.

## Commands

### Extract topic/result links

```bash
python3 {baseDir}/scripts/cdp-snapshot.py --port PORT --format topic-links
```

What it does:

- prefers repeated content containers commonly seen on forums/search pages
- prefers anchors that look like primary content links inside those containers
- falls back to repeated containers under `main`/`article`/`[role=main]`, then to anchors in the main content area if no preferred containers are found

Output is JSON with `title`, `url`, and `content`, where `content` is a JSON-encoded array like:

```json
[
  {
    "text": "Example topic",
    "href": "https://example.com/t/topic/123",
    "meta": "optional snippet from the surrounding container"
  }
]
```

`meta` is optional and truncated to 400 characters.

### Click a link by visible text

```bash
python3 {baseDir}/scripts/cdp-eval.py --port PORT --click-link-text 'Example topic'
```

What it does:

- finds visible anchors whose text exactly matches or contains the requested phrase
- prefers exact matches over partial matches
- scrolls the chosen anchor into view before clicking
- returns candidate links when nothing matches
- when combined with `--navigate`, pair it with `--wait-navigation` or `--wait-for` so the destination DOM has rendered before clicking

## Notes

- `topic-links` is a best-effort heuristic, not a guaranteed universal schema.
- Works best on Discourse-style forums, topic lists, category pages, and search result pages, but also falls back to generic main-content result lists.
- On non-forum pages, prefer the generic `links` format or plain `--eval` JavaScript.
- If a site renders results inside shadow DOM, canvas, or highly dynamic widgets, fall back to direct page-specific evaluation.
