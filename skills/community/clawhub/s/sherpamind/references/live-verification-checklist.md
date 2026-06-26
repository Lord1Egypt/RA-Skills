# Live Verification Checklist

> SherpaDesk API wiki: <https://github.com/sherpadesk/api/wiki>

Use this when moving from scaffold work to real API verification.

## Verify before implementing broadly

For each endpoint we intend to rely on, capture:
- exact path used
- exact auth/header pattern that worked
- response shape actually returned
- pagination behavior
- filtering/query semantics
- timestamp/update fields available for delta sync
- whether responses are stable enough for conservative retries

## First verification order

1. authentication sanity check
2. one read-only low-volume endpoint
3. tickets list behavior
4. ticket detail behavior
5. comments/notes behavior
6. users/accounts/technicians behavior

## Recording rule

Do not leave live findings only in chat.
Write them down in this repo once verified.
