---
name: x-thread-reader
description: Fetch full text or generate a PDF from any X/Twitter thread using twitter-thread.com. Use when asked to "get the full thread", "read this tweet", "save this thread", "download thread as PDF", or when processing X/Twitter URLs dropped in chat.
---

# X Thread Reader

Fetch full text or generate a PDF from any X/Twitter thread via twitter-thread.com.

## How It Works

**Text mode:** `curl` the twitter-thread.com `/pdf/{tweet_id}` page. The full article is embedded in the HTML `<meta name="description">` tag — no browser or JS rendering needed. Fast, reliable, zero dependencies beyond `curl` and `python3`.

**PDF mode:** Uses Chrome headless (`--print-to-pdf`) or `agent-browser` to render and save the PDF. Browser required because the PDF generation page uses JS.

## Limitations

- Requires the thread to be **indexed on twitter-thread.com** — if not indexed, visit the thread URL in a browser first to trigger indexing
- Does **NOT** work for **X Articles** (`x.com/i/article/...`) — those require a logged-in browser
- Does **NOT** work for protected/private accounts or deleted tweets

## Quick Usage

### Get full thread text
```bash
scripts/x_thread.sh text "https://x.com/user/status/1234567890"
```

### Download PDF
```bash
scripts/x_thread.sh pdf "https://x.com/user/status/1234567890"
# Custom output path:
scripts/x_thread.sh pdf "https://x.com/user/status/1234567890" "/tmp/my-thread.pdf"
```

Accepts full X/Twitter URL or raw tweet ID.

## Output Format

The text mode outputs structured content:
- **Author** and **date** from the thread
- **Full article text** — complete thread content, all tweets concatenated
- **Source URL** for citation

Suitable for archiving to Obsidian, note-taking apps, or further analysis.

## Gotchas
- The `/pdf/{id}` URL returns HTML (not a PDF) — the article is in the `<meta name="description">` tag, extracted via python3. If twitter-thread.com changes their HTML structure, this extraction breaks silently (empty output).
- Thread must be indexed on twitter-thread.com first. Fresh threads (< 30 min old) may not be available yet. The `/t/{id}` page triggers indexing when visited in a browser.
- macOS grep does not support `-P` (PCRE). All grep patterns in the script use `-oE` (extended regex) for portability.
- Very long threads may truncate in the meta description. If output seems incomplete, compare against the PDF version.
- The script extracts from the **first** `<meta name="description">` match — if the page structure adds multiple, it may grab the wrong one.

## Troubleshooting

**"Thread not found" error:**
The thread is not yet indexed on twitter-thread.com. Visit `https://twitter-thread.com/t/{tweet_id}` in a browser to trigger indexing, wait ~30s, then retry.

**Empty article text:**
twitter-thread.com may have changed their HTML structure. Check if the `<meta name="description">` tag still contains the article content.

**X Article links (`x.com/i/article/...`):**
These are NOT threads. They require a logged-in browser session and cannot be fetched with this skill.

**Protected/deleted tweets:**
The skill cannot access tweets from private accounts or tweets that have been deleted.
