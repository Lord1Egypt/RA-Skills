# World Cup Analyzer API — endpoint reference

Base URL (production): `https://www.jiajielitong.com`
Base URL (local dev): `http://localhost:8000`
Interactive OpenAPI docs: `<base>/docs`
OpenAPI JSON: `<base>/openapi.json`
Auth: `X-API-Key: <your_key>` (every request)
Agent Skill users can omit `SOCCER_API_KEY`; the client requests a temporary
key from `POST /matches/agent/temp-key` and uses it as `X-API-Key`.

The default production hostname is `https://www.jiajielitong.com`.
Override via `WORLDCUP_API_BASE` env var for local dev or staging.

## `POST /matches/agent/temp-key`

Request a 24-hour Agent temporary API key. No request body and no existing
API key required.

### Response

```json
{
  "code": 200,
  "message": "Agent temporary key created. Store it securely; it is shown only once.",
  "data": {
    "api_key": "agent_tmp_...",
    "key_type": "agent_temp",
    "expires_in": 86400,
    "limit": 2,
    "used": 0,
    "remaining": 2,
    "auth_header": "X-API-Key"
  }
}
```

| Field | Meaning |
|---|---|
| `data.api_key` | Temporary key to send as `X-API-Key` for `/matches/predict/`. |
| `data.expires_in` | Seconds until expiry; currently 86400. |
| `data.limit` | Free prediction credits for the temporary key; currently 2. |
| `data.remaining` | Remaining temporary-key prediction credits. |

Rules:
- Each source IP can request one Agent temporary key per UTC day.
- The temporary key expires after 24 hours and is bound to the requesting IP.
- When the temporary-key limit is reached, tell users to register a permanent
  API key at `https://www.jiajielitong.com`.

### Curl example

```bash
curl -X POST 'https://www.jiajielitong.com/matches/agent/temp-key'
```

## `GET /matches/teams/`

Return the list of supported national teams for a competition. Use this to
validate user-supplied team names **before** calling `/matches/predict/`,
so typos don't burn prediction quota.

### Query string

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `competition` | string | ✗ | `"worldcup"` | `"worldcup"`; `"england-premium"` is reserved for future support |

### Response

```json
{
  "code": 200,
  "data": {
    "competition": "worldcup",
    "name": "FIFA World Cup 2026",
    "teams": [
      "Algeria - 阿爾及利亞",
      "Argentina - 阿根廷",
      "Brazil - 巴西",
      "...",
      "Uzbekistan - 烏茲別克"
    ],
    "count": 51
  }
}
```

The client wraps this in `list_teams(competition)` with a **12-hour
in-memory cache** (longer than the 6h predict cache, since rosters change
much less often). Pair it with `validate_team(name, competition)` which
returns `(True, canonical_name)` or `(False, fuzzy_suggestion)`.
`list_teams()` normalizes bilingual display labels such as `"Brazil - 巴西"`
to the English team names accepted by `/matches/predict/`.

### Curl example

```bash
curl -X GET 'https://www.jiajielitong.com/matches/teams/?competition=worldcup' \
  -H 'X-API-Key: your_key'
```

## `POST /matches/predict/`

Predict the outcome of a match between two national teams. The service uses
a machine learning model with player strength, coach level, club ratings,
and other factors.

### Request body (JSON)

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `home_team` | string | ✓ | — | e.g. `"Germany"`, `"Argentina"` |
| `visitor_team` | string | ✓ | — | e.g. `"France"`, `"Brazil"` |
| `competition` | string | ✗ | `"worldcup"` | `"worldcup"`; `"england-premium"` is reserved for future support |

This skill defaults `competition` to `"worldcup"` since the host project is
about the 2026 World Cup. The client always sends an explicit
`competition` value. `england-premium` is accepted by the client as a
reserved future value and should be used only after the upstream API enables
that competition.

### Response

```json
{
  "results": {
    "home_team": "Germany",
    "visitor_team": "France",
    "win_goals": -0.02,
    "win_or_not": "Loss",
    "updatedAt": "2026-06-03 17:08:18.681524"
  },
  "usage": {
    "used": 37,
    "limit": -1,
    "vip_level": "deluxe_vip"
  }
}
```

| Field | Meaning |
|---|---|
| `code` | Optional. Absent on success in current API; when present, `200` = success, `403` = auth/quota error. Treat presence of `results` as the authoritative success signal. |
| `results.win_goals` | Expected goal difference (home minus away). Positive = home advantage. May be a float (`-0.02`) or stringified float (`"0.7"`). |
| `results.win_or_not` | `"Win"` / `"Draw"` / `"Loss"`, **from the home team's POV**. |
| `results.updatedAt` | Model-snapshot timestamp. Useful as a freshness hint. |
| `usage.used` | Predictions consumed by the current key. |
| `usage.limit` | Total quota on the current plan. **`-1` means unlimited** (e.g. `deluxe_vip`); never render as `-1` to users. |
| `usage.vip_level` | Plan tier (`free`, `pro`, `deluxe_vip`, etc.). |

The provider does not consume additional credits when the exact same
home/away fixture is queried repeatedly within 3 days. Swapping `home_team`
and `visitor_team` is treated as a different fixture.

When `usage.used >= usage.limit` for a finite limit, tell users to log in at
`https://www.jiajielitong.com` to register a permanent API key.

### Curl example

```bash
curl -X POST 'https://www.jiajielitong.com/matches/predict/' \
  -H 'X-API-Key: your_key' \
  -H 'Content-Type: application/json' \
  -d '{
    "home_team": "Germany",
    "visitor_team": "France",
    "competition": "worldcup"
  }'
```

### Error cases

The API may return:

- HTTP `200` with `code: 403` — auth failure (invalid key, IP mismatch for
  an Agent temporary key) **or** quota exhausted. The error message in
  `message` / `error` distinguishes them.
- HTTP `429` — rate limit; honor `Retry-After`.
- HTTP `5xx` — upstream issue; retry with backoff.
- HTTP `404` — wrong path; verify `WORLDCUP_API_BASE`.
