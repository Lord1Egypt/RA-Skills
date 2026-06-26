# Security Policy

## Data Handling Summary

| Data | Storage | Permissions | Lifetime |
|------|---------|-------------|----------|
| ELBA User ID | `config.json` | `0600` | Permanent (user-managed) |
| 5-digit PIN | `config.json` | `0600` | Permanent (user-managed) |
| Bearer Token | `.pw-profile/token.json` | `0600` | Ephemeral (minutes); deleted on `logout` |
| Browser Session | `.pw-profile/` | `0700` | Ephemeral; deleted on `logout` |

**Note:** The PIN alone cannot access your account. Every login requires manual 2FA approval (pushTAN) on your registered mobile device.

## Why Browser Automation?

Raiffeisen ELBA does not provide a public API for personal finance automation. The only way to programmatically retrieve account data is to:

1. Automate the browser login flow (Playwright)
2. Complete 2FA via the official pushTAN mobile app
3. Extract the Bearer token from the authenticated browser session
4. Use that token to call ELBA's internal JSON APIs

This approach is necessary but inherently sensitive. The skill implements multiple safeguards to minimize risk.

## How the Bearer Token is Extracted

The skill uses two methods to obtain the Bearer token after successful 2FA login:

1. **Primary:** Read from browser storage (`localStorage`/`sessionStorage`) using `page.evaluate()`.
2. **Fallback:** If not found in storage, the skill uses Playwright's `page.route()` to observe outgoing API requests within the same browser context and capture the `Authorization: Bearer ...` header.

This is **not** a man-in-the-middle attack — it's read-only observation of requests made by the browser the skill itself controls. No external proxy or network interception is involved. The captured token is cached locally (with `0600` permissions) to enable subsequent API calls without re-authenticating.

## Security Safeguards

### File Permissions
- **Strict umask (`0077`):** All files created by the skill are private by default.
- **Explicit hardening:** Directories use `0700`, files use `0600`.
- **Immediate application:** Permissions are set the moment files are created, not after.

### Path Restrictions
- **Output sanitization:** The `_safe_output_path()` function prevents directory traversal attacks.
- **Allowed locations:** Exported data can only be written to the workspace directory or `/tmp/`.

### Token Lifecycle
- **Short-lived:** Bearer tokens expire within minutes of inactivity.
- **Cached locally:** Stored in `.pw-profile/token.json` with `0600` permissions.
- **Cleared on logout:** The `logout` command deletes the entire `.pw-profile/` directory.

### No External Transmission
- **All network traffic goes to `*.raiffeisen.at`** — the official bank domain.
- **No telemetry, analytics, or third-party services.**

## Recommended Usage

```
login → [operations] → logout
```

Always run `logout` when finished. This ensures:
- Browser cookies are deleted
- Cached Bearer token is deleted
- No valid session state remains on disk

## Vulnerability Reporting

If you discover a security issue beyond the known architectural limitations described above, please open an issue in the skill's GitHub repository.
