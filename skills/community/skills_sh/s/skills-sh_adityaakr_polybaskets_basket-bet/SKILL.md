---
name: basket-bet
description: Use when the agent needs to claim CHIP tokens and place a bet on an existing basket via vara-wallet. This is the primary agent action. Do not use for basket creation, querying, or claiming payouts.
---

# Basket Bet

Claim CHIP tokens and bet on a PolyBaskets basket via `vara-wallet`.

## Setup

**MAINNET ONLY.** Run `vara-wallet config set network mainnet` before anything else. NEVER switch to testnet — there are no contracts there. If a call fails, debug the error, do not fall back to testnet.

**Requires vara-wallet 0.10+** for hex→bytes auto-conversion. Update with: `npm install -g vara-wallet@latest`

```bash
# Ensure mainnet (default RPC)
vara-wallet config set network mainnet

BASKET_MARKET="0xea8373e8b4441ef6e95325c1044d23ebf615b43fdef60a48623836a15ca7a25a"
BET_TOKEN="0x186f6cda18fea13d9fc5969eec5a379220d6726f64c1d5f4b346e89271f917bc"
BET_LANE="0x35848dea0ab64f283497deaff93b12fe4d17649624b2cd5149f253ef372b29dc"
_PB="${POLYBASKETS_SKILLS_DIR:-skills}"
IDL="$_PB/idl/polymarket-mirror.idl"
BET_TOKEN_IDL="$_PB/idl/bet_token_client.idl"
BET_LANE_IDL="$_PB/idl/bet_lane_client.idl"
BET_QUOTE_URL="https://bet-quote-service-production.up.railway.app"
MY_ADDR=$(vara-wallet balance --account agent | jq -r .address)
VOUCHER_URL="https://voucher-backend-production-5a1b.up.railway.app/voucher"
```

## Check / Refresh Gas Voucher (hourly-tranche model)

Season 2 voucher model: each agent gets **500 VARA per hourly tranche**. A single batched POST registers the required CHIP programs and funds the voucher with 500 VARA. Do not top up just because the hourly window is open: GET voucher state first, reuse the current voucher while its known on-chain balance is at least 10 VARA, and POST again only when the voucher is missing, program coverage is incomplete, or the known balance is below 10 VARA and `canTopUpNow=true`.

**Rate limits**:
- **Per wallet**: 1 funded POST per hour. 2nd POST within the 1h window returns `429` with `Retry-After` + `retryAfterSec` — reuse the existing `voucherId`, do NOT abort.
- **Per IP**: 40 tranches per UTC day (abuse gate). Hitting the ceiling returns the same `429` shape with `Retry-After` set to seconds until next UTC midnight.

**GET is free** and read-only — always check state first before POSTing.

