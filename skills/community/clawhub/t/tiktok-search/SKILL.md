---
name: tiktok-search
description: Search TikTok videos and run product, trend, competitor, and content insights through Gecho Bridge MCP. Use for TikTok keyword research, trending video discovery, winning-product analysis, and checking async insight jobs. Requires the Gecho Chrome extension, an active TikTok session, and the shared Gecho Bridge MCP server.
metadata:
  openclaw:
    os: ["darwin", "linux", "win32"]
    requires:
      bins: ["node", "npx"]
  hermes:
    tags: [tiktok, search, insight, gecho, mcp]
    category: social-media
    os: [darwin, linux, windows]
---

# TikTok Search & Insight by Gecho

Search TikTok from an AI chat, collect structured video metadata, and run async product or trend insight jobs through the official Gecho Bridge MCP workflow.

This is the default TikTok aggregate Skill for Gecho. It covers the TikTok video search and TikTok insight workflow. Single-tool TikTok Skills may exist for distribution and search traffic, but this Skill is the recommended default for users who want the complete TikTok research workflow.

## Critical prerequisite: read before use

Gecho Skills must be used with the Gecho Chrome extension. You must be logged in to both your Gecho account in the extension and TikTok in the Chrome web app. If either login is missing, all TikTok search and insight features may fail even though the Skill is installed.

## 3-step quick start

### Step 1: Install the Gecho Chrome extension

