# Strava API (quick reference)

This skill uses Strava’s official OAuth2 + API v3.

## OAuth

- Authorize: `https://www.strava.com/oauth/authorize`
- Token: `https://www.strava.com/oauth/token`

Common scope:
- `activity:read_all`

## Common endpoint

List athlete activities (supports pagination):
- `GET https://www.strava.com/api/v3/athlete/activities`
  - Query params: `after` (epoch seconds), `before` (epoch seconds), `page`, `per_page`

List detailed activity:
- `GET https://www.strava.com/api/v3/activities/{id}`

Notes:
- Strava tokens include `expires_at` (epoch seconds) + `refresh_token`.
