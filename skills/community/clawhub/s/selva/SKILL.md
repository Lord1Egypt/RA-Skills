---
name: Selva
description: Shopping platform for AI agents
---

# Selva

Shopping platform for AI agents. Search, compare, and buy physical products from Amazon.

## User Experience

- Be concise and human. Do not narrate command execution unless asked.
- Prefer outcome-first messaging:
  - Good: "You’re registered. I can search now. Want me to find options for `<item>`?"
  - Avoid: "CLI installed... API key saved... next command is..."
- Ask for only the missing info needed for the next step.
- When sharing links, use friendly markdown labels when supported:
  - `[Open settings page](https://...)`
- When listing products for chat clients, send each product as a separate message with:
  - the product image as a photo attachment
  - a short caption (title, price, rating/reviews, delivery)
  - a final text message asking which item to open or buy

## Default Conversation Flow

1. **Register quietly**
   - If registration is needed, do it and confirm briefly.
2. **Check readiness**
   - If name or address is missing, ask for them naturally.
   - If card is missing and user wants to buy, offer the settings link.
3. **Search and guide**
   - Present top choices clearly (title, price, rating, delivery/get-it-by, image url, quick reason).
   - Ask a simple follow-up: "Want details on any of these?"
4. **Buy**
   - Confirm selected item and payment method.
   - If approval flow is enabled and triggered, explain next action briefly.


## Setup

1. `npx selva-cli register` — generates an API key, stored locally at ~/selva/config.json
2. `npx selva-cli settings set-name --name "Jane Doe"` — required before buying
3. `npx selva-cli settings set-address --street "123 Main St" --line2 "Apt 4B" --city "Austin" --state "TX" --zip "78701" --country "US"` — required before buying (`--line2` optional)
4. Optionally set phone: `npx selva-cli settings set-phone --phone "+14155551234"`
5. Optionally set email for purchase receipts and approval notifications: `npx selva-cli settings set-email --email "you@example.com"`
6. Link a payment card and optionally set an approval threshold at the web settings page: `npx selva-cli settings page`

# Commands

### Search
`npx selva-cli search "<query>"`
Returns up to 10 normalized results with `selva_id`, title, price, rating, source, url, `delivery_estimate` (get-it-by), and `image_url`.
When presenting search results to users, always include delivery/get-it-by text.
Prefer separate photo messages with captions (one per item) over markdown image links.
Requires address for best results but works without one.

### Details
`npx selva-cli details <selva_id>`
Returns full product details from the original provider. Use the `selva_id` from search results (e.g. `amzn_B0EXAMPLE`).

### Buy
`npx selva-cli buy <selva_id> --method <saved|card>`
Requires name, address, and a chargeable card profile. Buy creates an order record and returns its current status.
If an approval threshold is configured and the price exceeds it, the order enters `awaiting_approval` and an approval email is sent.

Options:
- `--method saved` — uses the card linked on the settings page. Fails if no card is linked - ask the user to link one.
- `--method card --number <num> --exp <MM/YY> --cvv <code>` — tokenizes with Stripe and saves a reusable payment method snapshot for later processing. Card details never reach the Selva API.

### Orders
`npx selva-cli orders`
Lists all orders with status: awaiting_approval, processing, expired, shipping.
Status meaning:
- `awaiting_approval`: waiting for user approval email click.
- `processing`: order accepted and being processed.
- `shipping`: shipping status has been updated.

### Settings
- `npx selva-cli settings` — view current name, phone, address, email, approval threshold, and linked card info
- `npx selva-cli settings page` — generates a 24-hour link to the web settings page where a human can link/remove a payment card and set an approval threshold
- `npx selva-cli settings set-address --street <street> [--line2 <line2>] --city <city> --state <state> --zip <zip> --country <country>`
- `npx selva-cli settings set-name --name <name>`
- `npx selva-cli settings set-email --email <email>`
- `npx selva-cli settings set-phone --phone <phone>`

## Product ID Format
IDs are prefixed by provider: `amzn_` for Amazon. Pass these to `details` and `buy`.


## Capability Reference

- Register user and store API key locally.
- Search products.
- Fetch product details.
- Buy by `selva_id`.
- View orders.
- Manage settings (name, phone, address, email, settings page link).

## Command Reference

- `npx selva-cli register`
- `npx selva-cli search "<query>"`
- `npx selva-cli details <selva_id>`
- `npx selva-cli buy <selva_id> --method <saved|card>`
- `npx selva-cli orders`
- `npx selva-cli settings`
- `npx selva-cli settings page`
- `npx selva-cli settings set-address --street <street> [--line2 <line2>] --city <city> --state <state> --zip <zip> --country <country>`
- `npx selva-cli settings set-name --name <name>`
- `npx selva-cli settings set-email --email <email>`
- `npx selva-cli settings set-phone --phone <phone>`
