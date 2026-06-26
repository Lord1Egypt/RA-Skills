---
name: buy-it-cheaper
description: Save a personal grocery product watchlist and check nearby supermarket deals automatically by radius. Use when the user wants to track products (e.g., coffee pads), configure home location, choose radius, and set daily or weekly deal alerts with notifications.
---

# Supermarket Offer Watcher

## Overview
Use this skill to maintain a local product watchlist and run recurring nearby-offer checks across supermarket chains.

Configurable after installation:
- Home location (text)
- Radius (km)
- Product list
- Check frequency (**daily** or **weekly**)
- Check time and timezone

Default data file:
- `/data/workspace/data/supermarkt-watchlist.json`

## Quick setup

Run from the skill folder.

1) Initialize config:
```bash
python3 scripts/watchlist.py init --location "<ZIP CITY>" --radius-km 15 --mode daily --time 07:00 --tz Europe/Berlin
```

2) Add products:
```bash
python3 scripts/watchlist.py add "Senseo Coffee Pads" --aliases "Senseo Pads" --stores "REWE,EDEKA,Lidl,Aldi,Kaufland,Netto,Penny"
```

3) Inspect config:
```bash
python3 scripts/watchlist.py list
```

## Manage configuration later

Update location/radius:
```bash
python3 scripts/watchlist.py set-home --location "00001 Berlin" --radius-km 20
```

Update schedule:
```bash
# daily at 07:00
python3 scripts/watchlist.py set-schedule --mode daily --time 07:00 --tz Europe/Berlin

# weekly on monday at 07:00
python3 scripts/watchlist.py set-schedule --mode weekly --weekday monday --time 07:00 --tz Europe/Berlin
```

Remove product:
```bash
python3 scripts/watchlist.py remove "Senseo Coffee Pads"
```

## Offer-check workflow

1. Load watchlist config from `/data/workspace/data/supermarkt-watchlist.json`.
2. For each product, run 2–4 `web_search` queries (product + "offer/deal" + location + optional chain).
3. Open promising result pages using `web_fetch`.
4. Validate each hit before reporting:
   - Product (or alias) is explicit
   - Store/chain is clear
   - Date window is currently valid (today/in current week)
   - Price or discount is visible
5. Deduplicate same product/store/date combinations.
6. Send compact alert summary.

## Alert format

Use this line format per valid deal:

`✅ <Product> — <Store> — <Price/Discount> — valid until <Date> — <URL>`

If no safe deals are found, send:

`No reliable nearby offers found today.`

## Cron setup guidelines

Use `cron.add` with `sessionTarget: "isolated"` and `payload.kind: "agentTurn"`.

- Daily cron expression: `0 7 * * *`
- Weekly cron expression example (Monday): `0 7 * * 1`
- Always set timezone from config (e.g., `Europe/Berlin`).

In the cron prompt, instruct the agent to:
- read watchlist config,
- run offer checks,
- report only validated deals.
