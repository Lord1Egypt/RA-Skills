# Stop signals

- Human verification, suspicious activity or CAPTCHA: stop immediately; never bypass.
- Login redirect or login.x.com: stop and request user login in the real browser.
- Explicit rate limit / too many requests: one backoff at the configured rhythm; repeated limit stops.
- 5xx / temporary failure / retry: transient_error, not necessarily rate limiting; one supported retry.
- Disconnected browser: retain evidence and stop after the supported bounded retry.

Localized browser labels remain recognized by Unicode escapes in code. Do not falsify successful snapshots or empty-list results when these signals occur.
