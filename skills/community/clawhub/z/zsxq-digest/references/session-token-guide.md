# Session token guide

## Goal

Explain the simplest safe way to prepare `state/session.token.json` for remote-host or browserless deployments.

## Recommended file

Create:

```text
state/session.token.json
```

Keep it under a gitignored runtime directory.

## Recommended content

```json
{
  "kind": "cookie",
  "cookie_name": "zsxq_access_token",
  "cookie_value": "<paste-here>",
  "domain": ".zsxq.com",
  "source": "browser-devtools-copy",
  "captured_at": "2026-03-08T14:30:00+08:00",
  "user_agent": "optional",
  "note": "stored locally only; do not commit"
}
```

## Beginner-friendly extraction steps

### Method A: from browser cookies
1. Open the Knowledge Planet web app and log in.
2. Press `F12` to open browser devtools.
3. Open `Application` or `Storage`.
4. Open `Cookies` for `https://wx.zsxq.com`.
5. Find the cookie named `zsxq_access_token`.
6. Copy its value.
7. Paste it into `state/session.token.json` as `cookie_value`.

### Method B: from a network request
1. Open the Knowledge Planet web app and log in.
2. Press `F12` to open devtools.
3. Open the `Network` tab.
4. Refresh the page or click around once.
5. Find any request to `api.zsxq.com`.
6. In the request headers, locate `Cookie`.
7. Copy the value of `zsxq_access_token=...`.
8. Paste only the token value into `state/session.token.json`.

## Optional user-agent capture

Some token-based routes can be header-sensitive.
If needed, copy the request `User-Agent` from the same network request and store it as `user_agent`.

## Safety rules

- Never commit `state/session.token.json`.
- Never paste the token into a public issue, repo, or shared screenshot.
- If the token stops working, replace it locally instead of editing the public skill files.

## Expected errors

- `TOKEN_MISSING`: file missing or empty
- `TOKEN_INVALID`: malformed token file or cookie value
- `TOKEN_EXPIRED`: token used to work but now returns unauthorized
- `ACCESS_DENIED`: request rejected despite a present token
- `QUERY_FAILED`: unexpected response, network failure, or API shape mismatch

## MVP supported commands

The current session collector is designed around four actions:

1. `--mode groups`
   - Try to fetch the joined-group list from `/v2/groups`
2. `--mode group-topics --group-id <id>`
   - Try to fetch normalized topics from `/v2/groups/{group_id}/topics?scope=all&count=N`
3. `--mode multi-group-topics --group-id <id> --group-id <id>`
   - Fetch multiple groups in one run and merge normalized `items`
4. `--mode multi-group-topics --groups-file state/groups.json`
   - Fetch multiple groups from a local JSON array such as `["123","456"]` or `[{"group_id":"123","name":"AI圈"}]`
5. `--mode probe --url <url>`
   - Generic authenticated URL probe for debugging

## Recovery path

If token mode fails repeatedly:
1. refresh the token locally
2. retry once
3. if still failing, use browser relay mode to verify account status and page access
