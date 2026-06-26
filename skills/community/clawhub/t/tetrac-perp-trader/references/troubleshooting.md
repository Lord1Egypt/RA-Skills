# Troubleshooting

A reference for every error message this CLI can produce, what causes it, and how to fix it.

> **Before retrying any failed write operation** (orders, position close, leverage, trail-watch, twap, market-maker), see the **ERROR RECOVERY PROTOCOL** in `SKILL.md`. The protocol distinguishes pre-flight failures (safe to retry) from in-flight failures (verify state first — a blind retry can place a duplicate order).

---

## Error: `Missing credentials for exchange: <name>`

**Cause:** The CLI could not find an API key and secret for the requested exchange. Neither the CLI flags nor the `.env` file contained credentials for that exchange. (API keys never live in `config.toml` — that file holds non-secret preferences only.)

**Fix:**
1. Open `.env` in the project directory
2. Add the missing credentials:
   ```env
   ORDERLY_API_KEY=your_key
   ORDERLY_API_SECRET=your_secret
   ORDERLY_API_PASSPHRASE=your_broker_id   # required for Orderly, OKX, KuCoin, Bitget, BloFin
   ```
3. Re-run the command. The `.env` is loaded automatically.

**Note on passphrase:** For Orderly, the passphrase is your broker ID (e.g. `what_exchange`, `woofi_pro`, `ttc`) — not a password. For OKX, KuCoin, Bitget, and BloFin, it is the trading passphrase you set when creating the API key. For Binance, Bybit, Phemex, Hyperliquid, and BingX no passphrase is needed.

---

## Error: `API error [401]: Unauthorized`

**Cause:** Your `TTC_AUTH_TOKEN` is expired or invalid. Tokens last exactly 24 hours from the time they were issued (`TTC_TOKEN_ISSUED_AT`).

**Fix:**
```
skill-trading login
```

If `TTC_EMAIL` and `TTC_PASSKEY` are in `.env`, this completes with no prompts. If either is missing, you will be prompted to enter them.

**Proactive check:** Before starting any session, check token age:
```bash
issued=$(grep TTC_TOKEN_ISSUED_AT .env | cut -d= -f2)
age=$(( $(date +%s) - issued ))
echo "Token age: ${age}s / 86400s"
```
If age > 86400, run `skill-trading login` before doing anything else.

---

## Error: `API error [400]: ...tick size...` or `...price precision...`

**Cause:** Your order price does not match the exchange's minimum tick size for that symbol. For example, Orderly may require prices to be rounded to 4 decimal places, and you submitted a price with more precision or at the wrong increment.

**Fix:**
1. Fetch the current bid/ask to observe the required precision:
   ```
   skill-trading market best-bid-ask -e <exchange> --symbol <SYMBOL>
   ```
2. Round your price to the same number of decimal places as the bid/ask prices you see.
3. Resubmit the order.

**Example:** If best bid is `1.1710` and best ask is `1.1712`, the tick size is `0.0001`. Your price must be a multiple of `0.0001`.

---

## Error: `API error [400]: ...quantity...` or `...lot size...`

**Cause:** Your order quantity does not match the exchange's minimum lot size for that symbol.

**Fix:** Same as above — observe the quantity precision in the `best-bid-ask` output and round your quantity to match.

---

## Error: `API error [400]: ...insufficient balance...` or `...margin...`

**Cause:** Your available balance is not enough to cover the required margin for the order.

**Fix:**
1. Run `skill-trading account balance` and check the `Available` field.
2. Recalculate: `required_margin = (quantity × price) / leverage`
3. Reduce quantity until `required_margin ≤ available`
4. Or close an existing position to free margin

---

## Error: `API error [403]: Forbidden`

**Cause:** The method name sent to TTC Box is incorrect. This is a known quirk — `getOpenOrders` returns 403. The correct method name is `getOrders`.

This error should not appear in normal use since the CLI uses the correct method names. If you see it, something in the request body was malformed.

**Fix:** File a bug report. Capture the full command and output.

---

