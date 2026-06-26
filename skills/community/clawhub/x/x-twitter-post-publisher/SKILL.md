---
name: x-twitter-post-publisher
description: Publish posts to X/Twitter from plain text or markdown post banks using OpenCLI with an already logged-in browser session. Use when the user wants to auto-post to X/Twitter, especially when content lives in a markdown file with sections like "Post 1" / "Post 3", when normal browser typing leaves the Post button disabled, or when you need a reliable Windows workflow that uses clipboard paste to activate X's Draft.js editor before posting.
---

# X/Twitter Post Publisher

Use this skill to publish to X/Twitter through the user's existing logged-in browser context.

## Core rule

Do **not** trust visible text alone inside X compose. X uses a Draft.js editor. Regular DOM injection or some automation typing paths can leave the **Post** button disabled even when text appears in the editor.

Use the verified path:
1. Open compose in the logged-in browser context
2. Put final text onto the system clipboard
3. Focus the composer
4. `Ctrl+A` then `Backspace` to clear stale draft text
5. `Ctrl+V` to paste
6. Verify the Post button is enabled
7. Click Post
8. Verify by searching for a unique snippet or checking the author's timeline

## Preferred workflow

### A. Publish from a markdown file

Run the bundled script:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/publish-x-post.ps1 -MarkdownPath "C:\path\to\posts.md" -PostLabel "Post 1"
```

Optional dry run:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/publish-x-post.ps1 -MarkdownPath "C:\path\to\posts.md" -PostLabel "Post 1" -DryRun
```

### B. Publish direct text

```powershell
powershell -ExecutionPolicy Bypass -File scripts/publish-x-post.ps1 -Text "Your final X post here"
```

## What the script does

- Extract the requested post from markdown or use direct text
- Count characters before publishing
- Refuse to post when text is over the configured limit (default 280)
- Open `https://x.com/compose/post` in OpenCLI browser
- Use native clipboard paste so X recognizes the input
- Check button state via `browser eval`
- Click Post only after the button becomes enabled
- Verify with `opencli twitter search`

## Markdown format expectation

The extractor is designed for sections like:

```markdown
**Post 1 — Insight hook**
Line 1

Line 2

---
```

It also tolerates `**Post 1**` style headers.

## Troubleshooting

Read `references/troubleshooting.md` when:
- the Post button stays disabled
- the wrong browser session is being used
- duplicate text appears in the composer
- search verification does not find the post immediately

## Notes

- Prefer `opencli browser` / `opencli twitter` over isolated browser-agent sessions when the user is already logged into Chrome.
- If a post is too long, shorten it first; do not try to brute-force submission.
- If verification is inconclusive, search for a unique snippet from the published text before claiming success.
