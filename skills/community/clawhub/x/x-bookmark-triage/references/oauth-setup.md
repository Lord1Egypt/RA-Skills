# OAuth 2.0 Setup — x-bookmark-triage

## 1. Create an X Developer App

1. Go to [developer.x.com](https://developer.x.com) → Projects & Apps → New App
2. Select **User Authentication Settings**
3. Enable **OAuth 2.0**
4. Set **App permissions**: Read + Write (for unbookmark; Read-only if you skip unbookmark)
5. Set **Callback URL**: `http://localhost:3456/callback` (the authorize script uses this port)
6. Set **Organization URL**: required — must be a real URL you control (e.g., your website)
7. Save — copy **Client ID** and **Client Secret**

## 2. Required Scopes

| Scope | Required for |
|-------|-------------|
| `bookmark.read` | Reading bookmarks |
| `bookmark.write` | Deleting bookmarks (unbookmark feature) |
| `users.read` | Getting your user ID |
| `offline.access` | Refresh tokens (required for background operation) |
| `tweet.read` | Reading tweet content |

If you only want read + triage (no unbookmark), you can omit `bookmark.write`.

## 3. Run the Auth Flow

```bash
X_OAUTH2_CLIENT_ID=<your-client-id> \
X_OAUTH2_CLIENT_SECRET=<your-client-secret> \
node scripts/x-oauth2-authorize.js
```

The script:
1. Opens `https://x.com/i/oauth2/authorize?...` in your browser
2. Starts a local HTTP server on port 3456
3. Captures the callback with `code`
4. Exchanges for access + refresh tokens
5. Saves to `data/x-oauth2-token-cache.json`

## 4. Store Credentials

**For launchd / production:**
Add to your gateway plist `EnvironmentVariables`:
```xml
<key>X_OAUTH2_CLIENT_ID</key><string>YOUR_CLIENT_ID</string>
<key>X_OAUTH2_CLIENT_SECRET</key><string>YOUR_CLIENT_SECRET</string>
<key>X_OAUTH2_REFRESH_TOKEN</key><string>YOUR_REFRESH_TOKEN</string>
```

**For local testing:**
```bash
export X_OAUTH2_CLIENT_ID=...
export X_OAUTH2_CLIENT_SECRET=...
export X_OAUTH2_REFRESH_TOKEN=...
```

## 5. Refresh Token Rotation

X rotates refresh tokens on each use. This is expected behavior.

The scripts detect rotation and:
- Save the new token to `data/x-oauth2-new-refresh-token.txt`
- Print a warning: `⚠️ Refresh token rotated — update X_OAUTH2_REFRESH_TOKEN in plist`

**You must update `X_OAUTH2_REFRESH_TOKEN` in your env after each rotation**, or the next run will fail auth. Automating this requires writing back to your secrets store — see `references/adapting.md` for patterns.

## 6. Testing

```bash
# Verify auth works
node -e "
const {spawnSync} = require('child_process');
const r = spawnSync('curl', ['-s', 'https://api.x.com/2/users/me', '-H', 'Authorization: Bearer ' + process.env.X_OAUTH2_REFRESH_TOKEN]);
console.log(r.stdout.toString());
"

# Or dry-run the sweep
node scripts/backlog-sweep.js --dry-run --limit 5
```
