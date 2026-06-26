# target-com-shopper

Unofficial skill for shopping on Target.com. Search products, check
per-store stock near a ZIP, and hand the user a one-click pre-populated
guest cart — all without logging in.

![demo](demo.webp)

## What it does / doesn't do

| ✅ Does | ❌ Does not |
| --- | --- |
| Find items that are in stock based on ZIP code | Log in to your Target account |
| Help you add items to cart | Checkout, payment, or shipping |
| Produce a one-click cart link with all your items | Solve CAPTCHAs or rate-limit bans |
| Pare down API responses to LLM-friendly shape | Touch saved carts, Circle deals, or order history |

## Install

```bash
clawhub skill install target-com-shopper
```

Requires `python3` and [`uv`](https://docs.astral.sh/uv/) on `PATH`. The
skill ships with no Python dependencies — `uv` is just used for a reproducible
venv and to run the scripts.

## Use it

In openclaw, just ask:

- *"Search Target for wireless earbuds under $50."*
- *"Is TCIN 89827259 in stock near 55403?"*
- *"Build me a Target cart link for these three items."*

The model loads the skill on its own when relevant; you can also invoke it
directly with `/target-com-shopper`.

## Important caveats

- **Unofficial.** Not affiliated with, endorsed by, or sponsored by Target
  Corporation. Trademarks belong to Target Brands, Inc.
- **Unstable endpoints.** Wraps Target's public-facing web API — public
  endpoints, not a documented API. Expect breakage.
- **No warranty on prices or stock.** Always confirm via `buy_url` before
  the user commits to a purchase.
- **Personal use only.** Don't bulk scrape or monitor prices. The in-script
  throttle (`TARGET_MIN_INTERVAL`, default 1s) is the floor.
- **Cart links contain a bearer token.** Treat them like one-time share
  links — ~24h of cart-write access to whoever holds the URL.

See [SKILL.md](SKILL.md) for the full reference, every script's usage,
environment variables, and endpoint notes.

## License

[MIT-0](LICENSE) — do whatever you want, no attribution required.
