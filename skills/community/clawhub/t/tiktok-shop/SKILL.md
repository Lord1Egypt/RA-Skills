---
name: tiktok-shop
description: Search TikTok Shop products and retrieve known product details through the official Gecho Bridge MCP tools. Use for product discovery, catalog research, competitor comparison, pricing, sales signals, and item-level detail.
metadata:
  openclaw:
    os: ["darwin", "linux", "win32"]
    requires:
      bins: ["node", "npx"]
  hermes:
    tags: [tiktok, shop, ecommerce, product, research, gecho, mcp]
    category: ecommerce
    os: [darwin, linux, windows]
---

# TikTok Shop Research by Gecho

Use the official Gecho Bridge MCP tools to search TikTok Shop products and inspect a known TikTok Shop product. This is the TikTok Shop aggregate Skill for product discovery, catalog research, competitor comparison, and item-level detail.

Use `tiktok-shop-search` or `tiktok-product` when the user explicitly wants one raw workflow only. Use this aggregate Skill when the request combines discovery and product-detail research.

## Critical prerequisite: read before use

Gecho Skills must be used with the Gecho Chrome extension. You must be logged in to both your Gecho account in the extension and TikTok Shop in the Chrome web app. If either login is missing, TikTok Shop workflows may fail even though the Skill is installed.

If TikTok Shop shows a login wall, CAPTCHA, verification prompt, region selection, cookie consent, blocked page, or unavailable listing, resolve it manually in Chrome before running the tool again.

## 3-step quick start

### Step 1: Install the Gecho Chrome extension

