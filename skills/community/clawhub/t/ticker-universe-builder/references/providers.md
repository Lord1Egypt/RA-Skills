# Optional public-data adapters

`fetch` is an optional standard-library adapter. It writes evidence and bars, never a selected
universe. `build`, `validate`, `maintain`, `measure` and `evaluate` do not access the network.

```bash
python scripts/universe.py fetch --market cn --prices-until 2026-09-28 \
  --limit 1250 --workers 6 --output temp/cn
```

Use the latest completed trading day, not today's incomplete bar. Supported adapters: `us`, `jp`,
`cn`, `kr`, `hk`, `uk`, `crypto`; other registered markets accept externally researched snapshots.
`--include-watchlist old.txt` includes incumbent equities in the research requests if still present
in the eligible listing inventory. It does not preserve unverified symbols or select members.

Equities use the public TradingView scanner for observed primary listings and provider industry
labels; Yahoo supplies adjusted daily closes. The history bench includes the largest `--limit`
companies by observed market cap, three representatives per industry and requested incumbents.
CN retains active CNY A/H dual listings even if the provider marks the H-share as globally primary.
Daily turnover is **raw close × volume**, a proxy rather than exchange-reported notional. UK GBp
is converted to GBP for turnover; returns use adjusted prices. Currency and provider symbols are
recorded. Quote activity does not certify regulatory status, disclosure quality or investability.
CN excludes ST/delisting name flags; this does not replace exchange-level regulatory research.

Crypto uses official Binance Spot and USDⓈ-M contract inventories, product tags and daily klines.
USDT perpetual is preferred only if history passes; spot is the fallback. Product tags identify
broad groups and require review. Stablecoins, leveraged products, monitoring-tagged assets and
tokenised stocks/commodities are outside this adapter's operating-asset bench. It requires 180
effective bars, a continuous final 30-day window and at least $1m 30-day mean quoted turnover.
Perpetual matching uses the exact provider base asset; multiplier contracts need a separately
verified mapping. This is a disclosed research floor, not a universal selection threshold; new listings require a
separate event research route. Untagged and perpetual-only assets are outside this adapter's scope.

To research beyond the default spot-linked bench, use `--crypto-scope all-perpetuals --limit 1000`.
This also admits active USDT perpetuals whose official `exchangeInfo.underlyingSubType` identifies
an economic category. Aliases normalize DeFi, Layer-1/2, Storage, Payment and PoW to the product-tag
vocabulary; marketing labels Alpha, Crypto and Chinese alone do not establish a theme. The
classification source remains `exchangeInfo`, not the product endpoint. TradFi/index/cross-pair
contracts and product exclusions remain out; possible multiplier/spot duplicates await separate
identity verification. Identical history and liquidity gates apply. This is broader Binance
coverage, not a complete multi-exchange digital-asset universe.

Outputs:

- `listings.json`: observed inventory, date, provider classification and exact TradingView ticker.
- `prices.csv`: completed daily bars with adjusted close and turnover.
- `manifest.json`: requested/received counts, exclusions/errors, source URLs, mapping, conventions
  and SHA-256 of the price table. `complete=false` means requests did not all succeed.
- `raw/*.json`: URL/body, acquisition timestamp, response hash and raw response.

Exit 2 means a partial result; inspect it before research. The successful subset may support an
explicitly scoped snapshot, but must not be described as a complete screen. A failed history is
never assigned invented metrics. Cache reuse requires the exact request and the same UTC
acquisition date; older responses are refreshed and failure is reported instead of relabelled.
Raw data stays in the chosen output directory. Do not commit or redistribute provider histories;
check applicable source terms before wider use. Public endpoints are replaceable and may change.

## Recovery and input checks

Requests make at most three attempts for transient transport, truncated/invalid JSON and server
errors. HTTP 400/401/403/404 need source or request repair, not repeated identical requests.
Failures leave `raw/*.error.json` with request identity, dates and attempt errors; a subsequent
successful request clears its current error receipt. No failed response becomes a fresh cache.
If urllib encounters transport/decoding failures and system `curl` is already installed, remaining
attempts may use it with HTTPS verification and the same explicit CA settings. The total remains
three attempts; curl is optional and never installed by the skill. Receipts name `transport`;
`sha256` hashes the response bytes returned by that transport (curl decompresses them).
No shell is invoked. Without curl, failures remain resumable partial results.
Responses are read incrementally; equity inventory uses smaller pages. Compressed responses
are decoded before JSON parsing. Yahoo history must match the requested
provider symbol and market currency, with aligned timestamp/price/volume arrays; share-class
symbols keep their complete filenames. A failed Yahoo host may use the other public Yahoo host,
with the actual URL recorded. This does not guarantee endpoint availability.

TLS verification stays enabled. Python uses its configured trust store; on macOS a certificate
verification failure may retry against `/etc/ssl/cert.pem`, unless an explicit SSL_CERT_FILE or
SSL_CERT_DIR was supplied. For another trust store, set SSL_CERT_FILE to a verified CA bundle.
Never use an unverified SSL context. After these attempts, inspect the manifest and research a
verified alternative; retain its exact instrument, units, cutoff and raw receipts before measure.
For CN alternative feeds, establish share-versus-lot volume units per instrument; do not assume
one multiplier for the entire response population.