## Error: `API error [429]: Too Many Requests` or `Rate limited - retry after N seconds`

**Cause:** You have made too many requests in a short window. The CLI automatically retries up to 3 times with increasing delays.

**Fix:** Wait the number of seconds indicated, then retry. If this happens frequently, add a short pause between commands in automated workflows.

---

## Balance shows `0.0000` or `-0.0000` on Orderly

**Cause:** Your `ORDERLY_MAIN_WALLET_ADDRESS` is missing or incorrect. This is the most common issue for email-registered CLI users.

When you registered via email (using `skill-trading register`), TTC Box assigned a random keypair to your account. But Orderly needs to know your *actual* trading wallet address to look up your funds. Without this env var, the server looks at the wrong wallet.

**Fix:**
1. Find your Orderly trading wallet address (the public key of the wallet where your Orderly funds are held — a base58 Solana address, about 44 characters)
2. Add to `.env`:
   ```env
   ORDERLY_MAIN_WALLET_ADDRESS=GgUWyS5rsH4...
   ```
3. Run `skill-trading account balance` again

**Web3 users are not affected.** If you registered via the TTC Box web interface with a wallet, your `TTC_PUBLIC_KEY` is already your Orderly wallet.

---

## Error: `Position not found: <SYMBOL>`

**Cause:** You tried to close, modify, or read a position that does not exist on this exchange for this symbol.

**Fix:**
1. Run `skill-trading position get` to see all open positions and their exact symbol names
2. Symbol names are case-sensitive and exchange-specific. `BTCUSDT` on one exchange may not match another.
3. Retry with the exact symbol shown in the position list.

---

## Error: `Configuration error: ...`

**Cause:** Something is wrong with `config.toml` — malformed TOML, missing required field, or wrong file path.

**Fix:**
1. Check the path: by default the CLI looks for `./config.toml` in the current directory, then `~/Library/Application Support/com.ttcbox.skill-trading/config.toml` on macOS.
2. You can specify the path explicitly: `skill-trading --config /path/to/config.toml <command>`
3. Validate your TOML at https://www.toml-lint.com or delete `config.toml` entirely — it is optional. All credentials can come from `.env`.

---

## Error: `Invalid order parameters: ...`

**Cause:** One or more order fields failed validation before the request was sent. Common causes:
- `--buy` and `--sell` both specified (or neither)
- Negative or zero quantity or price
- `--stop-price` missing from a stop order
- `--tp-price` missing from a take-profit order

**Fix:** Read the error message for the specific field name. Correct the argument and retry.

---

## Login prompt appears even though TTC_EMAIL and TTC_PASSKEY are set

**Cause:** The `.env` file may not be in the current working directory, or the variable names have a typo.

**Fix:**
1. Verify you are in the directory that contains `.env`:
   ```bash
   ls .env
   ```
2. Check the exact variable names:
   ```bash
   grep -E "TTC_EMAIL|TTC_PASSKEY" .env
   ```
3. Make sure there are no spaces around the `=` sign in `.env`

---

## `skill-trading: command not found`

**Cause:** The binary is not in PATH.

**Fix:**
```bash
make release
make install     # installs to /usr/local/bin/skill-trading
```

Or add the binary location to PATH manually:
```bash
export PATH="$PATH:/usr/local/bin"
```

---

## Market data commands work but exchange commands fail

**Cause:** Market data commands (`hybrid-tickers`, `funding-rates`, `open-interest`, `volume-snapshot`, `scanner`) do not require exchange credentials — they hit TTC Box aggregation endpoints directly. Exchange-specific commands (`account balance`, `order limit`, etc.) require both a valid TTC session AND exchange API credentials.

**Fix:** Verify that:
1. `TTC_AUTH_TOKEN` is valid (run `skill-trading login` if unsure)
2. `{EXCHANGE}_API_KEY` and `{EXCHANGE}_API_SECRET` are set in `.env`
3. For Orderly: `ORDERLY_API_PASSPHRASE` and `ORDERLY_MAIN_WALLET_ADDRESS` are set (email-registered users)
