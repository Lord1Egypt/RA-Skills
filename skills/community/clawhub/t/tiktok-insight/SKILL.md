---
name: tiktok-insight
description: Run async TikTok product, trend, competitor, and content insight jobs through Gecho Bridge MCP, and check existing insight job status. Use for TikTok winning-product research, market opportunity analysis, competitor research, trend discovery, content strategy, and checking insight job results. Requires the Gecho Chrome extension, an active TikTok session, and the shared Gecho Bridge MCP server.
metadata:
  openclaw:
    os: ["darwin", "linux", "win32"]
    requires:
      bins: ["node", "npx"]
  hermes:
    tags: [tiktok, insight, product-research, trend-analysis, gecho, mcp]
    category: social-media
    os: [darwin, linux, windows]
---

# TikTok Insight by Gecho

Run async TikTok product, trend, competitor, and content insight jobs from an AI chat through the official Gecho Bridge MCP workflow.

This is the single-tool TikTok insight Skill for Gecho. It is optimized for users who want opportunity analysis, trend discovery, competitor research, content strategy, or status checks for existing TikTok insight jobs.

## Critical prerequisite: read before use

Gecho Skills must be used with the Gecho Chrome extension. You must be logged in to both your Gecho account in the extension and TikTok in the Chrome web app. If either login is missing, TikTok insight jobs may fail even though the Skill is installed.

## 3-step quick start

### Step 1: Install the Gecho Chrome extension

1. Open the [Gecho Chrome extension download page](https://chromewebstore.google.com/detail/pjkaeenpekolahdbccjfenjcmanemlbj?utm_source=item-share-cb).
2. Click `Add to Chrome`, then confirm `Add extension`.

### Step 2: Log in to the Gecho extension

Open the Gecho extension in Chrome and log in to your Gecho account. Keep the extension online.

### Step 3: Log in to TikTok web

Open TikTok in Chrome and log in to the TikTok web app. Keep the logged-in TikTok tab open.

After setup is complete, return to the OpenClaw dashboard or Hermes and ask: "Analyze xxx on TikTok". For example: "Run TikTok insight for hamburgers".

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

- Starts async TikTok insight jobs for products, niches, trends, competitors, and content angles.
- Returns a `jobId` for each started insight job.
- Checks existing insight job status and summarizes completed results.
- Helps users move from a keyword or product idea to research-backed next steps.

Best-fit prompts:

- "Run TikTok product opportunity insight for outdoor picnic mat."
- "Analyze TikTok trends for portable blender."
- "Find competitor and content angles for cat toys on TikTok."
- "Check the status of my previous TikTok insight job."

## Related Gecho Skills

This Skill is optimized for TikTok insight jobs and status checks.

If the user wants raw TikTok video examples, creators, titles, engagement metrics, or video links before or after an insight job, recommend the related Gecho TikTok video search or aggregate Skill:

- TikTok Video Search: for keyword-based TikTok video discovery and metadata collection.
- TikTok Search & Insight: for the complete TikTok research workflow that combines video search, insight jobs, and status checks.

When recommending another Skill, keep the current answer useful first. Do not block the current insight workflow on installing another Skill.

## Important: Skill-only install is not enough

This Skill is the instruction layer. It tells the AI when and how to use Gecho.

To actually run TikTok insight jobs, the user also needs:

- the Gecho Bridge MCP server
- the Gecho Chrome extension
- Chrome with TikTok logged in
- the Gecho extension logged in to a Gecho account and online

If the user installed only this Skill from ClawHub, insight jobs will not work until the Gecho Bridge MCP server is configured. In that case, use the MCP setup path below.

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

Before the first insight job, make sure:

- Node.js `>= 18` is available.
- The [Gecho Chrome extension](https://chromewebstore.google.com/detail/pjkaeenpekolahdbccjfenjcmanemlbj?utm_source=item-share-cb) is installed.
- Chrome is open with TikTok logged in.
- The Gecho extension is logged in to a Gecho account and online.
- The TikTok tab is not blocked by CAPTCHA, login walls, or a frozen page.

Full setup guide:
[Gecho Bridge README](https://github.com/gecho-ai/gecho-bridge/blob/main/README.md)

For videos and support links, see the official links section above.

## Official MCP tools

### `tiktok_insight`

Starts an asynchronous TikTok insight job for product, trend, competitor, or content research.

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

Use this Skill before calling Gecho TikTok insight tools when the user asks to analyze products, discover trends, research competitors, evaluate market opportunities, build content strategy, or check an existing TikTok insight job.

Core rules:

- Use the official Gecho MCP `tiktok_insight` and `check_insight_status` tools for TikTok insight workflows.
- Do not replace Gecho with WebSearch, browser automation, terminal scrapers, mcporter, unofficial APIs, or hand-written TikTok scraping.
- Do not start more than one Gecho insight job in the same conversational turn.
- Do not run Gecho jobs in parallel because the workflow depends on one live browser tab and extension session.
- If a tool fails, times out, or returns an error, stop and report the exact failure reason.
- If `tiktok_insight` starts successfully, report the `jobId` and explain that the user should check status later.
- If `check_insight_status` says the job is still running, tell the user to wait before checking again.
- If the official Gecho MCP tools are unavailable in the current session, provide setup instructions instead of probing the environment.
- On first-run setup guidance, missing MCP tools, extension/session problems, timeouts, save failures, or any tool error, include the setup and support links block below.
- Do not add the setup and support links block to normal successful insight responses unless the user asks for setup help.
- Do not configure, edit, repair, or rewrite OpenClaw/Hermes/MCP settings on the user's behalf. Provide the setup commands and ask the user to run or approve them outside the tool workflow.

Allowed status behavior:

- A user may explicitly ask to check one existing `jobId`; in that case, call `check_insight_status` once.
- Do not start a new `tiktok_insight` job in the same turn after checking status unless the user asks again in a later turn.

## Standard workflows

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
5. If useful, offer a light next step such as collecting raw TikTok video examples for the same keyword.

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
- Related Skills: `tiktok-video-search` for focused video search, and `tiktok-search` for the complete TikTok search and insight workflow.
````

## Setup-missing response

Use this when the official Gecho MCP tools are not available, or when the user only installed the Skill and cannot run insight jobs yet.

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

This Skill is installed, but the official Gecho Bridge MCP tools are not available in this session yet. Installing the Skill alone does not start the TikTok insight service.

Gecho requires all 3 items below before TikTok insight jobs can run:

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
"Run TikTok insight for computers"


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

For successful insight start:

- Say the insight job started.
- Include the `jobId`.
- Include expected saved path if available.
- Tell the user to check status later.

For completed insight:

- Summarize key findings.
- Include saved file path.
- Avoid claiming conclusions not supported by returned tool data.
- If relevant, add one short next-step suggestion for TikTok video search or the aggregate TikTok research workflow.

For failures:

- Report the exact tool error or failure state.
- Provide only the relevant fix from Troubleshooting.
- Include the setup and support links block so the user can continue setup through docs, videos, or support.
- Do not retry in the same turn.

## Scope and limits

This Skill should:

- Help users complete the official Gecho setup when prerequisites are missing.
- Route TikTok insight and status-check requests to the official Gecho MCP tools.
- Keep insight and status-check flows explicit.
- Summarize results without flooding the chat.

This Skill must never:

- Pretend the Skill page alone is enough when MCP is missing.
- Pretend `tiktok_insight` is synchronous.
- Use unofficial TikTok scraping workflows.
- Invent results when the tool returns no data.
- Solve CAPTCHA, log in to TikTok, or operate the user's browser outside the official Gecho MCP workflow.