1. Open the [Gecho Chrome extension download page](https://chromewebstore.google.com/detail/pjkaeenpekolahdbccjfenjcmanemlbj?utm_source=item-share-cb).
2. Click `Add to Chrome`, then confirm `Add extension`.

### Step 2: Log in to the Gecho extension

Open the Gecho extension in Chrome and log in to your Gecho account. Keep the extension online.

### Step 3: Log in to TikTok web

Open TikTok in Chrome and log in to the TikTok web app. Keep the logged-in TikTok tab open.

After setup is complete, return to the OpenClaw dashboard or Hermes and ask: "Search xxx on TikTok". For example: "Search hamburgers on TikTok".

## Official links and setup help

- Website: [gecho.ai](https://gecho.ai/)
- GitHub: [gecho-ai/gecho-bridge](https://github.com/gecho-ai/gecho-bridge)
- YouTube channel: [@Gecho-AI](https://www.youtube.com/@Gecho-AI)
- Chrome extension: [Gecho Extension](https://chromewebstore.google.com/detail/pjkaeenpekolahdbccjfenjcmanemlbj?utm_source=item-share-cb)
- OpenClaw setup video: [OpenClaw + TikTok: Direct AI Browser Control via Gecho Bridge](https://www.youtube.com/watch?v=ggwY9hISHcQ)
- Hermes setup video: [Hermes + TikTok: Direct AI Browser Control via Gecho Bridge](https://www.youtube.com/watch?v=zHKnuWnxt_c)
- Discord: [https://discord.gg/RFDVZMR6Tn](https://discord.gg/RFDVZMR6Tn)
- WeCom group QR code: [qywx.jpg](https://github.com/gecho-ai/gecho-bridge/blob/main/qywx.jpg)

## What this skill does

- Finds high-performing TikTok videos for a keyword.
- Collects titles, authors, engagement data, and video links.
- Saves full raw result sets to a local JSON file.
- Starts async insight jobs for product research, competitor analysis, and trend discovery.

Best-fit prompts:

- "Search TikTok for portable blender and show the top liked videos."
- "Find winning hooks for cat toy videos."
- "Run product opportunity insight for outdoor picnic mat."
- "Check the status of my previous TikTok insight job."

## Important: Skill-only install is not enough

This Skill is the instruction layer. It tells the AI when and how to use Gecho.

To actually run TikTok searches, the user also needs:

- the Gecho Bridge MCP server
- the Gecho Chrome extension
- Chrome with TikTok logged in
- the Gecho extension logged in to a Gecho account and online

If the user installed only this Skill from ClawHub, searches will not work until the Gecho Bridge MCP server is configured. In that case, use the MCP setup path below.

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

Before the first search, make sure:

- Node.js `>= 18` is available.
- The [Gecho Chrome extension](https://chromewebstore.google.com/detail/pjkaeenpekolahdbccjfenjcmanemlbj?utm_source=item-share-cb) is installed.
- Chrome is open with TikTok logged in.
- The Gecho extension is logged in to a Gecho account and online.
- The TikTok tab is not blocked by CAPTCHA, login walls, or a frozen page.

Full setup guide:
[Gecho Bridge README](https://github.com/gecho-ai/gecho-bridge/blob/main/README.md)

For videos and support links, see the official links section above.

## Tool choice

| User goal | Use tool | Notes |
|---|---|---|
| Search TikTok videos and collect metadata | `tiktok_search` | Returns results directly |
| Analyze a niche, product, trend, or competitor opportunity | `tiktok_insight` | Starts an async job and returns a `jobId` |
| Check an existing async insight job | `check_insight_status` | Use the `jobId` returned by `tiktok_insight` |

Use this aggregate Skill for broad TikTok research requests. If the user explicitly asks for one exact raw tool only, such as "run tiktok_search", a matching single-tool distribution Skill may be used instead when available.

## Official MCP tools

### `tiktok_search`

Searches TikTok for a keyword, scrolls the page through the Gecho browser extension, returns structured metadata, and saves the full result set.

Parameters:

- `query` string, required: search keyword or phrase.
- `save_dir` string, optional: absolute directory path for saving results. Do not pass a `.json` filename. Omit this parameter if no reliable absolute directory is available.

Expected result:

- A JSON array of video metadata, plus a saved local file path when results are written successfully.

### `tiktok_insight`

Starts an asynchronous TikTok insight job for product, trend, or competitor research.

Parameters:

- `query` string, required: search keyword or product/category phrase.
- `save_dir` string, optional: absolute directory path for saving results. Do not pass a `.json` filename. Omit this parameter if no reliable absolute directory is available.

Expected result:

- A `jobId`. The final result must be checked later with `check_insight_status`.

### `check_insight_status`

Checks the status or final result of an existing insight job.

Parameters:

- `jobId` string, required: the job ID returned by `tiktok_insight`.

Expected result:

- `running`, `error`, or completed insight data.

## Agent execution rules

Use this Skill before calling any Gecho TikTok MCP tool when the user asks to search TikTok, find trending videos, analyze competitors, collect TikTok metadata, discover winning products, or research keyword trends.

Core rules:

- Use only the official Gecho MCP tools: `tiktok_search`, `tiktok_insight`, and `check_insight_status`.
- Do not replace Gecho with WebSearch, browser automation, terminal scrapers, mcporter, unofficial APIs, or hand-written TikTok scraping.
- Do not start more than one Gecho scraping or insight job in the same conversational turn.
- Do not run Gecho scraping jobs in parallel because the workflow depends on one live browser tab and extension session.
- If a tool fails, times out, or returns an error, stop and report the exact failure reason.
- If `tiktok_search` returns no items, do not rewrite, translate, broaden, or retry the keyword automatically.
- If `tiktok_insight` starts successfully, report the `jobId` and explain that the user should check status later.
- If `check_insight_status` says the job is still running, tell the user to wait before checking again.
- If the official Gecho MCP tools are unavailable in the current session, provide setup instructions instead of probing the environment.
- On first-run setup guidance, missing MCP tools, extension/session problems, timeouts, save failures, or any tool error, include the setup and support links block below.
- Do not add the setup and support links block to normal successful search or insight responses unless the user asks for setup help.
- Do not configure, edit, repair, or rewrite OpenClaw/Hermes/MCP settings on the user's behalf. Provide the setup commands and ask the user to run or approve them outside the tool workflow.
- Do not use this Skill for TikTok Shop, X/Twitter, Amazon, or other platform workflows; those should have their own Gecho aggregate Skills.

Allowed status behavior:

- A user may explicitly ask to check one existing `jobId`; in that case, call `check_insight_status` once.
- Do not start a new `tiktok_search` or `tiktok_insight` job in the same turn after checking status unless the user asks again in a later turn.

## Standard workflows

### Search workflow

1. Use the exact keyword requested by the user.
2. If the user did not provide `save_dir`, choose a safe absolute directory path in the current workspace. If no reliable absolute directory is available, omit `save_dir` and let Gecho use its default data directory.
3. Call `tiktok_search`.
4. If the result is empty, say that the exact keyword returned no results and stop.
5. If results are present, summarize only the top 3 to 5 items and provide the saved file path.

### Insight workflow

1. Use the exact product, niche, or keyword requested by the user.
2. If the user did not provide `save_dir`, choose a safe absolute directory path in the current workspace. If no reliable absolute directory is available, omit `save_dir` and let Gecho use its default data directory.
3. Call `tiktok_insight`.
4. Report the returned `jobId`.
5. Tell the user the job may take several minutes and should be checked later with `check_insight_status`.

### Status workflow

1. Call `check_insight_status` with the provided `jobId`.
2. If still running, report the current status and recommend waiting about 60 seconds.
3. If completed, summarize the key findings and provide the saved file path.
4. If failed, report the exact error and stop.

## Setup and support links block

Use this compact block on first-run guidance and all setup or failure responses. Keep it near the end of the answer, after the exact fix.

````markdown
Helpful Gecho links:

- Website: https://gecho.ai/
- YouTube channel: https://www.youtube.com/@Gecho-AI
- OpenClaw setup video: https://www.youtube.com/watch?v=ggwY9hISHcQ
- Hermes setup video: https://www.youtube.com/watch?v=zHKnuWnxt_c
- GitHub and README: https://github.com/gecho-ai/gecho-bridge
- Support: Discord https://discord.gg/RFDVZMR6Tn, WeCom QR https://github.com/gecho-ai/gecho-bridge/blob/main/qywx.jpg
````

## Setup-missing response

Use this when the official Gecho MCP tools are not available, or when the user only installed the Skill and cannot run searches yet.

Use the template below as the canonical setup-missing response. The agent may translate the prose to match the user's language, but must not summarize it into a shorter checklist unless the user explicitly asks for a short version.

Required content that must not be omitted:

- State that Gecho Bridge MCP is not configured and the Skill alone cannot run TikTok.
- Include all 3 requirements: MCP configured, Gecho Chrome extension installed and logged in, TikTok web logged in and tab kept open.
- Include the OpenClaw MCP setup command and `openclaw mcp list` verification command.
- Include the Chrome extension link.
- Include after-setup wording that tells the user to return to OpenClaw Dashboard or Hermes and retry the request.
- Include all related links: website, OpenClaw setup video, Hermes setup video, YouTube channel, GitHub/README, Discord, and WeCom QR code.
- Include related Gecho Skills listed in the template.
- Do not recommend `openclaw plugins install` in this setup-missing response.

````markdown
Gecho Bridge is not ready yet.

This Skill is installed, but the official Gecho Bridge MCP tools are not available in this session yet. Installing the Skill alone does not start the TikTok search service.

Gecho requires all 3 items below before TikTok search or insight can run:

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

**3. Log in to TikTok web**

Open TikTok in Chrome, log in, and keep the logged-in TikTok tab open.

After setup, return to OpenClaw Dashboard or Hermes and ask again, for example:
"Search computers on TikTok"


**Related links**

- Website: https://gecho.ai/
- OpenClaw setup video: https://www.youtube.com/watch?v=ggwY9hISHcQ
- Hermes setup video: https://www.youtube.com/watch?v=zHKnuWnxt_c
- YouTube channel: https://www.youtube.com/@Gecho-AI
- GitHub and README: https://github.com/gecho-ai/gecho-bridge
- Discord support: https://discord.gg/RFDVZMR6Tn
- WeCom QR code: https://github.com/gecho-ai/gecho-bridge/blob/main/qywx.jpg

**Related Gecho Skills**

- `tiktok-video-search`: TikTok video search and metadata collection.
- `tiktok-insight`: TikTok product, trend, competitor, and content insight jobs.
- `tiktok-search`: complete TikTok search and insight workflow.
````

## Troubleshooting

| Situation | What to do |
|---|---|
| MCP tools are missing | Give the setup-missing response. Do not run local shell probes. |
| User installed only the Skill | Explain that Skill-only install is not enough and provide the OpenClaw MCP setup command. |
| Hermes MCP tools are missing | Provide the `hermes mcp add ...` command. Do not inspect or rewrite Hermes config files. |
| Extension not connected | Ask the user to enable/login to the Gecho Chrome extension and keep a logged-in TikTok tab open. |
| CAPTCHA or login wall | Ask the user to resolve it manually in Chrome, then retry in a later turn. |
| Request timeout | Report the timeout, mention stuck page/network/CAPTCHA as likely causes, and stop. |
| Empty search results | Say the exact keyword returned no results and ask the user to choose another keyword manually. |
| Insight still running | Report running status and recommend checking again after about 60 seconds. |
| Failed to save results | Ask the user to provide a valid absolute directory path with write permission. |

## FAQ

### Why is the Chrome extension required? Can't I just use the web page?

Gecho needs real-time platform data from a live browser session, such as TikTok videos and other platform data in Gecho workflows. The Chrome extension connects the AI workflow to the user's logged-in Chrome session; the Skill page alone cannot collect this data.

### Why do I need to log in to TikTok? Can I use it without login?

TikTok limits content access for logged-out users. After you log in, the extension can access the complete data available in your browser session, such as video captions/scripts, comments, engagement data, and other signals when available.

Gecho does not ask for or collect your TikTok password, private account information, or publish anything on your behalf.

### Need help?

Scan the [WeCom QR code](https://github.com/gecho-ai/gecho-bridge/blob/main/qywx.jpg) for 1:1 support.

## Output guidelines

For successful search:

- Say the search completed.
- Include total result count if available.
- Include saved file path if available.
- Show top 3 to 5 results only.
- Do not paste the full raw JSON into chat.

For successful insight start:

- Say the insight job started.
- Include the `jobId`.
- Include expected saved path if available.
- Tell the user to check status later.

For completed insight:

- Summarize key findings.
- Include saved file path.
- Avoid claiming conclusions not supported by returned tool data.

For failures:

- Report the exact tool error or failure state.
- Provide only the relevant fix from Troubleshooting.
- Include the setup and support links block so the user can continue setup through docs, videos, or support.
- Do not retry in the same turn.

## Scope and limits

This Skill should:

- Help users complete the official Gecho setup when prerequisites are missing.
- Route TikTok search and insight requests to the official Gecho MCP tools.
- Keep search, insight, and status-check flows explicit.
- Summarize results without flooding the chat.

This Skill must never:

- Pretend the Skill page alone is enough when MCP is missing.
- Pretend `tiktok_insight` is synchronous.
- Use unofficial TikTok scraping workflows.
- Invent results when the tool returns no data.
- Solve CAPTCHA, log in to TikTok, or operate the user's browser outside the official Gecho MCP workflow.