```bash
if [ -z "$MY_ADDR" ] || [ "$MY_ADDR" = "null" ]; then
  echo "Failed to resolve wallet address; aborting before voucher request."
  exit 1
fi
VOUCHER_STATE_URL="$VOUCHER_URL/$MY_ADDR"

# GET current voucher state — free, never rate-limited
VOUCHER_STATE=$(curl -s "$VOUCHER_STATE_URL")
VOUCHER_ID=$(echo "$VOUCHER_STATE" | jq -r .voucherId)
CAN_TOP_UP=$(echo "$VOUCHER_STATE" | jq -r .canTopUpNow)
HAS_ALL_PROGRAMS=$(echo "$VOUCHER_STATE" | jq -r \
  --arg bm "$BASKET_MARKET" --arg bt "$BET_TOKEN" --arg bl "$BET_LANE" \
  '($bm | ascii_downcase) as $bm | ($bt | ascii_downcase) as $bt | ($bl | ascii_downcase) as $bl | ((.programs // []) | map(ascii_downcase)) as $p | (($p | index($bm)) != null and ($p | index($bt)) != null and ($p | index($bl)) != null)')
VARA_BALANCE=$(echo "$VOUCHER_STATE" | jq -r .varaBalance)
BALANCE_KNOWN=$(echo "$VOUCHER_STATE" | jq -r .balanceKnown)
NEXT_ELIGIBLE=$(echo "$VOUCHER_STATE" | jq -r .nextTopUpEligibleAt)
LOW_VOUCHER_BALANCE="10000000000000" # 10 VARA in planck
NEED_TOP_UP=false
if [ "$BALANCE_KNOWN" = "true" ] && [ "$VARA_BALANCE" -lt "$LOW_VOUCHER_BALANCE" ]; then
  NEED_TOP_UP=true
fi

# POST a single batched request. Trigger when:
#   (a) no voucher yet (null), OR
#   (b) known balance is below 10 VARA and canTopUpNow=true, OR
#   (c) voucher is missing one of the required CHIP programs
if [ "$VOUCHER_ID" = "null" ] || [ "$HAS_ALL_PROGRAMS" != "true" ] || { [ "$NEED_TOP_UP" = "true" ] && [ "$CAN_TOP_UP" = "true" ]; }; then
  # ⚠ "programs" is a JSON ARRAY of contract IDs (NOT your agent address, NOT a single string).
  RESP=$(curl -s -w "\n%{http_code}" -X POST "$VOUCHER_URL" \
    -H 'Content-Type: application/json' \
    -d '{"account":"'"$MY_ADDR"'","programs":["'"$BASKET_MARKET"'","'"$BET_TOKEN"'","'"$BET_LANE"'"]}')
  HTTP_CODE=$(echo "$RESP" | tail -n1)
  BODY=$(echo "$RESP" | sed '$d')
  case "$HTTP_CODE" in
    200)
      VOUCHER_ID=$(echo "$BODY" | jq -r .voucherId)
      ;;
    429)
      RETRY_SEC=$(echo "$BODY" | jq -r .retryAfterSec)
      echo "Voucher rate-limited (next top-up in $RETRY_SEC s). Reusing existing voucherId — continue."
      # VOUCHER_ID from the initial GET remains valid; do not abort.
      ;;
    *)
      echo "Voucher POST failed: HTTP $HTTP_CODE — $BODY"
      exit 1
      ;;
  esac
fi
echo "Voucher: $VOUCHER_ID (canTopUpNow=$CAN_TOP_UP, balance=$VARA_BALANCE, known=$BALANCE_KNOWN, nextEligible=$NEXT_ELIGIBLE)"
```

**Drained-voucher STOP rule**: only trust `$VARA_BALANCE` when `BALANCE_KNOWN=true`. If `BALANCE_KNOWN=false`, the voucher backend couldn't reach the Vara node — keep going with the current voucher and do not top up solely from `CAN_TOP_UP`. When `BALANCE_KNOWN=true` AND `$VARA_BALANCE < 10000000000000` (10 VARA in planck):
- If `CAN_TOP_UP=true` → POST to top up +500 VARA and continue.
- If `CAN_TOP_UP=false` → STOP and wait until `$NEXT_ELIGIBLE` (next top-up slot). The 1h window is the minimum cadence; trying more often just returns 429.

**Migration note**: if the backend rejects your POST with an error naming the `program` field (singular), you're on an old skills copy. The API now takes `programs: string[]` (array). Re-pull the skill pack: `npx skills add Adityaakr/polybaskets -g --all`.

## CHIP Lane (Primary Path)

Most baskets use `asset_kind: "Bet"` (CHIP tokens). This is the default agent workflow.

### Step 1: Claim Hourly CHIP

Season 2 economy: agents get free CHIP tokens **once per hour**. Reward per claim = `500 + 10 × (streak_days − 1)` CHIP, capped at **600**. The streak counter advances when you claim on a new UTC calendar day — multiple hourly claims within the same UTC day do NOT raise the streak. Miss a full UTC day → streak resets to 1.

So Day 1 claims = 500 each, Day 2 = 510 each, ..., Day 11+ = 600 each.

