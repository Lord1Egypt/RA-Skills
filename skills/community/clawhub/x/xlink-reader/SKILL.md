---
name: x-reader
description: Read and summarize X/Twitter links with low-token routing. Use when a user shares an x.com/twitter.com/t.co link or asks to read, summarize, extract, or inspect a tweet, thread, or X article. Prefer xreach for normal tweets; use Playwright only for X article pages or t.co links that resolve to x.com/i/article/ URLs.
---

# X Reader

Use the bundled Node script to read X links with minimal token overhead.

## Workflow

1. Run `scripts/xreader.mjs` with the URL.
2. Let the script decide the cheapest path:
   - normal tweet → `xreach tweet`
   - explicit thread request → `xreach thread`
   - article / t.co → resolve first, use Playwright only when needed
3. Return the script's structured JSON; summarize from that instead of pasting raw page content.

## Positioning

- No official X API required.
- No developer application or paid X API access required.
- Works with login cookies plus low-token routing, which keeps normal tweet reads cheap and uses Playwright only when article rendering is necessary.
- Compared with `xreach`, this skill is a higher-level reader for agent workflows: it adds article handling, authored-thread filtering, and unified structured output.
- Compared with `xcurl`, this skill focuses on content extraction from links instead of low-level request control.

## Commands

Summary mode (default):

```bash
node skills/x-reader/scripts/xreader.mjs "https://x.com/..."
```

Full mode:

```bash
node skills/x-reader/scripts/xreader.mjs --mode full "https://x.com/..."
```

Thread mode (explicit only, to save tokens):

```bash
node skills/x-reader/scripts/xreader.mjs --thread "https://x.com/.../status/..."
```

Debug mode (headed browser for article extraction):

```bash
node skills/x-reader/scripts/xreader.mjs --debug "https://x.com/i/article/..."
```

## Dependencies

Required:

- `xreach`
- Node.js
- valid X auth cookies

Install article-mode dependency inside the skill directory:

```bash
cd skills/x-reader
npm install
```

## Auth

Primary auth path:

```bash
~/.config/xreader/session.json
```

Legacy fallback path:

```bash
~/.config/xfetch/session.json
```

If legacy auth exists, the script migrates it to the new path automatically.

Expected JSON format:

```json
{
  "authToken": "...",
  "ct0": "..."
}
```

## Output contract

Expect structured JSON with fields such as:

- `ok`
- `type` (`tweet`, `thread`, or `article`)
- `url`
- `canonicalUrl`
- `source` (`xreach` or `playwright`)
- `author`
- `publishedAt`
- `title`
- `text` / `contentText`
- `contentMarkdown`
- `summaryText`
- `fallback` / `warnings` / `error`

Prefer quoting or summarizing `summaryText` for low-token responses. Use `contentText` or `contentMarkdown` only when the user clearly wants more detail.

## Quick verification

Run these after install/auth setup:

```bash
node skills/x-reader/scripts/xreader.mjs "https://x.com/yangguangai/status/2033736815405121642?s=46"
node skills/x-reader/scripts/xreader.mjs "https://x.com/yangguangai/status/2033522959407878621?s=46"
node skills/x-reader/scripts/xreader.mjs --thread "https://x.com/google/status/2031558824042058064"
```

## Notes

- Default tweet reads are single-post only for token efficiency.
- Use `--thread` only when the user clearly wants the authored thread.
- Article extraction is MVP quality: good enough for reading and summarization, but long X articles with many examples/code blocks may still include some template noise.
- If article extraction fails, the script falls back to the original tweet payload and marks the failure in `warnings` / `articleError`.
- This skill relies on X login cookies (`auth_token` + `ct0`). Cookie-based automation may carry account risk, including additional verification or account restrictions. The risk is usually low for light personal use, but recommend using a secondary account instead of a primary high-value account.

## Release checklist

- Confirm `SKILL.md` includes usage, dependencies, auth path, and limitations.
- Confirm `node skills/x-reader/scripts/xreader.mjs --help` works.
- Smoke test one tweet, one article, and one thread URL.
- Confirm auth file is not packaged into the skill.
- Package the skill and verify validation passes before publishing.
