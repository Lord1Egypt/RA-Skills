# Mobile proxies

Two kinds, both bought with `POST /proxies` and read with `GET /proxies/{id}`:

- **Shared** (`type: "shared"`): 4G/5G mobile IPs from a pool, billed by GB for a fixed period. Exit country, city, sticky sessions and rotation are chosen after purchase, per request or per list.
- **Standard dedicated** (`type: "dedicated_standard"`): one mobile modem of the user's own in a fixed country, carrier and region, unmetered, with IP rotation on demand. (Premium dedicated proxies are dashboard-only.)

Examples assume:

```bash
API=https://dashboard.voidmob.com/api/v1; H="Authorization: Bearer $VOIDMOB_API_KEY"
```

## Plans

```bash
curl -sS -m 30 -H "$H" "$API/proxy_plans?country=us"                                         # shared only (default)
curl -sS -m 30 -H "$H" "$API/proxy_plans?type=dedicated_standard&country=us&available=true"  # dedicated in stock
curl -sS -m 30 -H "$H" "$API/proxy_plans/plan_XXXXX"                                          # refresh one quote
```

Query: `type` (`shared`, `dedicated_standard`, `all`), `country`, `min_gb`, `period` (`daily`, `weekly`, `monthly`), `available=true` and `cursor` (both need `type`), `limit`. Shared plans with `country: null` work worldwide.

Plan fields in `data.plans` (or `data.plan`): `id` (`plan_...`), `name`, `type`, `country`, `data_gb` (`null` for dedicated), `duration_days`, `period`, `quoted_price_cents` (what you pay), `available`, and for dedicated `carrier`, `region`. With `type` set, page with `data.next_cursor`.

## Buy

Show the plan and `quoted_price_cents`, get approval, then send that price as `max_price_cents` (required):

```bash
IDEM=$(uuidgen 2>/dev/null || openssl rand -hex 16); echo "Idempotency-Key: $IDEM"
curl -sS -m 60 -X POST "$API/proxies" -H "$H" -H "Content-Type: application/json" \
  -H "Idempotency-Key: $IDEM" -d '{"plan_id":"plan_XXXXX","max_price_cents":450}'
```

`202` returns `data.proxy` with `id` (`prx_...`) and `status`:

- Shared: `provisioning`, then `active` within 1-2 minutes.
- Dedicated: often `active` in the response already; otherwise `active` within about 5 minutes.
- `refunded`: provisioning failed and the charge was refunded in full.

`409 PRICE_MISMATCH` (price above your cap) and `503 SERVICE_OUT_OF_STOCK` (dedicated plan sold out) charge nothing.

## Poll until active

```bash
curl -sS -m 30 -H "$H" "$API/proxies/prx_8f6a1b2c"
```

Every 15-30 seconds (the `reads` group allows 60/min). Useful fields: `status` (`provisioning`, `active`, `expired`, `exhausted`, `refunded`), `type`, `country`, `carrier`, `data_gb_total`, `data_bytes_used` (synced every 30 minutes), `expires_at`, `auto_renew`, `next_renewal_price_cents`, `gateway`, `lists`, `rotation_url` (dedicated).

## Shared: credentials

### Gateway (one login, geo per request)

Free, idempotent, needs `Idempotency-Key`:

```bash
curl -sS -m 30 -X POST "$API/proxies/prx_8f6a1b2c/flex_credentials" -H "$H" \
  -H "Idempotency-Key: $(uuidgen 2>/dev/null || openssl rand -hex 16)"
```

`data.proxy.gateway`: `host`, `port` (10092), `protocol` (`http`), `username`, `password`. Append parameters to the username for each request:

| Suffix | Effect |
|---|---|
| (none) | New IP per request, any country |
| `_c_US` | Country, uppercase ISO code |
| `_city_New-York` | City, spaces as hyphens (use with `_c_`) |
| `_zip_10001` | Postal code (needs `_c_`) |
| `_asn_12271` | ASN |
| `_s_<id>` | Sticky session: same exit IP for the same id (expires after 60 minutes idle) |
| `_ttl_10m` | Session lifetime (`s`, `m`, `h`), with `_s_` |
| `_rotm_<n>` | On node failure: `0` rotate instantly (default), `1` after 5 s, `2` do not rotate |

Example username: `<username>_c_US_s_job1_ttl_10m`. Use a different session id per parallel worker. Suffix prefixes are case-sensitive.

Rotate the gateway password (old one stops working immediately): `POST /proxies/{id}/regenerate_password` with a new `Idempotency-Key`.

### Lists (fixed geo per login, SOCKS5 too)

