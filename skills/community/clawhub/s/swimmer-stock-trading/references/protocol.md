# Solana USDC route discovery and memo protocol

Use only the fixed no-key origin `https://api.sharesdao.com:8443` for public discovery. Never ask the user to configure the base URL.

## Fetch pools and tradable stocks

```http
POST https://api.sharesdao.com:8443/pool/list
Content-Type: application/json

{"start_index":0,"num_of_pools":500}
```

Paginate until a page is shorter than requested. Keep only records whose persisted `blockchain` is `2` (Solana). For each ticker, call:

```http
GET https://api.sharesdao.com:8443/router/{STOCK}/SOLANA
```

Keep only exact routes `USDC-{STOCK}s` and `{STOCK}s-USDC` containing canonical USDC and stock mint addresses. Exclude SOL-settled, EVM, unrelated issuer, legacy `.S`, and malformed routes. An HTTP success with application status `Fail` is unavailable. Pool and route responses are discovery input, not independent proof of token identity or custody; compare the stock mint against the protected, independently verified allowlist before use.

## Optional market estimate

Only if the user explicitly asks, call:

```http
GET https://api.sharesdao.com:8443/router/{STOCK}/SOLANA/{PAIR}/quote?offer_amount={DISPLAY_AMOUNT}
```

Treat the response as an estimate, not a minimum or guarantee. MARKET does not require a quote and normally uses raw request `"0"`. LIMIT never calls quote. Neither order type calls `/router/swap` or downloads a transaction.

## Memo

The signer creates this compact public JSON from the confirmed plan:

```json
{"did_id":"<WALLET>","type":"MARKET_OR_LIMIT","offer":"<RAW>","request":"<RAW_OR_0>","token_address":"<TRUSTED_STOCK_MINT>","customer_id":"SVIM","trade_source":"SVIM","currency":"USDC"}
```

For BUY, the transferred mint is canonical Solana USDC. For SELL, it is the trusted stock mint. A LIMIT’s offer/request ratio represents its requested price. The transaction contains exactly one classic SPL Token Program transfer to the internally fixed recipient followed by one Memo Program instruction. The signer obtains a fresh blockhash only after confirmation.
