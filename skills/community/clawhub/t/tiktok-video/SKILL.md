---
name: tiktok-video
description: Get TikTok video detail data and comments from a known TikTok video URL with the official Gecho Bridge MCP tool. Use when the user wants one video's metadata, comments, replies, or engagement context, not keyword video search.
metadata:
  openclaw:
    os: ["darwin", "linux", "win32"]
    requires:
      bins: ["node", "npx"]
  hermes:
    tags: [tiktok, video-detail, comments, gecho, mcp]
    category: social-media
    os: [darwin, linux, windows]
---

# TikTok Video Detail and Comments by Gecho

Use the official Gecho Bridge MCP tool to open one known TikTok video, collect its available detail data, expand the comments area, and continue scrolling to collect comments and replies.

This is the single-tool TikTok video detail Skill for Gecho. It is optimized for a known video URL. Keyword discovery belongs to `tiktok-video-search`; product, trend, competitor, and content research belongs to `tiktok-insight` or the aggregate `tiktok-search` Skill.

## Critical prerequisite: read before use

Gecho Skills must be used with the Gecho Chrome extension. You must be logged in to both your Gecho account in the extension and TikTok in the Chrome web app. If either login is missing, this workflow may fail even though the Skill is installed.

If TikTok shows a login wall, CAPTCHA, verification prompt, region selection, cookie consent, unavailable video, private account, deleted video, or blocked page, resolve the issue manually in Chrome before running the tool again.

## 3-step quick start

### Step 1: Install the Gecho Chrome extension