```bash
curl -sS -m 30 -X POST "$API/proxies/prx_8f6a1b2c/lists" -H "$H" -H "Content-Type: application/json" \
  -H "Idempotency-Key: $(uuidgen 2>/dev/null || openssl rand -hex 16)" \
  -d '{"name":"us-ny","country":"US","region":"New York","rotation_period_seconds":0}'
```

- Geo: `country` (with optional `region`, `city`, `isp`, `zip`) or `countries` (2-30 codes, no subfilters). Discover names with `GET /geo`, `GET /geo?country=us`, `GET /geo?country=us&region=New+York`.
- `rotation_period_seconds`: `0` new IP per request, `-1` sticky, `1`-`86400` keep the IP that many seconds.
- `201` returns `data.list`: `id` (`list_...`), `credentials` (`host`, `port`, `username`, `password`) and `entries` (`login:pass@host:port`). Usable within a few minutes of creation.
- The same host, port and login work with `http://` and `socks5://`.
- Up to 100 lists per package. `GET`, `PATCH`, `DELETE /proxies/{id}/lists/{lid}`; `POST /proxies/{id}/lists/{lid}/regenerate_password`. All writes need `Idempotency-Key`.

## Using the credentials

`-U` passes the login without URL-encoding problems. In shell, write `${PUSER}_c_US`, not `$PUSER_c_US`.

```bash
curl -sS -m 30 -x "http://$PHOST:$PPORT" -U "${PUSER}_c_US:$PPASS" https://ipinfo.io/json      # gateway
curl -sS -m 30 -x "socks5h://$PHOST:$PPORT" -U "$LUSER:$LPASS" https://ipinfo.io/json         # list login, SOCKS5
```

Playwright (Node):

```js
const browser = await chromium.launch({
  proxy: { server: `http://${host}:${port}`, username: `${username}_c_US`, password },
});
```

Playwright's browsers do not accept SOCKS5 with a username and password, so use `http://` there. Inside a URL (`http://user:pass@host:port`), percent-encode the username and password.

## Dedicated: credentials and rotation

While `active`, `gateway` holds `host`, `port` (HTTP), `socks_port` (SOCKS5, or `null`), `username`, `password`. Use them as-is: no username suffixes, the location is the modem's.

```bash
curl -sS -m 30 -x "http://$PHOST:$PPORT" -U "$PUSER:$PPASS" https://ipinfo.io/json
curl -sS -m 30 -x "socks5h://$PHOST:$SOCKS_PORT" -U "$PUSER:$PPASS" https://ipinfo.io/json
```

New exit IP: `POST /proxies/{id}/rotate_ip` (no `Idempotency-Key`; each call rotates). 60-second cooldown per proxy (`429 RATE_LIMITED`); open connections drop. Do not retry automatically. `rotation_url` in the proxy object does the same without a key.

The usage, lists, flex_credentials and regenerate_password endpoints are shared-only: on a dedicated proxy `/usage` returns `404 PROXY_NOT_FOUND` and the others `409 PROXY_NOT_READY`.

## Usage, top-up, renew, auto-renew

- Live traffic (shared): `GET /proxies/{id}/usage` -> `data.usage`: `total_bytes`, `total_gb_allocated`, `remaining_bytes`, `daily_bytes`, `weekly_bytes`, `monthly_bytes`.
- Top-up (shared only, charges the balance, ask first): `POST /proxies/{id}/topup` with `{"additional_gb":5,"max_price_cents":225}` and a new `Idempotency-Key`. Price = plan price / plan GB x GB, rounded, with the user's discount. Works on `active`, `exhausted`, and `expired` less than 7 days ago.
- Renew (charges, ask first): `POST /proxies/{id}/renew` with `{"max_price_cents": <next_renewal_price_cents>}` and a new `Idempotency-Key`. Shared: adds the plan's GB and one period; allowed until 7 days after expiry. Dedicated: adds one term, only while `active`; an expired dedicated proxy cannot be renewed.
- Auto-renew (Standard dedicated only; future charges, ask first): `POST /proxies/{id}/auto_renew` with `{"enabled":true}`. Renews about 12 hours before `expires_at`.

## List orders

```bash
curl -sS -m 30 -H "$H" "$API/proxies?status=active&limit=20"
```

Filters: `status` (repeatable), `type`, `country`, `cursor`. Response `data.proxies`, `data.next_cursor`. The list is not sorted by date: to find a purchase whose response was lost, filter `status=provisioning&status=active` and page with `cursor` until `next_cursor` is `null`, comparing `created_at`.
