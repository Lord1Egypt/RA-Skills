# Selva CLI

Shopping platform CLI for AI agents. Search, inspect, and buy physical products from Amazon through a single interface.

## Quick start

1. Register an API key:

```bash
npx selva-cli register
```

2. Set name (required before buying):

```bash
npx selva-cli settings set-name --name "Jane Doe"
```

3. Set address (required before buying, `--line2` optional):

```bash
npx selva-cli settings set-address --street "123 Main St" --line2 "Apt 4B" --city "Austin" --state "TX" --zip "78701" --country "US"
```

4. Optionally set phone:

```bash
npx selva-cli settings set-phone --phone "+14155551234"
```

5. Optionally set email (for receipts and approval notifications):

```bash
npx selva-cli settings set-email --email "you@example.com"
```

6. Link a card / optionally configure approval threshold via settings page:

```bash
npx selva-cli settings page
```

## Commands

### Search

```bash
npx selva-cli search "<query>"
```

Returns up to 10 normalized results with `selva_id`, title, price, rating, source, and url.

### Details

```bash
npx selva-cli details <selva_id>
```

Returns expanded product details for a result (for example `amzn_B0EXAMPLE`).

### Buy

```bash
npx selva-cli buy <selva_id> --method <saved|card>
```

Requires name and address to be set before placing an order.
Buy creates an order record and returns current order status.

Options:

- `--method saved` uses the linked card from settings page.
- `--method card --number <num> --exp <MM/YY> --cvv <code>` tokenizes with Stripe and saves a reusable payment method snapshot for later processing.

### Orders

```bash
npx selva-cli orders
```

Lists all orders with status (`awaiting_approval`, `processing`, `expired`, `shipping`).
- `awaiting_approval`: waiting for approval email action.
- `processing`: order accepted and being processed.
- `shipping`: shipping status updated.

### Settings

- `npx selva-cli settings`
- `npx selva-cli settings page`
- `npx selva-cli settings set-address --street <street> [--line2 <line2>] --city <city> --state <state> --zip <zip> --country <country>`
- `npx selva-cli settings set-name --name <name>`
- `npx selva-cli settings set-email --email <email>`
- `npx selva-cli settings set-phone --phone <phone>`
