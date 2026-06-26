---
name: whop-digital-sales
version: 1.0.14
description: |
  Auto-create and manage digital products on Whop.com. Manages product lifecycle
  from creation to checkout link generation. Uses Whop REST API v1 with Company API key.
  Handles products, plans, and checkout links for digital product sales.
metadata:
  author: ssyopros.zo.computer
  category: digital-sales
  display-name: Whop Digital Sales
  tags: whop, digital-products, checkout-links, paid-community, api
---

# whop-digital-sales

Auto-manage digital products and checkout links on Whop.

## Whop API Setup

Base URL: `https://api.whop.com/api/v1`
Auth: `Authorization: Bearer {WHOP_API_KEY}`

**To get your API key:**
1. Go to https://sell.whop.com/developer
2. Create a Company API key
3. Save as secret `WHOP_API_KEY` in [Settings > Advanced](/?t=settings&s=advanced)

## Key Endpoints

- `POST /products` — Create product
- `GET /products` — List products  
- `POST /v2/plans` — Create plan (pricing)
- `GET /v2/plans` — List plans
- `POST /checkouts` — Create checkout link
- `GET /payments` — List payments

## Product Strategy

**Free products** → capture emails, build audience
**Paid products** → $9-99/month or $47-199 one-time
**Bundle** → free + paid ladder

## Script: `scripts/create_whop_products.py`

Creates 3 products:
1. Free community entry (email capture)
2. $19/mo AI tools access (options bot, whale scanner)
3. $199 one-time lifetime deal (all skills bundle)

## Running

```bash
python scripts/create_whop_products.py
python scripts/generate_checkout_links.py
```

## Next Steps After API Key

1. Create product with plan
2. Generate checkout link
3. Share link on Twitter/X, ClawHub, Gumroad