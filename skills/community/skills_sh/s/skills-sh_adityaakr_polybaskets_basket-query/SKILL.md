---
name: basket-query
description: Use when the agent needs to read basket state, user positions, settlement status, config, or basket count from the on-chain contracts. All queries are free (no gas, no account needed). Do not use for state-changing operations.
---

# Basket Query

All queries are read-only and free — no `--account` needed.

## Setup

**MAINNET ONLY.** Run `vara-wallet config set network mainnet` before anything else. NEVER switch to testnet — there are no contracts there.

```bash
# Set network and variables (see ../references/program-ids.md)
vara-wallet config set network mainnet
BASKET_MARKET="0xea8373e8b4441ef6e95325c1044d23ebf615b43fdef60a48623836a15ca7a25a"
BET_TOKEN="0x186f6cda18fea13d9fc5969eec5a379220d6726f64c1d5f4b346e89271f917bc"
BET_LANE="0x35848dea0ab64f283497deaff93b12fe4d17649624b2cd5149f253ef372b29dc"
FREEBET_LEDGER="0x6b4ad81d13194f8e27f71f4046c6e489b2af2b0b1ce835f390899941034fd979"
_PB="${POLYBASKETS_SKILLS_DIR:-skills}"
IDL="$_PB/idl/polymarket-mirror.idl"
BET_TOKEN_IDL="$_PB/idl/bet_token_client.idl"
BET_LANE_IDL="$_PB/idl/bet_lane_client.idl"
FREEBET_LEDGER_IDL="$_PB/idl/freebet-ledger.idl"
```

## Get Your Hex Address

Sails `actor_id` args require hex format — SS58 addresses won't work:

```bash
MY_ADDR=$(vara-wallet balance | jq -r .address)
echo $MY_ADDR  # 0xe008...
```

## BasketMarket Queries

### Get basket count

```bash
vara-wallet call $BASKET_MARKET BasketMarket/GetBasketCount --args '[]' --idl $IDL
```

Returns `u64` — total baskets created. Basket IDs are 0-indexed.

### Get a basket

```bash
vara-wallet call $BASKET_MARKET BasketMarket/GetBasket --args '[0]' --idl $IDL
```

Response is nested under `.result.ok`. Parse with jq:

```bash
# ⚠ Use .result.ok — NOT .ok!
vara-wallet call $BASKET_MARKET BasketMarket/GetBasket --args '[0]' --idl $IDL | jq '.result.ok'
```

Basket fields: `id`, `creator`, `name`, `description`, `items` (array of BasketItem), `created_at`, `status` (Active/SettlementPending/Settled), `asset_kind` (Vara/Bet).

### Get user positions

```bash
vara-wallet call $BASKET_MARKET BasketMarket/GetPositions \
  --args '["'$MY_ADDR'"]' --idl $IDL
```

Returns `vec Position`. Each position has: `basket_id`, `user`, `shares`, `claimed`, `index_at_creation_bps`.

### Get native freebet positions

```bash
vara-wallet call $BASKET_MARKET BasketMarket/GetFreebetPositions \
  --args '["'$MY_ADDR'"]' --idl $IDL
```

Returns native VARA freebet positions recorded by `FreebetLedger/SpendFreebet`. Each position has the same shape as native VARA positions: `basket_id`, `user`, `shares`, `claimed`, `index_at_creation_bps`.

To check whether BasketMarket is wired to the expected ledger:

```bash
vara-wallet call $BASKET_MARKET BasketMarket/GetFreebetLedger \
  --args '[]' --idl $IDL
```

To get the agent's own address:
```bash
AGENT_ADDR=$(vara-wallet wallet list | jq -r '.[0].address')
```

### Get settlement

```bash
vara-wallet call $BASKET_MARKET BasketMarket/GetSettlement --args '[0]' --idl $IDL
```

