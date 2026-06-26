---
name: sellapp-autolist
version: 1.0.14
description: |
  Auto-creates digital products on SellApp using the v2 API. Maintains a catalog of
  6+ digital products (Notion templates, PDFs, calculators, guides) priced $17–$47.
  Runs on a schedule, checks for existing products, and creates new ones   Saves API key as SELLAPP_API_KEY in Zo settings.
compatibility: Requires Python 3, requests library, SellApp API key
metadata:
  author: ssyopros.zo.computer
  category: commerce
  display-name: SellApp Auto-Lister
  tags: sellapp, digital-products, automation, passive----
# sellapp-autolist

Auto-list digital products on SellApp via the v2 API.

## What It Does

1. Reads existing products from `GET /api/v2/products`
2. Compares against a target catalog of digital products
3. Creates any missing products via `POST /api/v2/products`
4. Sets visibility to PUBLIC

## Products in Catalog

| Product | Price | Description |
|---|---|---|
| Options Trading Brain Notion Template | $27 | Professional options trading dashboard |
| Whale Alert Scanner — Trading Journal | $37 | Track whale trades and institutional flow |
| Elliott Wave Cheat Sheet — PDF | $17 | Complete Elliott Wave rules reference |
| Iron Condor Starter Pack — Calculator | $22 | Pre-built IC calculator for SPY/QQQ |
| DeFi Sniper Bot — Setup Guide | $47 | Build a pump.fun sniper bot in 30 min |
| Freelance Code — Win Crypto Gigs | $32 | Land high-paying crypto freelance gigs |

## Script

`scripts/create_product.py` — main automation script

## Run

```bash
python scripts/create_product.py
```

## Requirements

- Python 3 + `requests`
- `SELLAPP_API_KEY` saved in Zo Settings → Advanced → Secrets
