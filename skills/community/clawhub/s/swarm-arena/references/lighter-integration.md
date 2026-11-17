# Lighter Integration — references/lighter-integration.md

Everything swarmArena relies on from Lighter, verified 2026-09 against the
live API and the `lighter-python` SDK source. Assumptions we could not verify
are flagged **[ASSUMPTION]**.

## Base URL and environment

| Item | Value |
|---|---|
| REST base URL (config `base_url` default) | `https://mainnet.zklighter.elliot.ai` |
| WebSocket (optional, unused by default) | `wss://mainnet.zklighter.elliot.ai/stream` |
| App-chain ID | `304` (auto-derived by the SDK from the URL) |
| SDK | `pip install lighter-sdk` → `import lighter` |

## REST endpoints used

| Endpoint | Auth | Notes (verified shapes) |
|---|---|---|
| `GET /api/v1/orderBookDetails` | no | `{order_book_details: [{symbol, market_id, market_type, price_decimals, size_decimals, min_base_amount, min_quote_amount, mark_price, last_trade_price, ...}]}` — amounts are **strings**. Cached 1h by the client; drives symbol → `market_id` mapping. |
| `GET /api/v1/orderBooks` | no | Lighter list variant (`order_books`), same symbol/decimals fields. |
| `GET /api/v1/candles` | no | Params `market_id`, `resolution` (`1m/5m/15m/1h/4h/1d`), `start_timestamp`, `end_timestamp`, `count_back` — all required; timestamps in **milliseconds**; ≤500 bars; zero-valued fields are **omitted**; response `{r, c: [{t,o,h,l,c,v,V,i}]}`. |
| `GET /api/v1/orderBookOrders` | no | `market_id`, `limit` → `{asks: [{price, remaining_base_amount, ...}], bids: [...]}` (strings). |
| `GET /api/v1/funding-rates` | no | `{funding_rates: [{market_id, exchange, symbol, rate}]}` — multiple exchanges per market; the client prefers `exchange == "lighter"`. |
| `GET /api/v1/recentTrades` | no | `market_id`, `limit` → `{trades: [{size, price, timestamp(ms), is_maker_ask, ask_account_id, bid_account_id, ...}]}`. |
| `GET /api/v1/accountsByL1Address` | no | `l1_address` → `{sub_accounts: [{index, ...}]}` — account discovery in onboarding. |
| `GET /api/v1/account` | token* | `by=index&value=<account_index>` → `{accounts: [{collateral, available_balance, positions: [{market_id, symbol, sign(±1), position, avg_entry_price, unrealized_pnl, ...}]}]}` (strings). *Verified readable without auth on this environment; the client still sends the token when present. |
| `GET /api/v1/accountActiveOrders` | **yes** | `account_index` (+ optional `market_id`); `Authorization` header. |
| `GET /api/v1/trades` | **yes** for accounts | `account_index`, `limit` (1–100), `sort_by` (required enum), `sort_dir`, cursor pagination. **[ASSUMPTION]** `sort_by=block_height` is used; if the venue rejects it, the client surfaces the API error cleanly. |
| `GET /api/v1/pnl` | token | `by=index&value=N&resolution=1d&start_timestamp&end_timestamp&count_back` — timestamps in **seconds** here (unlike candles); verified live. |
| `GET /api/v1/fundings` | no | funding history (available, not used by default). |
| `GET /api/v1/exchangeStats` | no | venue stats (available, not used by default). |

## SDK surface used (`lighter_signer.py`)

Verified against the installed `lighter-python` `SignerClient`:

```python
SignerClient(url=BASE_URL, account_index=ACCOUNT_INDEX,
             api_private_keys={API_KEY_INDEX: PRIVATE_KEY})   # chain_id auto: 304 here
client.create_auth_token_with_expiry(deadline=3600)          # -> (auth, err)
client.create_order(market_index, client_order_index,
                    base_amount: int, price: int, is_ask: bool,
                    order_type, time_in_force,
                    reduce_only=False, trigger_price=0, order_expiry=-1)
                    # -> (CreateOrder, RespSendTx, None) | (None, None, error)
client.cancel_order(market_index, order_index)
client.cancel_all_orders(time_in_force, timestamp_ms)
```

Constants (verified): `ORDER_TYPE_MARKET=1`, `ORDER_TYPE_STOP_LOSS=2`,
`ORDER_TYPE_TAKE_PROFIT=4`; `ORDER_TIME_IN_FORCE_IMMEDIATE_OR_CANCEL=0`;
`DEFAULT_IOC_EXPIRY=0`; `DEFAULT_28_DAY_ORDER_EXPIRY=-1`;
`NIL_TRIGGER_PRICE=0`; `CANCEL_ALL_TIF_IMMEDIATE=0`.

**[ASSUMPTION]** For STOP_LOSS / TAKE_PROFIT the wrapper sets both `price` and
`trigger_price` to the trigger level. If a future SDK version requires
`price=0` for market-style triggers, change it in one place
(`lighter_signer._create_sl/_create_tp`).

**[ASSUMPTION]** `create_order` responses are accepted when `err is None` and
`resp.code == 200` (or `code` absent). Tx-level failures surface through
`err`.

## Wire precision

Prices/sizes on the wire are integers scaled by the market's decimals:

```
to_int_price(3100.0, 2) == 310000      to_int_size(0.0010, 4) == 10
```

Helpers live in `lighter_rest_client.py`: `to_int_price`, `to_int_size`,
`from_int_price`, `from_int_size`, `floor_to_step`, `round_to_decimals`.

## Critical differences vs Binance-style APIs

1. **No leverage endpoint** — leverage is a client-side sizing cap only
   (`references/leverage-policy.md`).
2. **No isolated margin mode** — account-level cross margin; exposure caps are
   client-side plus mandatory reduce-only brackets.
3. **No income endpoint** — realized PnL derives from `/api/v1/trades` matched
   against journaled entries, or `/api/v1/pnl`.
4. **Symbols map to integer market ids** — resolved dynamically via
   `orderBookDetails` (1h cache); ids differ per environment and are never
   hardcoded.

## Retry & rate-limit policy

All REST reads retry HTTP 429 and 5xx (and transient network errors) up to 3
attempts with exponential backoff (1s → 2s → 4s), honoring `Retry-After`.
API-level error bodies (`{"code": !=200}`) raise `LighterAPIError` without
retry. Order writes are **not** retried automatically — a retried write can
double-fill; the reconciler picks the state up next cycle instead.