1. Open the [Gecho Chrome extension download page](https://chromewebstore.google.com/detail/pjkaeenpekolahdbccjfenjcmanemlbj?utm_source=item-share-cb).
2. Click `Add to Chrome`, then confirm `Add extension`.

### Step 2: Log in to the Gecho extension

Open the Gecho extension in Chrome and log in to your Gecho account. Keep the extension online.

### Step 3: Log in to TikTok Shop

Open TikTok Shop in Chrome and log in. Keep the logged-in TikTok Shop tab open and usable.

After setup is complete, return to OpenClaw or Hermes and ask: "Search TikTok Shop for portable blender, then inspect the best product.".

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

- Searches TikTok Shop by keyword and collects structured product listings.
- Retrieves complete available data for a known TikTok Shop product URL or product ID.
- Supports a discovery-to-detail workflow without replacing Gecho with unofficial scraping.
- Saves raw results to a local JSON file when a reliable directory is available.
- Summarizes prices, ratings, sales signals, variants, reviews, and links without flooding the chat.

Best-fit prompts:

- "Search TikTok Shop for portable blender and show the strongest products."
- "Find TikTok Shop products for this niche, then inspect the best item."
- "Get the details, SKU, sales, and reviews for this TikTok Shop product: https://shop.tiktok.com/us/pdp/example."
- "Collect the raw TikTok Shop research data in my workspace."

## Related Gecho Skills

This Skill is the aggregate TikTok Shop workflow.

- `tiktok-shop-search`: keyword-based product discovery only.
- `tiktok-product`: known product detail collection only.
- `tiktok-search`: TikTok video search, creator collection, video details, and insight.
- `tiktok-insight`: TikTok product, trend, competitor, and content insight jobs.

When recommending another Skill, keep the current answer useful first. Do not block a TikTok Shop result on installing another Skill.

## Important: Skill-only install is not enough

This Skill is the instruction layer. It tells the AI when and how to use Gecho.

To actually run TikTok Shop research, the user also needs:

- the Gecho Bridge MCP server
- the Gecho Chrome extension
- Chrome with TikTok Shop logged in
- the Gecho extension logged in to a Gecho account and online

If the user installed only this Skill from ClawHub, the tools will not work until the Gecho Bridge MCP server is configured. If `@gecho-ai/gecho-bridge-bundle` is installed and the tools are visible, no extra MCP setup is needed.

## Quick start

### OpenClaw Skill install: configure MCP

```bash
openclaw mcp set gecho-bridge '{"command":"npx","args":["-y","@gecho-ai/gecho-bridge@latest"]}'
openclaw gateway restart
openclaw mcp list
```

The result should expose `tiktok_shop_search` and `tiktok_product`.

### Optional: OpenClaw Bundle Plugin

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

If Hermes cannot find `npx`, use its absolute path, for example `/opt/homebrew/bin/npx` on many macOS Homebrew installs.

## First-run checklist

Before the first TikTok Shop task, make sure:

- Node.js `>= 18` is available.
- The Gecho Chrome extension is installed.
- Chrome is open with TikTok Shop logged in.
- The Gecho extension is logged in and online.
- The product URL or product ID is complete when requesting item details.
- The page is not blocked by CAPTCHA, a login wall, a private shop state, or a frozen tab.

Full setup guide:
[Gecho Bridge README](https://github.com/gecho-ai/gecho-bridge/blob/main/README.md)

## Tool choice

| User goal | Use tool | Notes |
|---|---|---|
| Discover products by keyword | `tiktok_shop_search` | Returns structured listings |
| Inspect one known product | `tiktok_product` | Requires a product URL or product ID |

Use this aggregate Skill for combined TikTok Shop research. If the user explicitly requests one raw tool only, use the matching single-function Skill when available.

## Official MCP tools

### `tiktok_shop_search`

Search TikTok Shop and collect structured product results.

Parameters:

- `query` string, required: product keyword or phrase.
- `targetCount` number, optional: desired product count; default `100`.
- `save_dir` string, optional: absolute directory for saving results; pass a directory, not a `.json` filename.

Expected result: product data and a saved local result path when writing succeeds.

### `tiktok_product`

Collect the complete data available from a TikTok Shop product detail page.

Parameters:

- `product_url` string, required: TikTok Shop product URL or product ID.
- `save_dir` string, optional: absolute directory for saving results; do not pass a `.json` filename.

Expected result: structured product details such as title, price, SKU/variants, description, sales, ratings, reviews, and links when available, plus a saved local path when successful.

## Agent execution rules

Use this Skill before calling TikTok Shop MCP tools when the user asks for product discovery, product details, catalog research, competitor comparison, pricing, sales signals, or review context.

Core rules:

- Use only the official Gecho MCP tools `tiktok_shop_search` and `tiktok_product`.
- Use `tiktok_shop_search` for keyword discovery and `tiktok_product` for a known product.
- Do not replace Gecho with WebSearch, generic browser automation, terminal scrapers, mcporter, unofficial APIs, or hand-written TikTok Shop scraping.
- Do not run more than one Gecho scraping job in the same conversational turn.
- Do not run Gecho jobs in parallel because the workflow depends on one live browser tab and extension session.
- If a required keyword, product URL, or product ID is missing, ask only for that missing input.
- If a tool fails, times out, or returns an error, stop and report the exact reason.
- If a product page is unavailable, private, deleted, or blocked, report that state instead of inventing data.
- If official tools are unavailable, provide setup instructions instead of probing the local environment.
- On first-run setup, missing-tool, extension, timeout, save, or other error responses, include the setup and support links block below.
- Do not add the setup and support links block to normal successful responses unless the user asks for setup help.
- Do not configure, edit, repair, or rewrite OpenClaw, Hermes, or MCP settings on the user's behalf.

## Standard workflows

### Product discovery workflow

1. Use the exact product keyword requested by the user.
2. If no `save_dir` is provided, choose a safe absolute directory in the current workspace or omit it when no reliable directory exists.
3. Call `tiktok_shop_search`.
4. Summarize the top 3 to 5 listings and include the saved path when available.
5. If the user wants item-level detail, ask them to select a product URL or continue only when the tool returned a usable URL.

### Product detail workflow

1. Confirm that the user provided a product URL or product ID.
2. Preserve the identifier and do not substitute another product.
3. Choose or omit `save_dir` using the same safe-directory rule.
4. Call `tiktok_product`.
5. Summarize title, price, variants, sales, ratings, reviews, and links only when returned.
6. Include the saved path when available.

### Combined workflow

1. Search the user's exact keyword with `tiktok_shop_search`.
2. Show a concise shortlist and ask which product to inspect if the user did not specify one.
3. In a later turn, call `tiktok_product` for the selected product.
4. Do not launch the search and detail jobs in parallel.

## Setup and support links block

Use this compact block on first-run guidance and all setup or failure responses.

````markdown
Helpful Gecho links:

- Website: https://gecho.ai/
- YouTube channel: https://www.youtube.com/@Gecho-AI
- OpenClaw setup video: https://www.youtube.com/watch?v=ggwY9hISHcQ
- Hermes setup video: https://www.youtube.com/watch?v=zHKnuWnxt_c
- GitHub and README: https://github.com/gecho-ai/gecho-bridge
- Support: Discord https://discord.gg/RFDVZMR6Tn, WeCom group QR https://github.com/gecho-ai/gecho-bridge/blob/main/qywx.jpg, 1:1 support QR https://github.com/gecho-ai/gecho-bridge/blob/main/wx.jpg
- Related Skills: `tiktok-shop-search` for discovery and `tiktok-product` for known-product detail.
````

## Setup-missing response

Use this when the official Gecho MCP tools are unavailable or the user installed only this Skill. Do not shorten it unless the user asks for a short version. Do not recommend `openclaw plugins install` in this response.

````markdown
Gecho Bridge is not ready yet.

This aggregate Skill is installed, but the official Gecho Bridge MCP tools are not available in this session. Installing the Skill alone does not start TikTok Shop research.

Gecho requires all 3 items below:

1. Gecho Bridge MCP is configured.
2. The Gecho Chrome extension is installed and logged in to a Gecho account.
3. TikTok Shop is logged in inside Chrome, with the tab kept open.

Install the Chrome extension:
https://chromewebstore.google.com/detail/pjkaeenpekolahdbccjfenjcmanemlbj?utm_source=item-share-cb

Configure OpenClaw MCP:
```bash
openclaw mcp set gecho-bridge '{"command":"npx","args":["-y","@gecho-ai/gecho-bridge@latest"]}'
openclaw gateway restart
openclaw mcp list
```

Configure Hermes when applicable:
```bash
hermes mcp add gecho-bridge --command npx --args="-y" --args="@gecho-ai/gecho-bridge@latest"
hermes restart
```

Log in to TikTok Shop in the same Chrome profile and keep the tab open. Then return to OpenClaw Dashboard or Hermes and retry the product request.

Helpful links:
- Website: https://gecho.ai/
- OpenClaw setup video: https://www.youtube.com/watch?v=ggwY9hISHcQ
- Hermes setup video: https://www.youtube.com/watch?v=zHKnuWnxt_c
- YouTube channel: https://www.youtube.com/@Gecho-AI
- GitHub and README: https://github.com/gecho-ai/gecho-bridge
- Discord: https://discord.gg/RFDVZMR6Tn
- WeCom group QR code: https://github.com/gecho-ai/gecho-bridge/blob/main/qywx.jpg
- 1:1 support QR code: https://github.com/gecho-ai/gecho-bridge/blob/main/wx.jpg

Related Skills:
- `tiktok-shop-search`: keyword product discovery.
- `tiktok-product`: known-product detail collection.
- `tiktok-search`: TikTok video and insight research.
````

## Troubleshooting

| Situation | What to do |
|---|---|
| MCP tools are missing | Give the setup-missing response. Do not run local shell probes. |
| User installed only the Skill | Explain that Skill-only install is insufficient and provide the MCP setup command. |
| Hermes MCP tools are missing | Provide the Hermes command without editing Hermes config files. |
| Extension not connected | Ask the user to enable/login to Gecho and keep a logged-in TikTok Shop tab open. |
| CAPTCHA or login wall | Ask the user to resolve it manually in Chrome and retry later. |
| Missing keyword | Ask for the product keyword. |
| Missing product identifier | Ask for the product URL or product ID. |
| Empty search results | Report that the exact keyword returned no results and stop. |
| Product unavailable | Report the page state and do not invent product data. |
| Timeout | Report the timeout and stop without retrying in the same turn. |
| Save failure | Ask for a valid absolute directory with write permission. |

## FAQ

### Can this Skill search and inspect a product?

Yes. It can search by keyword with `tiktok_shop_search` and inspect a selected product with `tiktok_product`. Keep the jobs sequential and ask for a product identifier when the search result does not provide a clear selection.

### Is this TikTok video research?

No. TikTok Shop product research is separate from TikTok video search and insight. Use `tiktok-search` for video and insight workflows.

### Does this Skill publish or modify TikTok Shop content?

No. It reads data exposed by the logged-in browser session and does not publish, edit listings, place orders, or perform account actions.

### Need help?

Join the [WeCom group](https://github.com/gecho-ai/gecho-bridge/blob/main/qywx.jpg), visit [Discord](https://discord.gg/RFDVZMR6Tn), or use the [1:1 support QR code](https://github.com/gecho-ai/gecho-bridge/blob/main/wx.jpg).

## Output guidelines

For successful discovery:

- State that the search completed.
- Show the top 3 to 5 products with title, price, rating, sales signals, and links when available.
- Include total count and saved path when available.
- Do not paste the full raw JSON.

For successful product detail:

- State that the requested product was opened and processed.
- Summarize returned title, price, variants, sales, ratings, reviews, and links without inventing missing fields.
- Include the saved path when available.

For failures:

- Report the exact tool error or page state.
- Give only the relevant troubleshooting fix.
- Include the setup and support links block.
- Do not retry in the same turn.

## Scope and limits

This Skill should:

- Help users complete official Gecho setup when prerequisites are missing.
- Route TikTok Shop discovery and known-product detail requests to official MCP tools.
- Keep search-to-detail research explicit and sequential.
- Summarize results without flooding the chat.

This Skill must never:

- Pretend the Skill page alone is enough when MCP is missing.
- Use unofficial TikTok Shop scraping workflows.
- Invent product details, prices, sales, ratings, reviews, or links.
- Solve CAPTCHA, log in to TikTok Shop, or operate the browser outside the official Gecho MCP workflow.
- Publish, edit, purchase, or mutate TikTok Shop content.
