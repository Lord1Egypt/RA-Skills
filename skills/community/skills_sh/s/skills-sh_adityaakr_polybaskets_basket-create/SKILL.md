---
name: basket-create
description: Use when the agent needs to create a new prediction basket on-chain via vara-wallet. Do not use for betting, querying, or settlement.
---

# Basket Create

Create a new prediction basket on PolyBaskets via `vara-wallet`.

## Setup

**MAINNET ONLY.** Run `vara-wallet config set network mainnet` before anything else. NEVER switch to testnet — there are no contracts there.

```bash
vara-wallet config set network mainnet
BASKET_MARKET="0xea8373e8b4441ef6e95325c1044d23ebf615b43fdef60a48623836a15ca7a25a"
_PB="${POLYBASKETS_SKILLS_DIR:-skills}"
IDL="$_PB/idl/polymarket-mirror.idl"
```

Ensure you have a wallet and VARA for gas:

```bash
vara-wallet wallet list
vara-wallet balance
```

## Finding Polymarket Markets

Search for active markets on Polymarket to use as basket items. Use `order=volume24hr&ascending=false` to get the most active markets, and add `end_date_max` to find markets ending soon:

```bash
# Fetch high-volume markets ending within 48 hours (fastest resolution)
# end_date_min=now filters out markets that already ended (closed=false does NOT filter these!)
curl -s "https://gamma-api.polymarket.com/markets?closed=false&order=volume24hr&ascending=false&end_date_min=$(date -u +%Y-%m-%dT%H:%M:%SZ)&end_date_max=$(date -u -v+48H +%Y-%m-%dT%H:%M:%SZ)&limit=20"
# On Linux use: date -u -d '+48 hours' +%Y-%m-%dT%H:%M:%SZ

# Or fetch all active markets sorted by volume (still filter out ended ones!)
curl -s "https://gamma-api.polymarket.com/markets?closed=false&order=volume24hr&ascending=false&end_date_min=$(date -u +%Y-%m-%dT%H:%M:%SZ)&limit=20"
```

**WARNING: `closed=false` does NOT mean the market hasn't ended.** Markets past their `endDate` still appear. Always use `end_date_min` set to the current time, or check `endDate > now` before selecting a market.

Parse with jq:
```bash
# Show market id, question, YES/NO prices, and hours remaining
curl -s "https://gamma-api.polymarket.com/markets?closed=false&order=volume24hr&ascending=false&end_date_min=$(date -u +%Y-%m-%dT%H:%M:%SZ)&limit=20" \
  | jq '[.[] | {id, question, yes: (.outcomePrices | fromjson | .[0]), no: (.outcomePrices | fromjson | .[1]), endDate, liquidity}]'
```

**CRITICAL: `outcomePrices` is a JSON-encoded string**, not an array. The API returns `"[\"0.52\", \"0.48\"]"` (a string), not `["0.52", "0.48"]` (an array).
- jq: `.outcomePrices | fromjson | .[0]` for YES price
- Python: `json.loads(m['outcomePrices'])[0]`
- Node.js: `JSON.parse(m.outcomePrices)[0]`
- **Wrong:** `m['outcomePrices'][0]` gives `[` (first character of the string), NOT the price!

**Important:** `poly_market_id` is the **numeric Polymarket ID** (e.g. `"540816"`), not the hex `conditionId`. Use the `id` field from the API response.

**The `slug` field is already included in every market response.** Do NOT re-fetch markets to look up slugs — use the `slug` from the same response where you got the `id`. If you need details for a specific market ID, fetch it directly:
```bash
curl -s "https://gamma-api.polymarket.com/markets/540816"
```

## Pre-Check

Most deployments run in CHIP-only mode. Check VARA status:

```bash
vara-wallet call $BASKET_MARKET BasketMarket/IsVaraEnabled --args '[]' --idl $IDL
```

If false (typical), create a `"Bet"` basket (CHIP lane).