```bash
# Get your hex address (required for actor_id args — SS58 won't work)
MY_ADDR=$(vara-wallet balance | jq -r .address)
if [ -z "$MY_ADDR" ] || [ "$MY_ADDR" = "null" ]; then
  echo "Failed to resolve wallet address; aborting before voucher request."
  exit 1
fi
VOUCHER_STATE_URL="$VOUCHER_URL/$MY_ADDR"

# Get your voucher ID (check with GET first — see Quick Start in SKILL.md)
VOUCHER_ID=$(curl -s "$VOUCHER_STATE_URL" | jq -r .voucherId)

# Check if claim is available and how much you'll get
vara-wallet call $BET_TOKEN BetToken/GetClaimPreview \
  --args '["'$MY_ADDR'"]' --idl $BET_TOKEN_IDL

# Claim hourly CHIP (do this once per hour; streak advances per UTC day)
# NOTE: --voucher is required on ALL write calls (agent has no VARA for gas)
vara-wallet --account agent call $BET_TOKEN BetToken/Claim \
  --args '[]' --voucher $VOUCHER_ID --idl $BET_TOKEN_IDL
```

The response includes your `streak_days` and `total_claimed`. Higher streak → more CHIP per claim, up to the Day 11 cap.

### Step 2: Check CHIP Balance

```bash
vara-wallet call $BET_TOKEN BetToken/BalanceOf \
  --args '["'$MY_ADDR'"]' --idl $BET_TOKEN_IDL
```

### Step 3: Pick a Basket

Browse active baskets and find one to bet on:

```bash
# How many baskets exist
vara-wallet call $BASKET_MARKET BasketMarket/GetBasketCount --args '[]' --idl $IDL

# View a specific basket
vara-wallet call $BASKET_MARKET BasketMarket/GetBasket --args '[0]' --idl $IDL
# ⚠ Response is nested under .result.ok — NOT .ok!
# Example: {"result":{"ok":{"id":0,"name":"...","status":"Active","asset_kind":"Bet",...}}}
# Use jq: | jq '.result.ok'
# To get just name and status: | jq '.result.ok | {name, status}'
```

Check that `status` is `"Active"` and `asset_kind` is `"Bet"`. The basket data is at `.result.ok` in the JSON response.

**Important:** The `basket_id` for `PlaceBet` is a plain integer (e.g., `0`, `1`, `2`), not the hex program ID.

### Step 4: Approve CHIP Spend

Allow the BetLane contract to spend your CHIP:

```bash
vara-wallet --account agent call $BET_TOKEN BetToken/Approve \
  --args '["'$BET_LANE'", <amount>]' --voucher $VOUCHER_ID --idl $BET_TOKEN_IDL
```

**Note:** Approve returns `"result":false` — this is normal, it's the previous approval state (not an error). Verify with `BetToken/Allowance` if needed.

### Step 5: Get Signed Quote + Place Bet

Bets require a signed quote from the bet-quote-service. The quote service fetches live Polymarket prices, computes the index, and signs the payload. The contract verifies the signature on-chain.

**Preferred command** (get quote + estimate gas + place bet — run together to stay within the 30-second quote expiry):

```bash
# Replace <BASKET_ID> and <AMOUNT_RAW> with real values
QUOTE=$(curl -s -X POST "$BET_QUOTE_URL/api/bet-lane/quote" \
  -H 'Content-Type: application/json' \
  -d '{"user":"'"$MY_ADDR"'","basketId":<BASKET_ID>,"amount":"<AMOUNT_RAW>","targetProgramId":"'"$BET_LANE"'"}') && \
echo "$QUOTE" | jq -e '.payload' >/dev/null 2>&1 || { echo "Quote failed: $QUOTE"; exit 1; } && \
EST=$(vara-wallet --account agent call $BET_LANE BetLane/PlaceBet \
  --args "[<BASKET_ID>, \"<AMOUNT_RAW>\", $QUOTE]" \
  --voucher $VOUCHER_ID --idl $BET_LANE_IDL --estimate) && \
GAS_LIMIT=$(node -e 'const x=JSON.parse(process.argv[1]); const used=BigInt(x.min_limit??x.minLimit??x.gas_for_reply??x.gasForReply??0); const withBuffer=used + used/5n + 5000000000n; console.log(withBuffer.toString())' "$EST") && \
vara-wallet --account agent call $BET_LANE BetLane/PlaceBet \
  --args "[<BASKET_ID>, \"<AMOUNT_RAW>\", $QUOTE]" \
  --voucher $VOUCHER_ID --gas-limit $GAS_LIMIT --idl $BET_LANE_IDL
```

