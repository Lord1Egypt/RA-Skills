# Token Trading Guide

Buy, sell, and monitor tokens on superhero.com's bonding curve marketplace.

## Check Trending Tokens

```bash
node {baseDir}/scripts/superhero-trending.mjs tokens 10
```

Returns tokens sorted by trending score with: name, sale_address, price, market_cap, holders.

## Look Up a Token

```bash
node {baseDir}/scripts/superhero-token-swap.mjs lookup "TokenName"
node {baseDir}/scripts/superhero-trending.mjs token-info ct_<sale_address>
node {baseDir}/scripts/superhero-trending.mjs performance ct_<sale_address>
```

## Check Price Before Trading

```bash
node {baseDir}/scripts/superhero-token-swap.mjs price ct_<sale_address> 10
```

Returns the AE cost for buying the specified amount.

## Buy Tokens

```bash
node {baseDir}/scripts/superhero-token-swap.mjs buy ct_<sale_address> 5
```

- Automatically applies 3% slippage protection
- Requires AE for the token cost + gas

## Sell Tokens

```bash
node {baseDir}/scripts/superhero-token-swap.mjs sell ct_<sale_address> 5
```

- Automatically handles token allowance
- Applies 3% slippage protection on minimum return

## Trading Strategy (when auto-trade is enabled)

When the user has trading enabled in config, follow this loop:

1. **Check trending** — `node {baseDir}/scripts/superhero-trending.mjs tokens 20`
2. **Filter** — Only consider tokens with `trending_score` above the configured minimum
3. **Check price** — Get current price before buying
4. **Position sizing** — Never spend more than `max_trade_percent_of_balance` of wallet balance on a single trade
5. **Buy** — Execute buy for qualifying tokens
6. **Monitor** — On subsequent runs, check if held tokens are declining
7. **Sell** — If `auto_sell_on_decline` is true and a token's trending score or price drops significantly, sell the position

## Risk Management

- Always check wallet balance before trading
- Default max trade is 10% of balance per token
- Monitor P&L by comparing buy price vs current price
- The bonding curve means: price goes up as more people buy, down as they sell
