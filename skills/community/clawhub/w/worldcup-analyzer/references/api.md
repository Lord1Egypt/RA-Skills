# Football Match Analyzer API Reference

Production base URL: `https://www.jiajielitong.com`
Local dev base URL: `http://localhost:8000`
Interactive OpenAPI docs: `<base>/docs`
OpenAPI JSON: `<base>/openapi.json`
Auth header: `X-API-Key: <your_key>`

Agent Skill users can omit `SOCCER_API_KEY`; the client requests a temporary
key from `POST /matches/agent/temp-key` and uses it as `X-API-Key`. Override
the base URL with `WORLDCUP_API_BASE` when testing staging or local services.

## `POST /matches/agent/temp-key`

Request a 24-hour Agent temporary API key. No request body and no existing
API key required.

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

Rules:

- Each source IP can request one Agent temporary key per UTC day.
- The temporary key expires after 24 hours and is bound to the requesting IP.
- It includes 2 free simulation queries per day.
- Repeating the exact same home/away fixture within 3 days does not consume
  additional provider credits.
- When the temporary-key limit is reached, tell users to register or renew a
  permanent API key at `https://www.jiajielitong.com`.

## `GET /matches/epl/schedule/`

Return the provider's EPL schedule payload. Use this for EPL kickoff and
completed-result context before falling back to a neutral "not found" note.

The client wraps this in `list_epl_schedule()` with a 6-hour process-local
cache. `list_epl_teams()` infers club names from the schedule payload for
validation and fuzzy suggestions.

## `POST /matches/epl/simulate/`

Predict an English Premier League fixture.

Request body:

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `home_team` | string | yes | none | Home club, for example `"Arsenal"`. |
| `visitor_team` | string | yes | none | Away club, for example `"Chelsea"`. |
| `match_date` | string/null | no | `null` | Optional fixture date when known. |
| `season` | string | no | `"2026-27"` | Season identifier. |

Example:

```bash
curl -X POST 'https://www.jiajielitong.com/matches/epl/simulate/' \
  -H 'X-API-Key: your_key' \
  -H 'Content-Type: application/json' \
  -d '{
    "home_team": "Arsenal",
    "visitor_team": "Chelsea",
    "season": "2026-27"
  }'
```

## `GET /matches/teams/`

Return the list of supported World Cup national teams. Use this before
World Cup simulations so typos do not burn quota.

Query string:

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `competition` | string | no | `"worldcup"` | Send `"worldcup"` for national-team support. |

The API may return bilingual display labels such as `"Brazil - 巴西"`. The
client normalizes these to English team names accepted by simulations.

## `POST /matches/simulate/`

Predict a World Cup national-team matchup.

Request body:

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `home_team` | string | yes | none | Home national team, for example `"Brazil"`. |
| `visitor_team` | string | yes | none | Away national team, for example `"Morocco"`. |
| `competition` | string | no | `"worldcup"` | Send `"worldcup"`. |

Example:

```bash
curl -X POST 'https://www.jiajielitong.com/matches/simulate/' \
  -H 'X-API-Key: your_key' \
  -H 'Content-Type: application/json' \
  -d '{
    "home_team": "Brazil",
    "visitor_team": "Morocco",
    "competition": "worldcup"
  }'
```

## Prediction Response Notes

Prediction responses may be top-level `results` or nested under `data`; the
client normalizes both shapes.

```json
{
  "results": {
    "home_team": "Arsenal",
    "visitor_team": "Chelsea",
    "win_goals": 0.18,
    "win_or_not": "Win",
    "updatedAt": "2026-08-24 10:00:00"
  },
  "usage": {
    "used": 1,
    "limit": 2,
    "vip_level": "agent_temp"
  }
}
```

| Field | Meaning |
|---|---|
| `results.win_goals` | Expected goal difference, home minus away. |
| `results.win_or_not` | `"Win"`, `"Draw"`, or `"Loss"` from the home team's point of view. |
| `results.updatedAt` | Model snapshot timestamp when provided. |
| `usage.used` | Credits consumed by the current key. |
| `usage.limit` | Total finite quota; `-1` means unlimited and should never render as `-1`. |
| `usage.vip_level` | Plan tier. |

## Error Cases

- HTTP `200` with `code: 403`: auth failure, temporary-key IP mismatch, or
  quota exhausted. Surface the message and guide users to
  `https://www.jiajielitong.com`.
- HTTP `429`: rate limit; honor `Retry-After` if present.
- HTTP `5xx`: upstream issue; retry later.
- HTTP `404`: wrong path or wrong `WORLDCUP_API_BASE`.