**How it works:** vara-wallet 0.10+ auto-converts the hex signature (`"0x..."`) to a byte array for `vec u8` fields. No manual conversion needed — just pass the raw quote JSON from curl directly into `--args`.

**CRITICAL rules for placing bets:**
1. **Do NOT manually reconstruct the quote object.** The quote has a `{"payload": {...}, "signature": "0x..."}` structure — if you rebuild it without the `payload` wrapper, the contract will reject it with `InvalidIndexAtCreation`.
2. **Requires vara-wallet 0.10+.** Older versions need manual hex→bytes conversion. Check with `vara-wallet --version`.
3. **Always send `PlaceBet` with an explicit `--gas-limit`.** The preferred path is to estimate gas using the exact same `PlaceBet` args immediately before sending, then set `--gas-limit` to the estimate plus a buffer. Recommended baseline: `estimate * 1.2 + 5_000_000_000`.
4. **Never batch `PlaceBet` transactions blindly from one account.** Send one bet, wait for the result, then move to the next. Back-to-back writes can hit `OperationInProgress`.
5. **If you see `Message ran out of gas while executing` or `Failed to reserve gas for system signal: Ext(Execution(NotEnoughGas))`,** first query `BetLane/GetPosition` for that basket to confirm whether the state changed. Only if nothing changed should you fetch a fresh quote, increase the gas buffer, and retry once.
6. **If `OperationInProgress` persists for the same `(user, basket_id)`,** stop hammering that basket. Re-check position and quote freshness first; if the pair still looks stuck, report it instead of looping.

The quote is valid for 30 seconds. If it expires, request a new one. Each quote has a unique nonce and can only be used once.

Returns `u256` -- shares received.

### Complete CHIP Lane Example

```bash
# 0. Vars are set in the Setup block above. If starting fresh:
# MY_ADDR=$(vara-wallet balance --account agent | jq -r .address)
# VOUCHER_ID=$(curl -s "$VOUCHER_URL/$MY_ADDR" | jq -r .voucherId)

# 1. Claim hourly CHIP
vara-wallet --account agent call $BET_TOKEN BetToken/Claim \
  --args '[]' --voucher $VOUCHER_ID --idl $BET_TOKEN_IDL

# 2. Approve BetLane to spend 100 CHIP
vara-wallet --account agent call $BET_TOKEN BetToken/Approve \
  --args '["'$BET_LANE'", "100000000000000"]' --voucher $VOUCHER_ID --idl $BET_TOKEN_IDL

# 3. Get quote + estimate gas + place bet (30s expiry — run together!)
# ⚠ Do NOT manually reconstruct the quote. Pass the raw curl response directly.
QUOTE=$(curl -s -X POST "$BET_QUOTE_URL/api/bet-lane/quote" \
  -H 'Content-Type: application/json' \
  -d '{"user":"'"$MY_ADDR"'","basketId":0,"amount":"100000000000000","targetProgramId":"'"$BET_LANE"'"}') && \
EST=$(vara-wallet --account agent call $BET_LANE BetLane/PlaceBet \
  --args "[0, \"100000000000000\", $QUOTE]" \
  --voucher $VOUCHER_ID --idl $BET_LANE_IDL --estimate) && \
GAS_LIMIT=$(node -e 'const x=JSON.parse(process.argv[1]); const used=BigInt(x.min_limit??x.minLimit??x.gas_for_reply??x.gasForReply??0); const withBuffer=used + used/5n + 5000000000n; console.log(withBuffer.toString())' "$EST") && \
vara-wallet --account agent call $BET_LANE BetLane/PlaceBet \
  --args "[0, \"100000000000000\", $QUOTE]" \
  --voucher $VOUCHER_ID --gas-limit $GAS_LIMIT --idl $BET_LANE_IDL

# 5. Verify position
vara-wallet call $BET_LANE BetLane/GetPosition \
  --args '["'$MY_ADDR'", 0]' --idl $BET_LANE_IDL
```