If the user explicitly wants to spend native VARA freebet through `FreebetLedger`, `IsVaraEnabled` must be `true` and the basket must be created with asset kind `"Vara"`. A native freebet cannot be spent on a `"Bet"` basket.

## Validation Rules

Before sending the transaction, validate locally:

| Rule | Constraint |
|------|-----------|
| Name | Non-empty, max 128 characters |
| Description | Max 512 characters |
| Items | At least `GetConfig.min_items_per_basket` (current contract default: 2), hard max 32 items |
| Weights | All `weight_bps` must sum to exactly 10000 (= 100%). Each weight is in basis points: 50% = 5000, 30% = 3000, etc. |
| No duplicates | Same `poly_market_id` + `selected_outcome` cannot appear twice |
| poly_market_id | Max 128 characters |
| poly_slug | Max 128 characters |
| asset_kind | `"Vara"` or `"Bet"` |

## Create Basket

### Arguments

```
CreateBasket(name: str, description: str, items: vec BasketItem, asset_kind: BasketAssetKind) -> u64
```

Each `BasketItem`:
```json
{
  "poly_market_id": "540816",
  "poly_slug": "will-btc-hit-100k",
  "weight_bps": 5000,
  "selected_outcome": "YES"
}
```

- `poly_market_id` — the **numeric** Polymarket ID from the API `id` field (e.g. `"540816"`), NOT the hex conditionId
- `weight_bps` — weight in basis points. 50% = 5000, 30% = 3000, etc. All weights must sum to 10000 (= 100%)

### Example: 3-item basket

```bash
vara-wallet --account agent call $BASKET_MARKET BasketMarket/CreateBasket --voucher $VOUCHER_ID \
  --args '[
    "AI Regulation Bundle",
    "Outcomes related to AI policy",
    [
      {
        "poly_market_id": "540816",
        "poly_slug": "ai-regulation-2025",
        "weight_bps": 4000,
        "selected_outcome": "YES"
      },
      {
        "poly_market_id": "540817",
        "poly_slug": "openai-ipo-2025",
        "weight_bps": 3500,
        "selected_outcome": "YES"
      },
      {
        "poly_market_id": "540818",
        "poly_slug": "eu-ai-act-enforcement",
        "weight_bps": 2500,
        "selected_outcome": "NO"
      }
    ],
    "Bet"
  ]' \
  --idl $IDL
```

Weights: 40% + 35% + 25% = 100% (4000 + 3500 + 2500 = 10000 bps).

## Parse Result

The call returns a `u64` basket ID:

```bash
RESULT=$(vara-wallet --account agent call $BASKET_MARKET BasketMarket/CreateBasket --voucher $VOUCHER_ID \
  --args '[...]' --idl $IDL)
BASKET_ID=$(echo $RESULT | jq -r '.result // .ok // .')
echo "Created basket: $BASKET_ID"
```

## After Creation

- Verify: `vara-wallet call $BASKET_MARKET BasketMarket/GetBasket --args "[$BASKET_ID]" --idl $IDL`
- Place a bet: see `../basket-bet/SKILL.md`
- Spend native VARA freebet on a `Vara` basket: see `../basket-freebet/SKILL.md`
- Share the basket ID for others to bet on

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `InvalidWeights` | Weights don't sum to 100% | Adjust weight_bps so they sum to 10000 (= 100%) |
| `NoItems` | Empty items array | Add at least 1 item |
| `NotEnoughItems` | Fewer than `min_items_per_basket` items | Add items or check `BasketMarket/GetConfig` |
| `TooManyItems` | More than 32 items | Remove items |
| `DuplicateBasketItem` | Same market+outcome twice | Remove duplicate |
| `VaraDisabled` | VARA mode off | Use `"Bet"` asset_kind instead |
| `NameTooLong` | Name > 128 chars | Shorten name |
| `DescriptionTooLong` | Description > 512 chars | Shorten description |

See `../references/error-codes.md` for all error variants.
