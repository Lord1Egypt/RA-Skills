# How to Run Taka CLI

## Option 1: Install from npm (Recommended)

```bash
npm install -g taka-cli
```

After installation, the `taka` command is available globally.

## Option 2: npx (No Install)

```bash
npx taka-cli --help
npx taka-cli login
npx taka-cli generate-image --prompt "sunset"
```

## Setup

### Step 1: Authenticate

```bash
taka login
```

You'll be prompted for:
1. Your email address
2. A verification code sent to that email
3. (If you have multiple businesses) Which business to use

Credentials are saved to `~/.config/taka/config.json` with restricted permissions.

### Step 2: Verify

```bash
taka whoami
```

### Step 3: Start Using

```bash
taka generate-image --prompt "a sunset over the ocean"
taka create-creative --name "My Post" --type instagram
taka list-creatives
```

## Custom Server URL

By default, Taka CLI connects to `https://api.taka.ai/v1`.

To use a different server (staging, development, self-hosted):

```bash
# Set for current session
export TAKA_SERVER_URL=https://staging.api.taka.ai/v1

# Then login (URL is saved with credentials)
taka login
```

## Token Management

Taka CLI uses JWT access/refresh tokens. Tokens auto-refresh silently when expired.

- **Access token**: Short-lived, used for API requests
- **Refresh token**: Long-lived, used to get new access tokens
- Both are stored in `~/.config/taka/config.json` (mode 0o600, owner-only)

You should rarely need to re-login. If auto-refresh fails:

```bash
taka login
```

## Logout

```bash
taka logout
```

This removes `~/.config/taka/config.json`.

## Troubleshooting

### "Not authenticated. Run taka login first."

You haven't logged in yet, or the config file was deleted.

```bash
taka login
```

### "Session expired. Run taka login to re-authenticate."

Both access and refresh tokens have expired. This is rare.

```bash
taka login
```

### "Not enough credits"

Your business has run out of generation credits. Purchase more via the Taka web app.

### "You need to create a business first"

Your account doesn't have a business yet. Create one through the Taka web app, then try `taka login` again.

### Command Not Found

```bash
# Verify installation
which taka

# If not found, reinstall
npm install -g taka-cli
```