**Important:** CHIP has 12 decimals. 100 CHIP = `100000000000000` (100 * 10^12) in raw units.

## How the Quote Works

The agent does NOT calculate `index_at_creation_bps` manually anymore. The bet-quote-service:
1. Reads the basket from chain (validates it's active + Bet kind)
2. Fetches live Polymarket prices for each outcome
3. Computes the weighted `quoted_index_bps`
4. Signs the payload with SR25519 (includes user, basket_id, amount, deadline, nonce)
5. Returns the signed quote

The BetLane contract verifies the signature on-chain. This prevents price manipulation.

**Quote properties:**
- Valid for 30 seconds (`deadline_ms`)
- One-time use (nonce prevents replay)
- Bound to specific user, basket, and amount

See `../references/index-math.md` for payout formula: `payout = shares * (settlement_index / entry_index)`.

## VARA Lane (asset_kind: Vara)

Some baskets accept native VARA instead of CHIP. Check basket's `asset_kind`.

```bash
# Bet 100 VARA on basket 0 at index 6120
vara-wallet --account agent call $BASKET_MARKET BasketMarket/BetOnBasket \
  --args '[0, 6120]' \
  --value 100 \
  --idl $IDL
```

Returns `u128` — shares received (equal to VARA sent in minimal units).

Note: VARA lane may be disabled on some deployments. Check with:
```bash
vara-wallet call $BASKET_MARKET BasketMarket/IsVaraEnabled --args '[]' --idl $IDL
```

## After Betting

Check your position (use `BetLane/GetPosition`, NOT `GetUserPositions` which doesn't exist):

```bash
vara-wallet call $BET_LANE BetLane/GetPosition \
  --args '["'$MY_ADDR'", <BASKET_ID>]' --idl $BET_LANE_IDL
```

- Wait for settlement, then claim payout: `../basket-claim/SKILL.md`
- Come back tomorrow for more CHIP: repeat Step 1

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `InvalidIndexAtCreation` | Malformed quote struct (missing `payload` wrapper) | Do NOT manually reconstruct the quote — pipe the raw curl response through python3 |
| `InvalidQuoteSignature` | Quote not signed by configured signer | Check bet-quote-service config |
| `QuoteExpired` | Quote older than 30 seconds | Request a fresh quote |
| `QuoteNonceAlreadyUsed` | Same quote submitted twice | Request a new quote for each bet |
| `QuoteTargetMismatch` | Quote was for a different BetLane | Check `targetProgramId` matches `$BET_LANE` |
| `InvalidBetAmount` | No `--value` attached (VARA lane) | Add `--value <amount>` |
| `BasketNotActive` | Basket in settlement/settled | Cannot bet on non-active baskets |
| `BasketAssetMismatch` | Wrong lane for basket | Check basket's `asset_kind` |
| `VaraDisabled` | VARA betting off | Use CHIP lane instead |
| `AmountBelowMinBet` | CHIP amount too low | Check BetLane config for min_bet |
| `AmountAboveMaxBet` | CHIP amount too high | Check BetLane config for max_bet |
| `BetTokenTransferFromFailed` | Insufficient CHIP balance or approval | Claim more tokens or increase approval |
