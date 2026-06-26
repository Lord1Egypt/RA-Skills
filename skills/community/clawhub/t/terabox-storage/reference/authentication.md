# Authentication Guide

This guide covers the login authentication flow for the terabox CLI.

---

## Pre-Login Disclaimer (Mandatory)

**Regardless of the login method, the security notice and disclaimer MUST be shown to the user and their confirmation obtained before executing the login command.**

The disclaimer content is in [reference/notes.md](./notes.md).

**login.sh script (sole entry point)**: The script has built-in disclaimer display and confirmation flow. **The Agent MUST and can ONLY execute login through this script.**
- **FORBIDDEN: Agent must NOT directly call** `terabox login --get-auth-url`, `terabox login --set-code`, or any terabox login subcommand
- **FORBIDDEN: Even in GUI environments (macOS, desktop Linux), do NOT use `terabox login` to launch WebView directly**

---

## Login Method

**Mandatory: Must use the login script**

> **FORBIDDEN: Agent MUST and can ONLY execute login through login.sh script. Direct use of terabox login subcommands is strictly prohibited.**

> **FORBIDDEN: Even in GUI environments (macOS, desktop Linux), do NOT use `terabox login` to launch WebView directly.**

### Manual Authorization Code Login (OOB Mode)

```bash
bash scripts/login.sh
```

The script handles the complete login flow automatically (disclaimer → user confirmation → display authorization link → wait for user to input authorization code → complete login).

**Use cases:**
- SSH remote login (no GUI)
- Terminal does not support auto-opening browser
- Manual authorization code input required

---

## Verify Login Status

### Check Current Login Status

```bash
terabox whoami
```

**Example output:**
```
Auth Status: Logged in
Token expires: 2026-03-10 10:30:00
```

**When not logged in:**
```
Auth Status: Not logged in
Please run: bash scripts/login.sh to log in
```

---

## Logout

```bash
terabox logout
```

Clears locally stored authentication credentials (`~/.config/terabox/config.json`).

---

## FAQ

### Token Expired After Login

**Symptoms:**
```
Error: Token expired
```

**Solution:**
```bash
bash scripts/login.sh
```

### Authorization Link Invalid

**Symptoms:** Browser shows the link is invalid after opening

**Solutions:**
1. Re-run `bash scripts/login.sh` to get a new authorization link
2. Complete authorization within the link's validity period (usually 10 minutes)

### Error After Entering Authorization Code

**Symptoms:** Error reported after entering the authorization code

**Solutions:**
1. Ensure the authorization code is copied completely without extra spaces
2. Verify the code displayed in the browser matches what you entered
3. If it fails repeatedly, re-run `bash scripts/login.sh` to get a new code

> **FORBIDDEN:** All login operations above MUST be performed through `bash scripts/login.sh`. Direct use of `terabox login` is prohibited.

---

## Config File Location

```
~/.config/terabox/config.json
```

**Environment variables:**

| Variable | Description | Default |
|----------|-------------|---------|
| `XDG_CONFIG_HOME` | Base config directory (Linux/macOS) | `~/.config` |
| `APPDATA` | Base config directory (Windows) | `%USERPROFILE%\AppData\Roaming` |

Config file path: `$XDG_CONFIG_HOME/terabox/config.json` (Linux/macOS) or `%APPDATA%\terabox\config.json` (Windows).

---

## Security Notes

- **OAuth 2.0**: Uses authorization code flow, no user passwords are stored
- **Token storage**: Tokens are stored encrypted in the local config file
- **Auto-renewal**: The tool automatically refreshes tokens before expiration
- **Note**: Config file permissions are set to 600 (owner read/write only)

---

## Auto-Login Fallback Scenarios

The following scenarios will automatically switch to OOB mode:

| Scenario | Description |
|----------|-------------|
| SSH remote login | No GUI available |
| WSL environment | Limited WebView support |
| Locked desktop | WebView cannot be launched |
| No browser installed | Cannot open WebView |

When switching to OOB mode, the tool automatically displays the authorization link without user intervention.
