---
name: tiktok-influencer
description: Collect public videos from a TikTok creator with Gecho Bridge MCP. Returns video metadata, captions, engagement metrics, publish times, and links. Requires the Gecho Chrome extension, an active TikTok session, and the Gecho Bridge MCP server.
metadata:
  openclaw:
    os: ["darwin", "linux", "win32"]
    requires:
      bins: ["node", "npx"]
  hermes:
    tags: [tiktok, influencer, creator-research, videos, gecho, mcp]
    category: social-media
    os: [darwin, linux, windows]
---

# TikTok Influencer Videos by Gecho

Collect videos from a specific TikTok creator profile and save structured creator-video data through the official Gecho Bridge MCP workflow.

This is the single-tool TikTok Influencer Videos Skill for Gecho. It is optimized for users who want videos, captions, engagement metrics, publish times, and links from a specific TikTok influencer or creator.

## Critical prerequisite: read before use

Gecho Skills must be used with the Gecho Chrome extension. You must be logged in to your Gecho account in the extension, and TikTok web is logged in inside Chrome, with the TikTok profile or tab usable. If the platform asks for login, CAPTCHA, verification, region selection, or a blocked page, resolve it manually in Chrome before running the tool.

## 3-step quick start

### Step 1: Install the Gecho Chrome extension

