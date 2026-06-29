# Runtime Status And Errors

Use this reference for authentication, environment selection, pagination, timeout, retry, cache, partial success, and normalized errors.

## Runtime Request Rules

- Skill calls only `scripts/invoke`, which calls `yeelight-home invoke --stdin`.
- Region, endpoint, credential store, pagination, timeout, and cache policy are Runtime concerns.
- The model must not set endpoint URLs, headers, operation names, retry counts, cache TTLs, or network policy.
- Reads may be paginated by Runtime. The user-facing answer should summarize the returned result, not page mechanics.
- Do not blindly retry writes. If Runtime reports uncertainty, explain `partial` or `blocked` as returned.
- After writes, trust Runtime to invalidate topology cache and re-check state when the adapter supports verification.

## Status Handling

| Runtime status | Skill behavior |
| --- | --- |
| `success` | State the actual result. |
| `partial` | State what succeeded, what did not, and any returned safe next step. |
| `clarification_required` | Ask exactly the smallest returned clarification question. |
| `confirmation_required` | Show the returned plan; wait for user confirmation before `plan.commit`. |
| `auth_required` | Tell the user to run the local QR login command; if QR is unavailable, tell them to import an approved token in their own terminal with `auth token set --stdin`; do not request secrets. |
| `blocked` | Explain the returned reason and safe alternative. |
| `not_supported` | Explain the unsupported capability without attempting raw fallback. |
| `error` | Report the redacted message and avoid guessing cause or success. |

## Runtime Missing

- If `scripts/invoke` returns `error.code=runtime_missing`, the local `yeelight-home` CLI is not available to the Skill.
- Tell the user to install `yeelight-home` from the public `yeelight/yeelight-home` release or a currently available package manager. Currently available guidance names are GitHub Releases, Homebrew, Scoop, Debian package, and npm; Winget can be mentioned only after its registry shows the package is published.
- If the user already installed the CLI in a non-PATH location, tell them to set `YEELIGHT_HOME_BIN` to the absolute executable path.
- After installation, ask the user to run `yeelight-home auth status --json`; if not logged in, use `yeelight-home auth login --qr`. If QR is unavailable, use `printf '%s' "$YEELIGHT_TOKEN" | yeelight-home auth token set --stdin --region <region>` in the user's own terminal for explicit local token import outside chat.
- Do not suggest curl, raw API calls, API keys, or external compatibility services as a workaround.

## Error Rules

- Missing credentials are handled locally with the Runtime login flow.
- Ambiguous or unknown targets should become one clarification question, not guessed IDs.
- Business failures must stay redacted; do not expose raw envelopes, identifiers, or token-like values.
- App-only, LAN-only, BLE-only, QR, pairing, or credential-sensitive flows must become Runtime guidance or blocks.
- Write verification mismatch is a partial outcome until Runtime returns a definitive state.
