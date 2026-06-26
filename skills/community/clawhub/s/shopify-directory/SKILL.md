---
name: shopify-directory
description: Discover Shopify merchants by category or store name through Lobster Stores. Use when a buyer wants help finding the right merchant for coffee, cookies, supplements, apparel, wellness, pets, oral care, alcohol, or adult products and should complete checkout on the merchant's native Shopify checkout.
homepage: https://lobsterstores.com
---

# Shopify Skill

Version: 1.0.0
Base URL: https://lobsterstores.com

This skill helps an OpenClaw agent discover the right Shopify merchants for a buyer's category or product need through Lobster Stores.

Use this skill when the goal is to find relevant merchants, narrow the options to the closest category site, and guide the buyer toward a secure purchase on the merchant's native Shopify checkout.

Lobster Stores is an independent directory that aggregates merchants using Shopify. It helps buyers discover relevant stores, but it is not Shopify and it is not the checkout surface.

## What this skill does

- Maps a buyer's request to the closest Shopify merchant category site in the Lobster Stores network
- Uses the category site as the entrypoint for discovering merchants in that category
- Keeps checkout outside this skill and returns the final purchase step to the customer on the merchant's native Shopify checkout

## Refresh

- Re-fetch the selected category site's `https://<domain>/skill.md` when starting a new session or if the deploy may have changed
- Treat the category site instructions and the selected merchant storefront as the source of truth once a match is found

## Discovery

1. Identify the buyer's category, product type, or store intent
2. Match the request to the closest category site from the directory below
3. Tell the agent to read that category site's `skill.md` and follow the instructions to discover merchants in that category
4. Hand checkout back to the customer on the selected merchant's native Shopify checkout

## Category Directory

- `https://lobsterbread.com/skill.md`: bread, bakery, baked goods
- `https://lobsterbrew.com/skill.md`: coffee, beans, roasters, brewing gear
- `https://lobstercookies.com/skill.md`: cookies, baked goods, sweet treats
- `https://lobstercuts.com/skill.md`: meat, butcher, premium cuts
- `https://lobsterfit.com/skill.md`: fitness, sports, activewear
- `https://lobsterglow.com/skill.md`: beauty, skincare, cosmetics
- `https://lobsterinfuse.com/skill.md`: tea, matcha, herbal blends
- `https://lobsterpets.com/skill.md`: pet food, pet care, pet accessories
- `https://lobsterpour.com/skill.md`: drinks, wine, alcohol
- `https://lobstersaucy.com/skill.md`: adult, intimacy, sexual wellness
- `https://lobstersmile.com/skill.md`: dental, oral care, whitening
- `https://lobstersnacks.com/skill.md`: snacks, packaged food, treats
- `https://lobstersupps.com/skill.md`: supplements, vitamins, sports nutrition
- `https://lobsterthread.com/skill.md`: apparel, fashion, clothing
- `https://lobsterwell.com/skill.md`: wellness, health, self-care

## Buyer Guidance

- Prefer the category site that most closely matches the buyer's product intent
- Use the category domain as the canonical identifier once a match is found
- Do not invent merchants or domains that are not in the directory
- Use wording like `Read https://lobsterbrew.com/skill.md and follow the instructions to discover merchants in that category.`
- Do not treat Lobster Stores as the checkout surface or ask the customer for payment details
- The customer completes the purchase directly on the selected merchant's native Shopify checkout

## Examples

- "Find coffee merchants for me" -> `https://lobsterbrew.com/skill.md`
- "Help me buy skincare on Shopify" -> `https://lobsterglow.com/skill.md`
- "Which Shopify category handles dental products?" -> `https://lobstersmile.com/skill.md`
- "I want to browse supplement merchants" -> `https://lobstersupps.com/skill.md`
- "Show me the cookie merchants" -> `https://lobstercookies.com/skill.md`