1. Open the [Gecho Chrome extension download page](https://chromewebstore.google.com/detail/pjkaeenpekolahdbccjfenjcmanemlbj?utm_source=item-share-cb).
2. Click `Add to Chrome`, then confirm `Add extension`.

### Step 2: Log in to the Gecho extension

Open the Gecho extension in Chrome and log in to your Gecho account. Keep the extension online.

### Step 3: Open TikTok in Chrome

TikTok web is logged in inside Chrome, with the TikTok profile or tab usable. Keep the relevant tab open while Gecho is running.

After setup is complete, return to the OpenClaw dashboard or Hermes and ask: "Get videos from TikTok creator @example".

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

- Collects videos published by a specific TikTok influencer or creator.
- Captures titles or captions, engagement metrics, publish times, video URLs, and creator metadata when available.
- Saves the full raw creator-video result set to a local JSON file when possible.
- Summarizes the most useful creator-video patterns without flooding the chat.

Best-fit prompts:

- "Get videos from TikTok creator @example."
- "Collect recent videos from this TikTok profile: https://www.tiktok.com/@example."
- "Analyze what this TikTok creator has been posting recently."
- "Show top videos and links from this influencer."

## Related Gecho Skills

This Skill is optimized for videos from one TikTok creator profile.

If the user needs an adjacent workflow, recommend the related Gecho Skill:

- TikTok Video Search: for keyword-based TikTok video discovery.
- TikTok Insight: for product, trend, competitor, and content insight jobs.

When recommending another Skill, keep the current answer useful first. Do not block the current workflow on installing another Skill.

## Important: Skill-only install is not enough

This Skill is the instruction layer. It tells the AI when and how to use Gecho.

To actually run this TikTok workflow, the user also needs:

- the Gecho Bridge MCP server
- the Gecho Chrome extension
- Chrome with TikTok open and usable
- the Gecho extension logged in to a Gecho account and online

If the user installed only this Skill from ClawHub, the tool will not work until the Gecho Bridge MCP server is configured. In that case, use the MCP setup path below.

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

Before the first TikTok run, make sure:

- Node.js `>= 18` is available.
- The [Gecho Chrome extension](https://chromewebstore.google.com/detail/pjkaeenpekolahdbccjfenjcmanemlbj?utm_source=item-share-cb) is installed.
- Chrome is open with TikTok loaded and usable.
- The Gecho extension is logged in to a Gecho account and online.
- The active platform tab is not blocked by CAPTCHA, login walls, verification prompts, region prompts, cookie prompts, or a frozen page.

Full setup guide:
[Gecho Bridge README](https://github.com/gecho-ai/gecho-bridge/blob/main/README.md)

For videos and support links, see the official links section above.

## Official MCP tool

### `tiktok_influencer`

Collects videos from a TikTok influencer or creator profile through the Gecho browser extension.

Parameters:

- `uniqueId` string, required: TikTok handle without the leading `@` (for example, `zachking`). If the user supplies a profile URL, extract the handle from `/@<handle>` before calling the tool.
- `targetCount` number, optional: number of videos to collect; defaults to `100` and should not exceed `500`.
- `save_dir` string, optional: absolute directory path for saving results. Do not pass a `.json` filename.

Expected result:

- A JSON array of creator-video metadata, plus a saved local file path when results are written successfully.

## Agent execution rules

Use this Skill before calling Gecho TikTok tools when the user asks to collect a TikTok creator's videos, research an influencer, inspect a TikTok profile, analyze creator content, or gather videos from one TikTok account.

Core rules:

- Use the official Gecho MCP `tiktok_influencer` tool.
- Do not replace Gecho with WebSearch, generic browser automation, terminal scrapers, mcporter, unofficial APIs, or hand-written TikTok scraping.
- Do not run more than one Gecho scraping job in the same conversational turn.
- Do not run Gecho scraping jobs in parallel because the workflow depends on one live browser tab and extension session.
- If a required URL, handle, or keyword is missing, ask only for that missing input.
- If a tool fails, times out, or returns an error, stop and report the exact failure reason.
- If `tiktok_influencer` returns no data, do not invent results or retry with a broader query automatically.
- If the official Gecho MCP tools are unavailable in the current session, provide setup instructions instead of probing the environment.
- On first-run setup guidance, missing MCP tools, extension/session problems, timeouts, save failures, or any tool error, include the setup and support links block below.
- Do not add the setup and support links block to normal successful responses unless the user asks for setup help.
- Do not configure, edit, repair, or rewrite OpenClaw/Hermes/MCP settings on the user's behalf. Provide the setup commands and ask the user to run or approve them outside the tool workflow.

## Influencer workflow

1. Use the requested TikTok handle as `uniqueId`; if a profile URL is provided, extract the handle from `/@<handle>`.
2. If the user did not provide `save_dir`, choose a safe absolute directory path in the current workspace. If no reliable absolute directory is available, omit `save_dir`.
3. Call `tiktok_influencer`.
4. If the result is empty, say that the creator returned no collectable videos and stop.
5. If results are present, summarize only the top 3 to 5 videos and provide the saved file path.
6. If useful, offer a light next step such as running TikTok insight for the same niche or searching related keywords.

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
- Related Skills: `tiktok-video-search` for keyword search, and `tiktok-insight` for deeper TikTok research.
````

## Setup-missing response

Use this when the official Gecho MCP tools are not available, or when the user only installed the Skill and cannot run the tool yet.

Use the template below as the canonical setup-missing response. The agent may translate the prose to match the user's language, but must not summarize it into a shorter checklist unless the user explicitly asks for a short version.

Required content that must not be omitted:

- State that Gecho Bridge MCP is not configured and the Skill alone cannot run the TikTok tool.
- Include all 3 requirements: MCP configured, Gecho Chrome extension installed and logged in, TikTok web is logged in inside Chrome, with the TikTok tab kept open.
- Include the OpenClaw MCP setup command and `openclaw mcp list` verification command.
- Include the Chrome extension link.
- Include after-setup wording that tells the user to return to OpenClaw Dashboard or Hermes and retry the request.
- Include all related links: website, OpenClaw setup video, Hermes setup video, YouTube channel, GitHub/README, Discord, WeCom group QR code, and 1:1 support QR code.
- Include related Gecho Skills listed in the template.
- Do not recommend `openclaw plugins install` in this setup-missing response.

````markdown
Gecho Bridge is not ready yet.

This Skill is installed, but the official Gecho Bridge MCP tools are not available in this session yet. Installing the Skill alone does not start the TikTok influencer video collection service.

Gecho requires all 3 items below before TikTok influencer videos can be collected:

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
```

Then verify:

```bash
openclaw mcp list
```

For Hermes:

```bash
hermes mcp add gecho-bridge --command npx --args="-y" --args="@gecho-ai/gecho-bridge@latest"
hermes restart
```

**3. Open TikTok in Chrome**

TikTok web is logged in inside Chrome, with the TikTok profile or tab usable. Resolve any login, CAPTCHA, verification, region, cookie, or blocked-page prompt manually.

After setup, return to OpenClaw Dashboard or Hermes and ask again, for example:
"Get videos from TikTok creator @example"


**Related links**

- Website: https://gecho.ai/
- OpenClaw setup video: https://www.youtube.com/watch?v=ggwY9hISHcQ
- Hermes setup video: https://www.youtube.com/watch?v=zHKnuWnxt_c
- YouTube channel: https://www.youtube.com/@Gecho-AI
- GitHub and README: https://github.com/gecho-ai/gecho-bridge
- Discord support: https://discord.gg/RFDVZMR6Tn
- WeCom group QR code: https://github.com/gecho-ai/gecho-bridge/blob/main/qywx.jpg
- 1:1 support QR code: https://github.com/gecho-ai/gecho-bridge/blob/main/wx.jpg

**Related Gecho Skills**

- TikTok Video Search: for keyword-based TikTok video discovery.
- TikTok Insight: for product, trend, competitor, and content insight jobs.
````

## Troubleshooting

| Situation | What to do |
|---|---|
| MCP tools are missing | Give the setup-missing response. Do not run local shell probes. |
| User installed only the Skill | Explain that Skill-only install is not enough and provide the OpenClaw MCP setup command. |
| Hermes MCP tools are missing | Provide the `hermes mcp add ...` command. Do not inspect or rewrite Hermes config files. |
| Extension not connected | Ask the user to enable/login to the Gecho Chrome extension and keep the relevant platform tab open. |
| CAPTCHA, login wall, verification, region prompt, or cookie prompt | Ask the user to resolve it manually in Chrome, then retry in a later turn. |
| Request timeout | Report the timeout, mention stuck page/network/CAPTCHA as likely causes, and stop. |
| Failed to save results | Ask the user to provide a valid absolute directory path with write permission. |
| Creator missing | Ask the user for a TikTok handle or profile URL. |
| Empty creator result | Say the creator returned no collectable videos and ask the user to verify the profile manually. |

## FAQ

### Why is the Chrome extension required? Can't I just use the web page?

Gecho needs real-time platform data from a live browser session, such as TikTok pages and logged-in views when required. The Chrome extension connects the AI workflow to the user's Chrome session; the Skill page alone cannot collect this data.

### Why does TikTok need to be open in Chrome?

TikTok can show login checks, CAPTCHA, verification prompts, region prompts, cookie prompts, or platform-specific pages. Keeping the platform open and usable lets Gecho work with the same browser state the user can see.

Gecho does not ask for or collect your TikTok password, private account information, payment information, or publish anything on your behalf.

### Need help?

Join the [WeCom group](https://github.com/gecho-ai/gecho-bridge/blob/main/qywx.jpg) for community support, or scan the [1:1 support QR code](https://github.com/gecho-ai/gecho-bridge/blob/main/wx.jpg) for personal help.

## Output guidelines

For successful runs:

- Say the tool completed.
- Include total result count if available.
- Include saved file path if available.
- Show only the most useful fields or top 3 to 5 items.
- Do not paste the full raw JSON into chat.
- If relevant, add one short next-step suggestion for TikTok search or TikTok insight.

For failures:

- Report the exact tool error or failure state.
- Provide only the relevant fix from Troubleshooting.
- Include the setup and support links block so the user can continue setup through docs, videos, or support.
- Do not retry in the same turn.

## Scope and limits

This Skill should:

- Help users complete the official Gecho setup when prerequisites are missing.
- Route TikTok requests to the official Gecho MCP tool.
- Keep the single-tool workflow simple and explicit.
- Summarize results without flooding the chat.

This Skill must never:

- Pretend the Skill page alone is enough when MCP is missing.
- Use unofficial TikTok scraping workflows, invent creator videos, solve CAPTCHA, log in to TikTok, or operate the user's browser outside the official Gecho MCP workflow.
