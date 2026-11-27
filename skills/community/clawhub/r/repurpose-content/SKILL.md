---
name: repurpose-content
description: Turn a blog post, article URL, video, transcript or long text into platform-specific social posts and threads, then draft or schedule them with Auto Poster AI. Use when the user says "turn this into posts", "promote this article", "repurpose", or pastes a URL or long text to share on social media.
---

# Repurpose content into social posts

Uses the Auto Poster AI MCP tools (`autoposter_*`).

## Workflow

1. **Get the source.** Fetch the URL or read the pasted text. If you cannot read it, ask the user to paste it. Do not write posts from a title alone.
2. **Pull out the material.** One main idea, 2 to 4 supporting points, one concrete number or quote, and the link.
3. **Pick platforms.** Use what the user named. If none, call `autoposter_list_accounts` and propose the connected ones.
4. **Check limits.** Call `autoposter_get_rules`.
5. **Write one version per platform**, not one text pasted everywhere:
   - **X / Threads / Bluesky:** a hook in the first line, one idea. Long source: a thread via `threadComments`.
   - **LinkedIn:** short opening line, white space, a takeaway the reader can use. Link in `firstComment`.
   - **Instagram / Facebook:** a hook plus context, hashtags at the end or in `firstComment`.
   - **TikTok / YouTube Shorts:** a caption and title only; say if a video is needed.
   - **Pinterest:** keyword-rich title and description.
6. **Show all versions** and wait for the user's edits.
7. **Hand off to `schedule-social-posts`** to draft or schedule once the user approves.

## Rules

- Only claim what the source says. No made-up stats, quotes or results.
- Keep the author's voice if the user gave examples; otherwise plain and specific, no hype words.
- Offer two hook options for the main platform, not for all of them.
- Include the source link unless the user says not to.
