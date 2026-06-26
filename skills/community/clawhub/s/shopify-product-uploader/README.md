# 🛍️ Shopify Product Uploader — OpenClaw Skill

Upload single products, bulk CSVs, or image-based listings to Shopify — directly from WhatsApp, Telegram, Slack, or any OpenClaw channel. Auto-generates SEO-optimised titles, descriptions, and tags in UK English.

## What it does

- **Single product upload** from a text message — just describe the product and it handles the rest
- **Bulk CSV upload** — drop a CSV, get a preview, confirm, and upload dozens of products in minutes
- **Image-to-listing** — attach a product photo and it generates a full listing from visual analysis
- **Update existing products** — change prices, add variants, update stock levels
- **Collection assignment** — automatically add products to collections

## Example usage

```
You: Upload this — Leather Bifold Wallet, £29.99, Brown/Black/Tan, 50 units each
Bot: 📦 Ready to upload:
     Title: Slim Leather Bifold Wallet | 6 Card Slots | Brown, Black & Tan
     Price: £29.99 GBP
     Variants: Brown, Black, Tan
     Tags: leather-wallet, bifold-wallet, mens-wallet, slim-wallet...
     Reply YES to upload.
You: Yes
Bot: ✅ Uploaded! https://yourstore.myshopify.com/products/slim-leather-bifold-wallet
```

## Setup

1. Create a Shopify Custom App with `write_products`, `read_products`, `write_inventory`, `write_collections` scopes
2. Copy your Admin API access token
3. Tell your OpenClaw bot: `Set my Shopify config: Store: my-store, Token: shpat_xxx`
4. Start uploading

Full setup guide: see `CONFIG.md`

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Full skill instructions and workflow logic |
| `EXAMPLES.md` | Few-shot examples for consistent output quality |
| `CONFIG.md` | Setup guide and troubleshooting |

## Compatibility

- Shopify (all plans)
- OpenClaw v0.9+
- Works with Claude, GPT-4o, and Gemini backends
- UK English output by default (configurable)

## Notes

- Image uploads require a publicly accessible URL (Shopify CDN or external)
- Bulk uploads of 100+ products respect Shopify API rate limits automatically
- All API credentials stored locally in OpenClaw memory — never sent externally

---

Built for UK e-commerce operators. Feedback welcome via ClawHub or GitHub issues.
