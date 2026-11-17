---
name: tiktok-shop-search
description: Search TikTok Shop products by keyword with the official Gecho Bridge MCP tool and return structured product data, prices, ratings, sales signals, and links. Use when the user wants TikTok Shop product discovery or competitor product research.
metadata:
  openclaw:
    os: ["darwin", "linux", "win32"]
    requires:
      bins: ["node", "npx"]
  hermes:
    tags: [tiktok, shop, product-search, ecommerce, gecho, mcp]
    category: ecommerce
    os: [darwin, linux, windows]
---

# TikTok Shop Product Search by Gecho

Use the official Gecho Bridge MCP tool to search TikTok Shop for products matching a keyword. This is a single-tool Skill: use it for product discovery, not general TikTok video search.

## Critical prerequisite: read before use

Gecho Skills must be used with the Gecho Chrome extension. You must be logged in to both your Gecho account in the extension and TikTok Shop in the Chrome web app. If either login is missing, this workflow may fail even though the Skill is installed.

If the platform asks for login, CAPTCHA, verification, region selection, cookie consent, or a blocked page, resolve it manually in Chrome before running the tool.

## 3-step quick start

### Step 1: Install the Gecho Chrome extension

1. Open the [Gecho Chrome extension download page](https://chromewebstore.google.com/detail/pjkaeenpekolahdbccjfenjcmanemlbj?utm_source=item-share-cb).
2. Click Add to Chrome, then confirm Add extension.

### Step 2: Log in to the Gecho extension

Open the Gecho extension in Chrome and log in to your Gecho account. Keep the extension online.

### Step 3: Log in to TikTok Shop

Open TikTok Shop in Chrome and log in. Keep the logged-in TikTok Shop tab open and usable.

After setup is complete, return to the OpenClaw dashboard or Hermes and ask: "Search TikTok Shop for portable blender and show the top products.".

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
- Routes requests to the official tiktok_shop_search workflow.
- Collects structured TikTok Shop data and saves raw results when possible.
- Summarizes useful fields and links without flooding the chat.
- Keeps browser, login, CAPTCHA, timeout, and save-failure handling explicit.

Best-fit prompts:
- "Search TikTok Shop for portable blender and show the top products."
- "Collect the structured result and save it to my research folder."
- "Show the most useful fields and links from this TikTok Shop task."

## Related Gecho Skills

This Skill is optimized for the single TikTok Shop workflow described above.

If the user needs an adjacent workflow, recommend the related Gecho Skill:

- `tiktok-product`: product detail collection.
- `tiktok-shop`: combined TikTok Shop discovery and product-detail research.
- `tiktok-video-search`: TikTok video search and metadata collection.
- `tiktok-search`: complete TikTok search and insight workflow.

When recommending another Skill, keep the current answer useful first. Do not block the current workflow on installing another Skill.

## Important: Skill-only install is not enough

This Skill is the instruction layer. It tells the AI when and how to use Gecho.

To actually run this TikTok Shop workflow, the user also needs:

- the Gecho Bridge MCP server
- the Gecho Chrome extension
- Chrome with TikTok Shop logged in
- the Gecho extension logged in to a Gecho account and online

If the user installed only this Skill from ClawHub, the tool will not work until the Gecho Bridge MCP server is configured. In that case, use the MCP setup path below.

Already installed Gecho Bridge? If the Gecho MCP tools are visible, no extra MCP setup is needed for this Skill.

## Quick start

### OpenClaw Skill install: configure MCP

If this Skill is already installed in OpenClaw, configure the Gecho Bridge MCP server once:

~~~bash
openclaw mcp set gecho-bridge '{"command":"npx","args":["-y","@gecho-ai/gecho-bridge@latest"]}'
openclaw gateway restart
~~~

Then verify:

~~~bash
openclaw mcp list
~~~

### Optional: OpenClaw Bundle Plugin

If the user has not installed this Skill yet and prefers plugin management:

~~~bash
openclaw plugins install clawhub:@gecho-ai/gecho-bridge-bundle
openclaw gateway restart
~~~

To upgrade later:

~~~bash
openclaw plugins update clawhub:@gecho-ai/gecho-bridge-bundle
openclaw gateway restart
~~~

### Hermes setup

~~~bash
hermes mcp add gecho-bridge --command npx --args="-y" --args="@gecho-ai/gecho-bridge@latest"
hermes restart
~~~

If Hermes cannot find npx, use the absolute npx path; on many macOS Homebrew installations this is:

~~~bash
hermes mcp add gecho-bridge --command /opt/homebrew/bin/npx --args="-y" --args="@gecho-ai/gecho-bridge@latest"
hermes restart
~~~

## First-run checklist

- Node.js >= 18 is available.
- The Gecho Chrome extension is installed.
- Chrome is open and logged in to TikTok Shop.
- The Gecho extension is logged in to a Gecho account and online.
- The TikTok Shop tab is not blocked by CAPTCHA, login walls, verification prompts, region prompts, cookie prompts, or a frozen page.

Full setup guide:
[Gecho Bridge README](https://github.com/gecho-ai/gecho-bridge/blob/main/README.md)


## Official MCP tool

### `tiktok_shop_search`

Search TikTok Shop and collect structured product results.

Parameters:

- `query` string, required: product keyword or phrase.
- `targetCount` number, optional: desired product count; default `100`.
- `save_dir` string, optional: absolute directory for saving results; pass a directory, not a `.json` filename.

Expected result: a product data array and, when saved successfully, a local result path.

## Agent execution rules

Use this Skill before calling Gecho TikTok Shop tools when the user asks to use this focused workflow, collect structured results, save data, or research this platform.

Core rules:

- Use the official Gecho MCP `tiktok_shop_search` tool for this workflow.
- Do not replace Gecho with WebSearch, generic browser automation, terminal scrapers, mcporter, unofficial APIs, or hand-written TikTok Shop scraping.
- Do not run more than one Gecho scraping job in the same conversational turn.
- Do not run Gecho scraping jobs in parallel because the workflow depends on one live browser tab and extension session.
- If a required URL, identifier, keyword, or marketplace is missing, ask only for that missing input.
- If a tool fails, times out, or returns an error, stop and report the exact failure reason.
- If the tool returns no items, say that the exact query returned no results and stop.
- If the official Gecho MCP tools are unavailable, provide setup instructions instead of probing the environment.
- On setup, missing-tool, extension, timeout, save, or other error responses, include the setup and support links block below.
- Do not configure OpenClaw, Hermes, or MCP settings on the user's behalf.

## Focused workflow

1. Use the exact URL, identifier, keyword, or marketplace supplied by the user.
2. If save_dir is missing, choose a safe absolute directory or omit it.
3. Call `tiktok_shop_search` once.
4. If the tool returns no items, say that the exact query returned no results and stop.
5. Summarize the most useful 3 to 5 items or fields and provide the saved file path.
6. If useful, offer a light next step such as related product search or TikTok insight.

## Setup and support links block

Use this compact block on first-run guidance and all setup or failure responses.

~~~markdown
Helpful Gecho links:

- Website: https://gecho.ai/
- YouTube channel: https://www.youtube.com/@Gecho-AI
- OpenClaw setup video: https://www.youtube.com/watch?v=ggwY9hISHcQ
- Hermes setup video: https://www.youtube.com/watch?v=zHKnuWnxt_c
- GitHub and README: https://github.com/gecho-ai/gecho-bridge
- Support: Discord https://discord.gg/RFDVZMR6Tn, WeCom group QR https://github.com/gecho-ai/gecho-bridge/blob/main/qywx.jpg, 1:1 support QR https://github.com/gecho-ai/gecho-bridge/blob/main/wx.jpg
- `tiktok-product`: product detail collection.
- `tiktok-video-search`: TikTok video search and metadata collection.
- `tiktok-search`: complete TikTok search and insight workflow.
~~~

## Setup-missing response

Use this when official Gecho MCP tools are unavailable or the user installed only the Skill. Do not summarize this response unless the user asks for a short version.

Gecho Bridge is not ready yet.

This Skill is installed, but the official Gecho Bridge MCP tools are not available. The Skill alone does not start the TikTok Shop service.

Gecho requires:
1. Gecho Bridge MCP configured.
2. Gecho Chrome extension installed, logged in, and online.
3. TikTok Shop logged in inside Chrome with the relevant tab open.

Chrome extension: https://chromewebstore.google.com/detail/pjkaeenpekolahdbccjfenjcmanemlbj?utm_source=item-share-cb

OpenClaw MCP:
~~~bash
openclaw mcp set gecho-bridge '{"command":"npx","args":["-y","@gecho-ai/gecho-bridge@latest"]}'
openclaw gateway restart
openclaw mcp list
~~~

Hermes:
~~~bash
hermes mcp add gecho-bridge --command npx --args="-y" --args="@gecho-ai/gecho-bridge@latest"
hermes restart
~~~

Log in to TikTok Shop in Chrome, resolve prompts manually, keep the tab open, then return to OpenClaw Dashboard or Hermes and retry:
"Search TikTok Shop for portable blender and show the top products."

Related links:
https://gecho.ai/
https://www.youtube.com/watch?v=ggwY9hISHcQ
https://www.youtube.com/watch?v=zHKnuWnxt_c
https://www.youtube.com/@Gecho-AI
https://github.com/gecho-ai/gecho-bridge
https://discord.gg/RFDVZMR6Tn
https://github.com/gecho-ai/gecho-bridge/blob/main/qywx.jpg
https://github.com/gecho-ai/gecho-bridge/blob/main/wx.jpg

Related Skills:
- `tiktok-product`: product detail collection.
- `tiktok-video-search`: TikTok video search and metadata collection.
- `tiktok-search`: complete TikTok search and insight workflow.
~~~

## Troubleshooting

| Situation | What to do |
|---|---|
| MCP tools are missing | Give the setup-missing response; do not run local shell probes. |
| Skill-only install | Explain that Skill-only install is insufficient and provide the MCP setup command. |
| Extension not connected | Ask the user to enable/login to Gecho and keep a logged-in TikTok Shop tab open. |
| CAPTCHA, login wall, region, cookie, or verification prompt | Ask the user to resolve it manually in Chrome, then retry later. |
| Request timeout | Report the timeout and stop. |
| Empty results | Say the exact query returned no results and ask the user to choose another query manually. |
| Save failure | Ask for a writable absolute directory. |

## FAQ

### Why is the Chrome extension required? Can't I just use the web page?

Gecho needs real-time TikTok Shop data from a live browser session. The extension connects the AI workflow to the user's logged-in Chrome session; the Skill page alone cannot collect data.

### Why do I need to log in?

The platform may restrict content or return incomplete data for logged-out users. After login and any required region, cookie, or verification handling, the extension can access data available in the live browser session. Gecho does not ask for or collect platform passwords or payment information.

Gecho does not ask for or collect passwords, private account information, payment information, or publish anything on the user's behalf.

### Need help?

Join the [WeCom group](https://github.com/gecho-ai/gecho-bridge/blob/main/qywx.jpg) or use the [1:1 support QR code](https://github.com/gecho-ai/gecho-bridge/blob/main/wx.jpg).

## Output guidelines

For success:
- Say the tool completed.
- Include count and saved path when available.
- Show only the top 3 to 5 items or useful fields.
- Do not paste full raw JSON.

For failure:
- Report the exact error.
- Provide only the relevant fix.
- Include setup and support links.
- Do not retry in the same turn.

## Scope and limits

This Skill should route TikTok Shop requests to the official Gecho MCP tool and summarize results without flooding the chat.

This Skill must never use unofficial platform scraping, invent data, solve CAPTCHA, log in to the platform, or operate the browser outside the official Gecho MCP workflow.
