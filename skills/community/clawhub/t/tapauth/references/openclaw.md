# OpenClaw Integration

TapAuth works with [OpenClaw's exec secrets provider](https://docs.openclaw.ai/gateway/secrets) to resolve fresh OAuth tokens at startup. Tokens are held in memory only — they never touch disk as plaintext config.

## How It Works

1. **One-time setup:** Run `tapauth.sh <provider> <scopes>` to create a grant and show the approval URL. The grant ID + grant secret are saved immediately in the script cache directory.
2. **Configure OpenClaw immediately:** Add one exec provider per grant with `jsonOnly: false`. Do not wait for the user to say "done." OpenClaw must use the same cache directory you used during setup, so forward `TAPAUTH_HOME` or `CLAUDE_PLUGIN_DATA` into the exec provider environment. OpenClaw then runs `tapauth.sh --token <provider> <scopes>` and waits while the user approves.
3. **Runtime:** OpenClaw resolves tokens at startup into an in-memory snapshot. `tapauth.sh --token` uses the cached grant to fetch a fresh token from the TapAuth API when OpenClaw starts.

## Prerequisites

- `tapauth.sh` with `--token` flag support (the two-step approval flow)
- An approved grant for each provider/scope combination

## Setup

### 1. Create and approve grants

```bash
export TAPAUTH_HOME="$HOME/.tapauth"

# Each command creates a grant, prints an approval URL, saves the grant metadata, and exits immediately
scripts/tapauth.sh github repo
scripts/tapauth.sh google calendar.readonly
scripts/tapauth.sh slack channels:read,channels:history
```

After showing the URL to the user, configure the provider and run `openclaw secrets reload` right away. The reload command polls through `tapauth.sh --token` until approval completes.

> **Note:** All providers require explicit scopes. Run `tapauth.sh <provider> help` or check the API error response for valid scope names.

### 2. Configure exec providers

Add to `~/.openclaw/openclaw.json`:

```json5
{
  secrets: {
    providers: {
      tapauth_github: {
        source: "exec",
        command: "/path/to/skills/tapauth/scripts/tapauth.sh",
        args: ["--token", "github", "repo"],
        passEnv: ["TAPAUTH_HOME"],
        jsonOnly: false,
      },
      tapauth_google: {
        source: "exec",
        command: "/path/to/skills/tapauth/scripts/tapauth.sh",
        args: ["--token", "google", "calendar.readonly"],
        passEnv: ["TAPAUTH_HOME"],
        jsonOnly: false,
      },
      tapauth_slack: {
        source: "exec",
        command: "/path/to/skills/tapauth/scripts/tapauth.sh",
        args: ["--token", "slack", "channels:read,channels:history"],
        passEnv: ["TAPAUTH_HOME"],
        jsonOnly: false,
      },
    },
  },
}
```

> Use the absolute path to `tapauth.sh`. If installed via ClawHub: `~/.openclaw/skills/tapauth/scripts/tapauth.sh`.
> Set `TAPAUTH_HOME` before creating grants and before starting OpenClaw so both flows see the same cache. If your environment already provides `CLAUDE_PLUGIN_DATA`, pass that instead; relying on the default `./.tapauth` only works when OpenClaw runs from the same working directory as the setup step.

### 3. Reference tokens in config

Use SecretRefs wherever the active OpenClaw schema accepts secret-bearing values. The shape is always:

```json
{ "source": "exec", "provider": "tapauth_github", "id": "value" }
```

The `id` is always `"value"` since each provider returns a single token on stdout.

## Token Lifecycle

- **Resolution:** Fresh tokens fetched at each OpenClaw activation (startup + reload).
- **Caching:** `tapauth.sh` caches grant credentials locally as soon as a grant is created. Bearer tokens are fetched on demand and are not written to disk.
- **Refresh:** Each `--token` call fetches a fresh token from the TapAuth API. TapAuth handles OAuth refresh server-side.
- **Re-approval:** If a grant is revoked or expired, rerun `tapauth.sh <provider> <scopes>` to create a new approval URL.
- **Manual reload:** `openclaw secrets reload` forces re-resolution of referenced secrets without restart.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `tapauth: cached grant is no longer usable` | Grant revoked, expired, denied, or deleted | Re-run `tapauth.sh <provider> <scopes>` to create a new approval URL, then retry OpenClaw |
| Token works locally but not in OpenClaw | OpenClaw is using a different cache directory than setup | Export `TAPAUTH_HOME` during setup and startup, then add `TAPAUTH_HOME` to `passEnv` |
| `command must be absolute path` | Relative path in `command` | Use full path: `/Users/you/.openclaw/skills/tapauth/scripts/tapauth.sh` |
| Symlink error | Homebrew or similar | Add `allowSymlinkCommand: true` and `trustedDirs` to provider config |
