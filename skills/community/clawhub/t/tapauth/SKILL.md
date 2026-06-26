---
name: tapauth
description: >-
  OAuth token provider for OpenClaw agents — Google Calendar, Gmail, GitHub, Slack, Linear, Notion,
  Vercel, Sentry, Asana, Discord, or Apify — plus user-entered passwords/API keys through the
  manual `secret` provider. Integrates with OpenClaw's exec secrets provider so values are resolved
  at startup and held in memory — no shell commands or inline credentials needed at runtime.
  Configure once in openclaw.json, reference tokens/secrets via SecretRef.
license: MIT
compatibility: Requires curl and bash. Designed for OpenClaw's exec secrets provider.
metadata:
  author: tapauth
  version: "1.0"
  website: https://tapauth.ai
  docs: https://tapauth.ai/docs
---

# TapAuth — OAuth Tokens and Manual Secrets via OpenClaw Secrets Manager

TapAuth provides OAuth tokens and user-approved manual secrets through OpenClaw's exec secrets provider. Values are resolved at gateway startup and held in memory — they never appear in shell commands or config files as plaintext.

**You must NEVER use `tapauth.sh --token` directly in shell commands, curl calls, or `$(...)` substitutions.** Tokens are always resolved through the secrets manager. Your job as an agent is to configure the secrets provider, not to fetch tokens yourself.

## When a user asks you to do something that needs an OAuth token or fixed secret

Follow these steps **in order**. Do not skip to step 3. Do not run `--token` yourself.

### 1. Create a grant and show the approval URL

Run the script **without `--token`** to create a grant. Set `TAPAUTH_HOME` so the grant cache is stored in a stable location that the exec provider can also find:

```bash
TAPAUTH_HOME=/home/node/.tapauth /home/node/.openclaw/skills/tapauth/scripts/tapauth.sh <provider> <scopes>
```

Example for Google Calendar:
```bash
TAPAUTH_HOME=/home/node/.tapauth /home/node/.openclaw/skills/tapauth/scripts/tapauth.sh google calendar.readonly
```

Example for a manual API key:
```bash
TAPAUTH_HOME=/home/node/.tapauth /home/node/.openclaw/skills/tapauth/scripts/tapauth.sh secret "Stripe Secret Key" "^sk_" "Use a Stripe secret key that starts with sk_"
```

Output:
```text
Approve access: https://tapauth.ai/approve/abc123

Show this URL to the user, then start --token immediately; it waits until approval completes.
```

**Show the approval URL to the user, then proceed immediately.** Do not ask the user to reply "done." The exec secrets provider will run `tapauth.sh --token` and wait while the user approves in the browser.

### 2. Configure the exec secrets provider in openclaw.json

Immediately after sharing the approval URL, **edit `~/.openclaw/openclaw.json`** to add an exec provider under `secrets.providers`:

```json
{
  "secrets": {
    "providers": {
      "tapauth_google_calendar": {
        "source": "exec",
        "command": "/home/node/.openclaw/skills/tapauth/scripts/tapauth.sh",
        "args": ["--token", "google", "calendar.readonly"],
        "passEnv": ["HOME"],
        "env": {"TAPAUTH_HOME": "/home/node/.tapauth"},
        "jsonOnly": false
      }
    }
  }
}
```

**Key fields:**
- **`command`**: Absolute path to `scripts/tapauth.sh` in this skill directory
- **`args`**: `["--token", "<provider>", "<scopes>"]` — must match the grant you created in step 1
- **`args` for manual secrets**: `["--token", "secret", "<description>", "<validation_regex>", "<validation_hint>"]` — description, regex, and hint must match the grant you created in step 1. Use a short, unique, stable, human-readable description because it is part of the lookup key; put formatting instructions in the hint.
- **`jsonOnly: false`**: The script outputs a raw token or secret string, not JSON
- **`passEnv`**: Must include `HOME`
- **`env.TAPAUTH_HOME`**: Must be `/home/node/.tapauth` — the same path used when creating the grant in step 1

Use the naming convention `tapauth_<provider>` or `tapauth_<provider>_<scope>` for the provider key.

Add a matching SecretRef wherever the OpenClaw config field accepts secrets for the user's task. The SecretRef must use the provider key above and `id: "value"`.

### 3. Reload secrets while the user approves

After editing `openclaw.json`, run:

```bash
openclaw secrets reload
```

