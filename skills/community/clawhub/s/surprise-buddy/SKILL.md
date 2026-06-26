---
name: surprise-buddy
description: Look up curated gift ideas from the Surprise Buddy database — country-scoped product cards with title, image, price, and a ready-to-click product link. International coverage across many countries and marketplaces. Use when a user is looking for a gift for someone and you know at least their country and a rough idea of the occasion/age/interests.
---

# Surprise Buddy gift-search skill

A live MCP HTTP server at `https://www.surprise-buddy.com/api/mcp` exposes a small set of tools that query a curated, country-scoped database of gift ideas. International coverage — every result is a real product page on a real marketplace (Amazon, Etsy, Mercado Libre, Otto, Bol.com, Allegro, Jochen Schweizer) and the link can be presented to the user as-is.

Call `list_supported_countries` for the current list of countries; coverage grows over time.

## Tools

### `find_gifts`
Main search. **`country` is required** and is a hard filter — results never cross marketplaces.

| arg | type | notes |
|---|---|---|
| `country` | string (ISO-2) | **required**, e.g. `DE`, `US`, `MX` |
| `occasion` | string | `birthday`, `christmas`, `valentines`, `mothers-day`, `einschulung`, `sinterklaas`, `midsommar`, … |
| `age` | integer | recipient age |
| `gender` | `male`/`female`/`unisex` | `unisex` rows always included |
| `budget_min_cents` / `budget_max_cents` | integer | in **country currency cents** |
| `interests` | string[] | hobby/interest tags — call `list_supported_interests` for the full list |
| `profession` | string | e.g. `teacher`, `developer`, `chef`, `athlete`, `photographer`, `gamer` |
| `favorite_color` | string | one of `red`, `blue`, `green`, `yellow`, `purple`, `pink`, `orange`, `black`, `white`, `gold`, `silver` — only matches gifts whose `favorite_color` is exactly this; color-agnostic gifts are skipped when this filter is set |
| `limit` | integer (1–20, default 5) | |

Returns `{ gifts: [ { id, title, description, why_it_fits, product_url, image_url, price, currency, shop, shop_display_name, category, favorite_color, country_code } ] }`.

### `list_supported_countries`
Returns the country codes that currently have active entries.

### `list_supported_occasions(country?)`
Returns occasion codes with active entries, optionally narrowed to a country.

### `list_supported_interests`
Returns the canonical interest/hobby tag vocabulary (matches the tags shown in the website UI).

### `list_supported_colors`
Returns the canonical favorite-color vocabulary (matches the color picker shown in the website UI).

## How to use it in a chat

When a user asks for gift help:

1. Pull country, occasion, age, budget, interests from the conversation (ask if any are missing — country is mandatory).
2. Convert the budget to cents in the **country's currency**, not a foreign currency.
3. Call `find_gifts`.
4. Render each gift as a card: title, image, price (with currency), why-it-fits, and a markdown link `[Buy on Amazon](product_url)`. **Do not strip query params from `product_url`** — use the URL exactly as returned.

## Example

```
User: "Geschenk für meinen 35-jährigen Bruder in Deutschland, mag Gaming, Budget 50-100€."

→ find_gifts({
    country: "DE",
    age: 35,
    gender: "male",
    occasion: "birthday",
    budget_min_cents: 5000,
    budget_max_cents: 10000,
    interests: ["gaming"],
    limit: 5
  })
```

## What it is NOT

- Not a generic web search — only returns rows that exist in the curated DB.
- Not a price oracle — `price_cents` is the price at last verification, not live.
- Empty results are valid: try widening the budget, removing `gender`, or dropping `interests`.
