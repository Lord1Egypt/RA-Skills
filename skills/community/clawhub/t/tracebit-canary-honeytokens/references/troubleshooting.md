# Troubleshooting — Tracebit Canaries

## Table of Contents
1. [CLI Issues](#cli-issues)
2. [Authentication Problems](#authentication-problems)
3. [Deployment Issues](#deployment-issues)
4. [Canary Not Firing](#canary-not-firing)
5. [API Errors (if using API fallback)](#api-errors-if-using-api-fallback)
6. [Script Errors](#script-errors)

---

## CLI Issues

### `tracebit: command not found`

The CLI isn't installed or not in PATH.

**Fix:**
```bash
# Install the CLI
bash skills/tracebit-canaries/scripts/install-tracebit.sh

# If just installed, open a new terminal or reload PATH:
source ~/.bashrc   # or ~/.zshrc on macOS/zsh
hash -r
which tracebit
```

On macOS, if you installed the .pkg, try:
```bash
/usr/local/bin/tracebit --version
# Add to PATH if needed:
export PATH="/usr/local/bin:$PATH"
```

### `tracebit show` returns nothing or errors

**Possible causes:**
1. Not authenticated yet — run `tracebit auth`
2. No canaries deployed yet — run `tracebit deploy all`
3. Token expired — run `tracebit auth` again

### Background daemon not running (credentials expiring)

The CLI daemon keeps credentials fresh automatically. If credentials are expiring:

**Check daemon status:**
```bash
# macOS (launchd)
launchctl list | grep tracebit

# Linux (systemd)
systemctl --user status tracebit 2>/dev/null || systemctl status tracebit 2>/dev/null

# Windows
# Check Task Scheduler for a "tracebit" entry
```

**Restart daemon:**
```bash
# macOS
launchctl stop com.tracebit.daemon 2>/dev/null
tracebit deploy all   # re-deployment restarts the daemon

# Linux
systemctl --user restart tracebit 2>/dev/null

# Manual refresh (any platform)
tracebit refresh
```

### `tracebit auth` browser doesn't open

```bash
# Force browser open manually:
tracebit auth --no-browser
# Then copy the URL it prints and open it manually in a browser
```

Or paste the auth URL into any browser on any device logged into your account.

---

## Authentication Problems

### "Not authenticated" or "Unauthorized"

**Fix:**
```bash
tracebit auth
# Complete the browser OAuth flow
# Verify auth worked:
tracebit show
```

If the browser can't open automatically (headless server):
```bash
tracebit auth --no-browser
# Copy the URL it prints → open in any browser → complete OAuth → return to terminal
```

### Token stored but still failing

The token may be corrupted or expired.

**Fix:**
```bash
# Remove old token and re-auth
rm -f ~/.config/tracebit/token
tracebit auth
```

---

## Deployment Issues

### `tracebit deploy all` fails partway through

Some canary types may deploy and others fail. Check which ones succeeded:
```bash
tracebit show
```

Deploy only the failed types:
```bash
tracebit deploy aws         # retry AWS only
tracebit deploy ssh         # retry SSH only
```

### AWS canary credentials not appearing

```bash
# Verify the canary profile exists in the standard AWS credentials file
tracebit show | grep aws

# If missing, deploy manually:
tracebit deploy aws
```

### SSH canary key not appearing

```bash
# Check if the canary key was deployed
tracebit show | grep ssh

# If missing:
tracebit deploy ssh

# The CLI places the key with correct permissions (600) automatically
```

### Cookie canary not deployed (no browser available)

Cookie canaries require a browser for placement. On headless systems, deploy other types:
```bash
tracebit deploy aws
tracebit deploy ssh
tracebit deploy username-password
tracebit deploy email
```

---

## Canary Not Firing

### Triggered a canary but no alert email after 20+ minutes

**Diagnosis checklist:**

1. **Check the Tracebit dashboard first:**
   ```bash
   tracebit portal
   # or visit: community.tracebit.com → Events
   ```
   - If the alert shows there but you got no email: check spam folder, verify email address in dashboard

2. **Verify canaries are active:**
   ```bash
   tracebit show
   bash skills/tracebit-canaries/scripts/check-canaries.sh
   ```
   Expired canaries don't alert.

3. **Re-trigger with the test script:**
   ```bash
   bash skills/tracebit-canaries/scripts/test-canary.sh ssh
   # SSH is fastest: alert in ~1–3 minutes
   ```

4. **For AWS canaries specifically:** CloudTrail has 5–15 minute processing latency. Wait longer before concluding the canary didn't fire.

5. **Check spam folder** — Tracebit alerts may be filtered.

### Alert in dashboard but no email

Email settings issue:
- Go to community.tracebit.com → Settings → Notifications
- Verify your email address is correct and notifications are enabled
- Add `@tracebit.com` to your allowed senders / whitelist

---

## API Errors (if using API fallback)

See `references/api-reference.md` for API-specific error handling.

### "401 Unauthorized"

Token invalid or expired.
```bash
# Re-authenticate via CLI:
tracebit auth
# Or get a new API token from dashboard: community.tracebit.com → Settings → API Keys
```

### "429 Too Many Requests"

Rate limit hit. Do not call issue-credentials in a loop. Issue all types in one call:
```json
{"types": ["aws", "ssh"]}
```

Wait and retry with exponential backoff: 5s → 10s → 30s.

---

## Script Errors

### `jq: command not found`

```bash
# Ubuntu/Debian
sudo apt-get install -y jq

# macOS
brew install jq

# Alpine
apk add jq

# RHEL/CentOS/Fedora
sudo dnf install -y jq
```

### `python3: command not found`

The check-canaries.sh fallback and some scripts require Python 3.

```bash
# Ubuntu/Debian
sudo apt-get install -y python3

# macOS (usually pre-installed)
# If not: brew install python3
```

### `parse-tracebit-alert.sh` returns all "unknown"

The parser uses regex patterns optimized for typical Tracebit email formats. If the format differs:
1. Read the email body directly from the alert session message
2. Manually extract: canary type, name, trigger time, source IP
3. Proceed with the incident response playbook — it works regardless of whether parsing succeeds

The parsing is best-effort. A failed parse doesn't block the IR procedure.

### Scripts not executable

```bash
chmod +x skills/tracebit-canaries/scripts/*.sh
```