1. Open the [Gecho Chrome extension download page](https://chromewebstore.google.com/detail/pjkaeenpekolahdbccjfenjcmanemlbj?utm_source=item-share-cb).
2. Click `Add to Chrome`, then confirm `Add extension`.

### Step 2: Log in to the Gecho extension

Open the Gecho extension in Chrome and log in to your Gecho account. Keep the extension online.

### Step 3: Log in to TikTok web

Open TikTok in Chrome and log in to the TikTok web app. Keep the logged-in TikTok tab open and usable.

After setup is complete, return to the OpenClaw dashboard or Hermes and ask: "Get the details and comments for this TikTok video: https://www.tiktok.com/@user/video/123".

## Official links and setup help

- Website: [gecho.ai](https://gecho.ai/)
- GitHub: [gecho-ai/gecho-bridge](https://github.com/gecho-ai/gecho-bridge)
- YouTube channel: [@Gecho-AI](https://www.youtube.com/@Gecho-AI)
- Chrome extension: [Gecho Extension](https://chromewebstore.google.com/detail/pjkaeenpekolahdbccjfenjcmanemlbj?utm_source=item-share-cb)
- OpenClaw setup video: [OpenClaw + TikTok: Direct AI Browser Control via Gecho Bridge](https://www.youtube.com/watch?v=ggwY9hISHcQ)
- Hermes setup video: [Hermes + TikTok: Direct AI Browser Control via Gecho Bridge](https://www.youtube.com/watch?v=zHKnuWnxt_c)
- Discord: [https://discord.gg/RFDVZMR6Tn](https://discord.gg/RFDVZMR6Tn)
- WeCom group QR code: [qywx.jpg](https://github.com/gecho-ai/gecho-bridge/blob/main/qywx.jpg)
- 1:1 support QR code: [wx.jpg](https://github.com/gecho-ai/gecho-bridge/blob/main/wx.jpg)

## What this skill does

- Opens a known TikTok video detail page from the URL supplied by the user.
- Collects available video detail fields returned by the live TikTok page.
- Expands the comments area and scrolls to collect comments and replies.
- Saves the raw result set to a local JSON file when a usable directory is available.
- Summarizes the useful detail fields and a bounded sample of comments without flooding the chat.

This Skill does not search TikTok by keyword. It does not infer a video URL from a title, creator name, or screenshot unless the user provides a supported URL or asks for a separate search workflow.

Best-fit prompts:

- "Get the details and comments for this TikTok video: https://www.tiktok.com/@user/video/123."
- "Analyze the comments on this TikTok video and save the raw data."
- "Collect up to 100 comments from this TikTok video: https://www.tiktok.com/@user/video/123."
- "Show me the video's metadata, engagement context, and representative comments."

## Related Gecho Skills

This Skill is optimized for one known TikTok video and its comments.

- `tiktok-video-search`: search TikTok by keyword and collect video metadata and links.
- `tiktok-insight`: run product, trend, competitor, or content insight jobs.
- `tiktok-search`: the complete TikTok search, video collection, insight, and status workflow.
- `tiktok-influencer`: collect creator-level TikTok data when the user wants creator discovery or profiling.

When recommending another Skill, keep the current answer useful first. Do not block the current video-detail result on installing another Skill.

## Important: Skill-only install is not enough

This Skill is the instruction layer. It tells the AI when and how to use Gecho.

To actually run TikTok video detail collection, the user also needs:

- the Gecho Bridge MCP server
- the Gecho Chrome extension
- Chrome with TikTok logged in
- the Gecho extension logged in to a Gecho account and online
- a reachable, public or otherwise accessible TikTok video URL

If the user installed only this Skill from ClawHub, the video-detail tool will not work until the Gecho Bridge MCP server is configured. In that case, use the MCP setup path below.

Already installed Gecho Bridge? If `@gecho-ai/gecho-bridge-bundle` is installed and the Gecho MCP tools are visible, no extra MCP setup is needed for this Skill.

## Quick start

### OpenClaw Skill install: configure MCP

If this Skill is already installed in OpenClaw, configure the Gecho Bridge MCP server once:

```bash
openclaw mcp set gecho-bridge '{"command":"npx","args":["-y","@gecho-ai/gecho-bridge@latest"]}'
openclaw gateway restart
```

Then verify:

```bash
openclaw mcp list
```

The result should expose the official `tiktok_video` tool.

### Optional: OpenClaw Bundle Plugin

If the user has not installed this Skill yet and prefers plugin management, the bundle plugin can install Gecho with the MCP entry configured:

```bash
openclaw plugins install clawhub:@gecho-ai/gecho-bridge-bundle
openclaw gateway restart
```

To upgrade later:

```bash
openclaw plugins update clawhub:@gecho-ai/gecho-bridge-bundle
openclaw gateway restart
```

### Hermes setup

```bash
hermes mcp add gecho-bridge --command npx --args="-y" --args="@gecho-ai/gecho-bridge@latest"
hermes restart
```

If Hermes cannot find `npx` even though Node.js is installed, use the absolute `npx` path. On many macOS Homebrew installs this is:

```bash
hermes mcp add gecho-bridge --command /opt/homebrew/bin/npx --args="-y" --args="@gecho-ai/gecho-bridge@latest"
hermes restart
```

## First-run checklist

Before the first video-detail request, make sure:

- Node.js `>= 18` is available.
- The [Gecho Chrome extension](https://chromewebstore.google.com/detail/pjkaeenpekolahdbccjfenjcmanemlbj?utm_source=item-share-cb) is installed.
- Chrome is open with TikTok logged in.
- The Gecho extension is logged in to a Gecho account and online.
- The user supplied a complete TikTok video URL, normally containing `/video/`.
- The video is not blocked by CAPTCHA, a login wall, a private account, a deleted page, or a frozen tab.

Full setup guide:
[Gecho Bridge README](https://github.com/gecho-ai/gecho-bridge/blob/main/README.md)

For videos and support links, see the official links section above.

## Official MCP tool

### `tiktok_video`

Gets TikTok video detail data and comments. It opens the video detail page, expands comments, and continues scrolling to collect comments and replies.

Parameters:

- `url` string, required: TikTok video detail-page URL, for example `https://www.tiktok.com/@user/video/123...`.
- `targetCount` number, optional: maximum number of comments and replies to collect; default and maximum are `200`.
- `save_dir` string, optional: absolute directory path for saving results. Do not pass a `.json` filename. Omit this parameter if no reliable absolute directory is available.

Expected result:

- Structured video detail data.
- A comments and replies collection, subject to what TikTok exposes in the live session and the requested limit.
- A saved local file path when results are written successfully.

## Agent execution rules

Use this Skill before calling Gecho TikTok video detail when the user provides a TikTok video URL and asks for metadata, comments, replies, engagement context, or raw detail data.

Core rules:

- Use the official Gecho MCP `tiktok_video` tool for this focused workflow.
- Do not use `tiktok_search` when the user already supplied a specific video URL and wants that video's details.
- Do not replace Gecho with WebSearch, browser automation, terminal scrapers, mcporter, unofficial APIs, or hand-written TikTok scraping.
- Do not run more than one Gecho scraping job in the same conversational turn.
- Do not run Gecho scraping jobs in parallel because the workflow depends on one live browser tab and extension session.
- If the video URL is missing, ask only for the video URL; do not guess a URL from a title or creator name.
- If `targetCount` is provided, clamp it to the tool's supported maximum of `200` and explain the adjustment briefly if needed.
- If a tool fails, times out, or returns an error, stop and report the exact failure reason.
- If the page is private, deleted, unavailable, or blocked, report that state instead of inventing detail or comments.
- If the official Gecho MCP tools are unavailable in the current session, provide setup instructions instead of probing the environment.
- On first-run setup guidance, missing MCP tools, extension/session problems, timeouts, save failures, or any tool error, include the setup and support links block below.
- Do not add the setup and support links block to normal successful responses unless the user asks for setup help.
- Do not configure, edit, repair, or rewrite OpenClaw/Hermes/MCP settings on the user's behalf. Provide the setup commands and ask the user to run or approve them outside the tool workflow.

## Focused workflow

1. Check that the user supplied a TikTok video detail URL.
2. Preserve the URL as provided. Do not rewrite tracking parameters or substitute a different video.
3. If the user did not provide `save_dir`, choose a safe absolute directory path in the current workspace. If no reliable directory is available, omit `save_dir` and let Gecho use its default data directory.
4. Pass `url`, the bounded `targetCount` when requested, and `save_dir` when reliable to `tiktok_video`.
5. Wait for the single job to finish; do not call another Gecho scraping tool in parallel.
6. If the result is empty or the page is unavailable, state that clearly and stop.
7. If details are present, summarize the video's identity and available metrics, then show a representative sample of comments and replies.
8. Include the saved file path when available.
9. Offer one useful next step only when relevant, such as keyword search for related videos, TikTok insight, or creator research.

## Setup and support links block

Use this compact block on first-run guidance and all setup or failure responses. Keep it near the end of the answer, after the exact fix.

````markdown
Helpful Gecho links:

- Website: https://gecho.ai/
- YouTube channel: https://www.youtube.com/@Gecho-AI
- OpenClaw setup video: https://www.youtube.com/watch?v=ggwY9hISHcQ
- Hermes setup video: https://www.youtube.com/watch?v=zHKnuWnxt_c
- GitHub and README: https://github.com/gecho-ai/gecho-bridge
- Support: Discord https://discord.gg/RFDVZMR6Tn, WeCom group QR https://github.com/gecho-ai/gecho-bridge/blob/main/qywx.jpg, 1:1 support QR https://github.com/gecho-ai/gecho-bridge/blob/main/wx.jpg
- Related Skills: `tiktok-video-search` for keyword discovery, `tiktok-insight` for focused research, and `tiktok-search` for the complete TikTok workflow.
````

## Setup-missing response

Use this when the official Gecho MCP tools are not available, or when the user only installed the Skill and cannot run video-detail collection yet.

Use the template below as the canonical setup-missing response. The agent may translate the prose to match the user's language, but must not summarize it into a shorter checklist unless the user explicitly asks for a short version.

Required content that must not be omitted:

- State that Gecho Bridge MCP is not configured and the Skill alone cannot collect TikTok video details.
- Include all 3 requirements: MCP configured, Gecho Chrome extension installed and logged in, and TikTok web logged in with the tab kept open.
- Include the OpenClaw MCP setup command and `openclaw mcp list` verification command.
- Include the Hermes setup command when the user uses Hermes.
- Include the Chrome extension link.
- Include after-setup wording that tells the user to return to OpenClaw Dashboard or Hermes and retry with the full TikTok video URL.
- Include all related links: website, OpenClaw setup video, Hermes setup video, YouTube channel, GitHub/README, Discord, WeCom group QR code, and 1:1 support QR code.
- Include related Gecho Skills listed in the template.
- Do not recommend `openclaw plugins install` in this setup-missing response.

````markdown
Gecho Bridge is not ready yet.

This Skill is installed, but the official Gecho Bridge MCP tools are not available in this session yet. Installing the Skill alone does not start the TikTok video-detail service.

Gecho requires all 3 items below before video details and comments can be collected:

1. Gecho Bridge MCP is configured.
2. The Gecho Chrome extension is installed and logged in to a Gecho account.
3. TikTok web is logged in inside Chrome, with the TikTok tab kept open.

Follow these first-time setup steps:

**1. Install the Gecho Chrome extension**

Chrome Web Store:
https://chromewebstore.google.com/detail/pjkaeenpekolahdbccjfenjcmanemlbj?utm_source=item-share-cb

After installing, open the extension and log in to your Gecho account.

**2. Configure Gecho Bridge MCP**

OpenClaw MCP setup:
```bash
openclaw mcp set gecho-bridge '{"command":"npx","args":["-y","@gecho-ai/gecho-bridge@latest"]}'
openclaw gateway restart
openclaw mcp list
```

Hermes setup:
```bash
hermes mcp add gecho-bridge --command npx --args="-y" --args="@gecho-ai/gecho-bridge@latest"
hermes restart
```

**3. Log in to TikTok**

Open TikTok in the same Chrome profile, log in, and keep the TikTok tab open. Make sure the supplied video URL can be opened in that session.

After setup is complete, return to OpenClaw Dashboard or Hermes and retry with the full TikTok video URL.

Helpful links:

- Website: https://gecho.ai/
- OpenClaw setup video: https://www.youtube.com/watch?v=ggwY9hISHcQ
- Hermes setup video: https://www.youtube.com/watch?v=zHKnuWnxt_c
- YouTube channel: https://www.youtube.com/@Gecho-AI
- GitHub and README: https://github.com/gecho-ai/gecho-bridge
- Discord support: https://discord.gg/RFDVZMR6Tn
- WeCom group QR code: https://github.com/gecho-ai/gecho-bridge/blob/main/qywx.jpg
- 1:1 support QR code: https://github.com/gecho-ai/gecho-bridge/blob/main/wx.jpg

Related Gecho Skills:

- `tiktok-video-search`: keyword-based TikTok video search.
- `tiktok-insight`: product, trend, competitor, and content insight jobs.
- `tiktok-search`: complete TikTok search and insight workflow.
````

## Troubleshooting

| Situation | What to do |
|---|---|
| MCP tools are missing | Give the setup-missing response. Do not run local shell probes. |
| User installed only the Skill | Explain that Skill-only install is not enough and provide the OpenClaw MCP setup command. |
| Hermes MCP tools are missing | Provide the `hermes mcp add ...` command. Do not inspect or rewrite Hermes config files. |
| Extension not connected | Ask the user to enable/login to the Gecho Chrome extension and keep a logged-in TikTok tab open. |
| Video URL is missing | Ask for the exact TikTok video detail URL. Do not search by title in this Skill. |
| URL is not a video URL | Ask the user to provide a URL containing the TikTok video path, normally `/video/`. |
| CAPTCHA or login wall | Ask the user to resolve it manually in Chrome, then retry in a later turn. |
| Private, deleted, or unavailable video | Report the page state and ask the user to provide an accessible video URL if appropriate. |
| Request timeout | Report the timeout, mention a stuck page, network issue, or CAPTCHA as likely causes, and stop. |
| Comments are fewer than requested | Explain that TikTok exposed fewer comments or replies in the live session; do not fabricate or silently retry. |
| Failed to save results | Ask the user to provide a valid absolute directory path with write permission. |

## FAQ

### Is this the same as TikTok video search?

No. `tiktok-video` handles one known video URL and collects its detail data, comments, and replies. `tiktok-video-search` finds videos by keyword with `tiktok_search`.

### Why is the Chrome extension required?

Gecho needs real-time platform data from a live browser session. The Chrome extension connects the AI workflow to the user's logged-in Chrome session; the Skill page alone cannot access TikTok detail pages or comments.

### Can I provide a creator URL or hashtag instead?

Not for this focused Skill. Provide a specific TikTok video detail URL. Use `tiktok-video-search` for keyword discovery or `tiktok-influencer` for creator-level research.

### How many comments can it collect?

The requested `targetCount` is capped at `200`. The actual count depends on what TikTok exposes in the live page and session.

### Does this Skill publish, like, or comment on TikTok?

No. It only reads the accessible video detail page and comments through the official Gecho workflow. It does not publish content or interact on the user's behalf.

### Need help?

Join the [WeCom group](https://github.com/gecho-ai/gecho-bridge/blob/main/qywx.jpg), visit [Discord](https://discord.gg/RFDVZMR6Tn), or scan the [1:1 support QR code](https://github.com/gecho-ai/gecho-bridge/blob/main/wx.jpg) for personal help.

## Output guidelines

For successful video-detail collection:

- Say that the requested TikTok video was opened and processed.
- Include the video URL or a normalized short reference when useful.
- Summarize available identity and engagement fields without inventing missing values.
- Report the number of comments/replies collected when available.
- Show a bounded representative sample rather than pasting the full raw JSON.
- Include the saved file path when available.
- If relevant, suggest one next step: keyword search, TikTok insight, or creator research.

For failures:

- Report the exact tool error or page failure state.
- Provide only the relevant fix from Troubleshooting.
- Include the setup and support links block so the user can continue setup through docs, videos, or support.
- Do not retry in the same turn.

## Scope and limits

This Skill should:

- Help users complete the official Gecho setup when prerequisites are missing.
- Route known TikTok video-detail requests to the official `tiktok_video` MCP tool.
- Collect available video metadata, comments, and replies from the live browser session.
- Preserve a bounded result set and summarize it clearly.

This Skill must never:

- Pretend the Skill page alone is enough when MCP is missing.
- Use unofficial TikTok scraping workflows.
- Invent video fields, comments, replies, or engagement metrics.
- Turn a missing URL into an automatic keyword search.
- Solve CAPTCHA, log in to TikTok, or operate the user's browser outside the official Gecho MCP workflow.
- Publish, like, follow, comment, or otherwise mutate TikTok content.
