---
name: wishfinity
description: Save a product from any store to a Wishfinity wishlist. Connects the Wishfinity +W MCP server, which returns a save link the user opens to finish saving. Free Wishfinity account (created when the link is opened).
metadata: {"openclaw":{"emoji":"💜","requires":{"config":["mcp.servers"]},"homepage":"https://info.wishfinity.com/integrations/overview"}}
---

# Wishfinity +W

Wishfinity +W adds one tool, `add_to_wishlist`. Give it a product page URL and it returns a link labelled **+W Save to Wishfinity**. The user opens the link to finish saving the product to their Wishfinity wishlist, where the product's name, image and price are filled in.

## Setup

**Hosted (recommended, nothing to install):**

```bash
openclaw mcp add wishfinity --url https://mcp.wishfinity.com/mcp --transport streamable-http
openclaw mcp doctor wishfinity --probe
```

Or in the Control UI: Settings → MCP → Add server → name `wishfinity`, transport **Streamable HTTP**, URL `https://mcp.wishfinity.com/mcp`.

**Local (stdio via npm):** in the Control UI, Settings → MCP → Add server → name `wishfinity`, transport **Stdio**, command `npx -y wishfinity-mcp-plusw`.

No API key or sign-in is needed to connect.

## Tool

`add_to_wishlist`
- `url` (string, required): the product page URL.
- Returns a markdown link `[+W Save to Wishfinity](<link>)` followed by JSON with the same link. If the URL doesn't look like a product page, the response includes a note.

## What it does and doesn't do

- Creates a save link. The save happens on wishfinity.com when the user opens it.
- Doesn't sign in to the user's Wishfinity account.
- Doesn't read, change or delete wishlists.

## Privacy

The server receives only the URL passed to the tool and stores nothing. Privacy policy: https://info.wishfinity.com/privacy

## Links

- Wishfinity integrations: https://info.wishfinity.com/integrations/overview
- npm: https://www.npmjs.com/package/wishfinity-mcp-plusw
- GitHub: https://github.com/wishfinity/wishfinity-mcp-plusw
- Official MCP Registry: io.github.wishfinity/wishfinity-mcp-plusw
- Support: play@wishfinity.com
