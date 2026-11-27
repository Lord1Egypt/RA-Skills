---
name: videxu
description: Order, make, track and download Videxu explainer videos (30-45 second videos with voiceover and captions, made from a business website) through the Videxu MCP server. Use it when the user wants a short promo or explainer video for their website or business for Reels, TikTok, Shorts or ads, or wants to check or download their Videxu videos.
---

# Videxu

Videxu turns your website or your ideas into short, on-brand, viral explainer videos with voiceover and captions for Reels, TikTok, Shorts and ads, made for you and ready to post.

## Connect

- Remote MCP server: `https://api.videxu.com/mcp` (Streamable HTTP).
- OAuth 2.1 with dynamic client registration: MCP clients that support it sign the user in to Videxu and ask them to allow access (`read`, or `read write` to make videos).
- Or an API key from https://app.videxu.com under "API, MCP & CLI", sent as `Authorization: Bearer <VIDEXU_API_KEY>`. A key is read-only unless the owner ticks "Can make videos". Keep it in the client's secret storage.
- Details: https://videxu.com/auth.md

## Tools

| Tool | Purpose |
| --- | --- |
| `get_pricing` | Current products and prices (no account needed) |
| `start_checkout` | Create a checkout link for a product; the person pays on the checkout page |
| `get_account` | Videos left and plan |
| `list_videos` | The account's videos |
| `get_video` | One video's status (making, ready or delayed) and download links |
| `make_video` | Start a video from `website`, `format` and `notes`; uses one of the videos left |

## Rules

- Always get prices from `get_pricing`; don't quote prices from memory.
- The person always pays: give them the checkout link. Never enter payment details for them. Say clearly if a plan renews monthly.
- Ask before `make_video`: each one uses one of the person's videos left. At most 10 new videos per account every 24 hours.
- With no videos left the answer is `no_videos_left`: offer the pricing and a checkout link instead.
- Ask what the video should say (offers, topics or a full script) and the language; if the person has no preference, Videxu picks topics for their niche.

## After ordering

- When a video is ready, the person gets it by email and in their account at https://app.videxu.com.
- Use `get_video` to check status and return the download links when it is ready.
- To ask for changes, the person replies to the delivery email; each video is redone once, free.

Terms: https://videxu.com/terms-of-service · Refunds: https://videxu.com/refund-policy · Privacy: https://videxu.com/privacy-policy · Support: support@videxu.com
