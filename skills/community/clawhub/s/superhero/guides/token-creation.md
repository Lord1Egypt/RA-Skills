# Token Creation Guide

Create new bonding-curve tokens on superhero.com via the CommunityFactory contract.

## Pre-flight Checklist

Always do these before creating:

1. Check balance: `node {baseDir}/scripts/superhero-wallet.mjs balance`
2. Ask the user what token name they want (uppercase A–Z, 0–9, dash; max 20 chars)
3. Check availability: `node {baseDir}/scripts/superhero-token-create.mjs check "MYTOKEN"`
4. Ask the user: _"Do you want to buy tokens at creation? If so, how much AE?"_
5. **Tell the user**: _"Creating will take 2–5 minutes. I'll check back in up to 10 minutes once it's on-chain."_
6. **Run in background** (background terminal) then call `await_terminal` with `timeout: 600000`

## Check if Token Name is Available

```bash
node {baseDir}/scripts/superhero-token-create.mjs check "MyTokenName"
```

Returns `{ exists, allowed_name_length, allowed_chars }`. Abort if `exists: true`.

## Create a Token

```bash
node {baseDir}/scripts/superhero-token-create.mjs create "MyTokenName" 0.1
```

Parameters:

- **Name**: Token name. Uppercase A–Z, digits 0–9, dash allowed. Max 20 chars. Must be unique.
- **buy_ae**: AE to spend on an initial buy at creation (default: 0). The script sends `buy_ae * 1.05` to cover bonding curve price drift. Token count is calculated automatically from the bonding curve formula.

The collection (`WORDS-ak_...`) is fetched automatically from the Superhero API — no need to specify it.

Returns: `sale_address`, `dao_address`, `estimated_tokens`, and `tx_hash`.

## Get Token Info After Creation

```bash
node {baseDir}/scripts/superhero-token-create.mjs info ct_<sale_address>
```

Or via the trending script:

```bash
node {baseDir}/scripts/superhero-trending.mjs token-info ct_<sale_address>
```

## Cost

Token creation requires:

- Gas fee (~0.001 AE)
- Initial buy: whatever AE amount you specify (optional; 0 = no buy). The script sends `buy_ae * 1.05` as buffer for on-chain price drift.

## Contract Details

- **Factory**: `ct_25cqTw85wkF5cbcozmHHUCuybnfH9WaRZXSgEcNNXG9LsCJWTN`
- Tokens use bonding curves — price increases with supply
- Each token has a sale contract, DAO contract, and community management contract