This tells the gateway to re-resolve referenced secrets. When a SecretRef points at the TapAuth provider, the exec provider runs `tapauth.sh --token` in the background and stores the result in the in-memory secrets snapshot.

Run this immediately after sending the approval URL. If approval is still pending, the command waits up to 10 minutes; keep the process running or track it as a background command. Once it completes, fulfill the user's original request without requiring a separate confirmation message.

**One-time verification (optional):** Since the grant is now approved and cached, you may run the script once to verify and fulfill the user's immediate request:

```bash
TAPAUTH_HOME=/home/node/.tapauth /home/node/.openclaw/skills/tapauth/scripts/tapauth.sh --token <provider> <scopes>
```

After this, all future token access must come from the secrets manager via SecretRef — do not use `--token` directly again.

## Rules

- **NEVER run `tapauth.sh --token` directly.** Do not use it in `$(...)`, do not capture its output, do not pipe it to curl. The secrets manager runs it for you.
- **NEVER wait for a "done" reply before configuring OpenClaw.** Always create the grant first (step 1), show the URL, configure the provider, then let `openclaw secrets reload` poll while the user approves.
- **No TapAuth API key needed.** TapAuth is zero-config. Do not look for TapAuth API keys, client secrets, or environment variables.
- **Manual secrets are browser-encrypted before TapAuth receives them.** Validation regexes are checked in-browser as a UX guard; validate the retrieved secret too if format matters.
- **Manual secret expiry is TapAuth-side only.** Expiry stops TapAuth from returning the value; it does not rotate or revoke the underlying password/API key.
- **Always use absolute paths** for the `command` field in the exec provider config.

## Quick Reference — Provider + Scopes

| Provider | Args for exec provider | Scopes Reference |
|----------|----------------------|------------------|
| Google Calendar | `["--token", "google", "calendar.readonly"]` | `references/google.md` |
| Google Drive | `["--token", "google", "drive.readonly"]` | `references/google.md` |
| Google Sheets | `["--token", "google", "spreadsheets.readonly"]` | `references/google.md` |
| Gmail | `["--token", "google", "gmail.send"]` | `references/gmail.md` |
| GitHub | `["--token", "github", "repo"]` | `references/github.md` |
| Vercel | `["--token", "vercel", "deployment"]` | `references/vercel.md` |
| Notion | `["--token", "notion", "read_content"]` | `references/notion.md` |
| Slack | `["--token", "slack", "users:read"]` | `references/slack.md` |
| Asana | `["--token", "asana", "tasks:read"]` | `references/asana.md` |
| Linear | `["--token", "linear", "read"]` | `references/linear.md` |
| Sentry | `["--token", "sentry", "project:read"]` | `references/sentry.md` |
| Discord | `["--token", "discord", "identify"]` | `references/discord.md` |
| Apify | `["--token", "apify", "full_api_access"]` | `references/apify.md` |
| Manual Secret | `["--token", "secret", "Stripe Secret Key", "^sk_", "Use a Stripe secret key that starts with sk_"]` | Built in |

Multiple scopes: comma-separate in a single string, e.g. `["--token", "google", "calendar.readonly,drive.readonly"]`.

## Token Lifecycle

- **Resolution:** Fresh tokens fetched at each gateway startup and `openclaw secrets reload`.
- **Caching:** `tapauth.sh` caches grant credentials locally. Bearer tokens and approved secrets are fetched on demand and are not written to disk.
- **Refresh:** Each `--token` call fetches a fresh value from the TapAuth API. TapAuth handles OAuth refresh server-side.
- **Re-approval:** If a grant is revoked or expired, re-run `scripts/tapauth.sh <provider> <scopes>` to create or re-show an approval URL.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `tapauth: cached grant is no longer usable` | Grant revoked, denied, link-expired, or deleted | Re-run `tapauth.sh <provider> <scopes>` to create a new approval URL, then retry OpenClaw |
| Token works locally but not in OpenClaw | `passEnv` missing `HOME` | Add `HOME` to `passEnv` array |
| `command must be absolute path` | Relative path in `command` | Resolve `scripts/tapauth.sh` to its absolute path |
| Symlink error | Skill installed via symlink | Add `allowSymlinkCommand: true` and `trustedDirs` to provider config |
| `tapauth: timed out` | User did not approve within 10 minutes | Re-run `scripts/tapauth.sh <provider> <scopes>` to re-show the URL, then retry OpenClaw |