Returns `Result<Settlement, BasketMarketError>`. Key fields: `status` (Proposed/Finalized), `payout_per_share`, `challenge_deadline`, `finalized_at`, `item_resolutions`.

### Check config

```bash
vara-wallet call $BASKET_MARKET BasketMarket/GetConfig --args '[]' --idl $IDL
```

Returns `BasketMarketConfig`: `admin_role`, `settler_role`, `liveness_ms`, `vara_enabled`, `min_items_per_basket`.

### Check VARA enabled

```bash
vara-wallet call $BASKET_MARKET BasketMarket/IsVaraEnabled --args '[]' --idl $IDL
```

Returns `bool`.

## BetToken Queries

### Check BET balance

```bash
vara-wallet call $BET_TOKEN BetToken/BalanceOf \
  --args '["'$MY_ADDR'"]' --idl $BET_TOKEN_IDL
```

### Check claim preview

```bash
vara-wallet call $BET_TOKEN BetToken/GetClaimPreview \
  --args '["'$MY_ADDR'"]' --idl $BET_TOKEN_IDL
```

Returns `ClaimPreview`: `amount`, `streak_days`, `next_claim_at`, `can_claim_now`.

### Check claim state

```bash
vara-wallet call $BET_TOKEN BetToken/GetClaimState \
  --args '["'$MY_ADDR'"]' --idl $BET_TOKEN_IDL
```

### Check token info

```bash
vara-wallet call $BET_TOKEN Metadata/Name --args '[]' --idl $BET_TOKEN_IDL
vara-wallet call $BET_TOKEN Metadata/Symbol --args '[]' --idl $BET_TOKEN_IDL
vara-wallet call $BET_TOKEN Metadata/Decimals --args '[]' --idl $BET_TOKEN_IDL
vara-wallet call $BET_TOKEN BetToken/TotalSupply --args '[]' --idl $BET_TOKEN_IDL
```

Note: `Name`, `Symbol`, `Decimals` are on the `Metadata` service, not `BetToken`.

## BetLane Queries

### Get position in BET lane

```bash
vara-wallet call $BET_LANE BetLane/GetPosition \
  --args '["0x<user_actor_id>", 0]' --idl $BET_LANE_IDL
```

Returns `Position`: `shares` (u256), `claimed`, `index_at_creation_bps`. Note: BetLane positions use `u256` shares (BET tokens), unlike BasketMarket positions which use `u128` (VARA).

### Get paginated positions

```bash
vara-wallet call $BET_LANE BetLane/GetPositions \
  --args '["0x<user_actor_id>", 0, 10]' --idl $BET_LANE_IDL
```

Args: `user`, `offset`, `limit`. Returns `Result<vec UserPositionView, BetLaneError>`.

### Check BetLane config

```bash
vara-wallet call $BET_LANE BetLane/GetConfig --args '[]' --idl $BET_LANE_IDL
```

Returns `BetLaneConfig`: `min_bet`, `max_bet`, `payouts_allowed_while_paused`.

### Check paused status

```bash
vara-wallet call $BET_LANE BetLane/IsPaused --args '[]' --idl $BET_LANE_IDL
```

## FreebetLedger Queries

### Check native VARA freebet balance

```bash
vara-wallet call $FREEBET_LEDGER FreebetLedger/BalanceOf \
  --args '["'$MY_ADDR'"]' --idl $FREEBET_LEDGER_IDL
```

Returns `u128` raw VARA units. 1 VARA = `1000000000000`.

### Check grant by id

```bash
vara-wallet call $FREEBET_LEDGER FreebetLedger/GetGrant \
  --args '["<grant_id>"]' --idl $FREEBET_LEDGER_IDL
```

### Check authorized bet program

```bash
vara-wallet call $FREEBET_LEDGER FreebetLedger/IsBetProgramAuthorized \
  --args '["'$BASKET_MARKET'"]' --idl $FREEBET_LEDGER_IDL
```

If this returns `false`, agents must not attempt `SpendFreebet`.
