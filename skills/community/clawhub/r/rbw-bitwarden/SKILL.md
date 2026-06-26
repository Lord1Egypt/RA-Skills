---
name: rbw-bitwarden
description: Unofficial Bitwarden CLI written in Rust. Manage passwords, TOTP codes, and secure notes from the terminal with a background agent for stateful sessions.
version: 1.0.0
author: community
license: MIT
metadata:
  hermes:
    tags: [Password Manager, Bitwarden, CLI, Security, Vault]
    homepage: https://github.com/doy/rbw
prerequisites:
  commands: [rbw, pinentry]
---

# rbw — Unofficial Bitwarden CLI

`rbw` is a command-line client for Bitwarden that uses a background agent (`rbw-agent`) to maintain state in memory, avoiding the need to manually pass session keys around in environment variables.

## Prerequisites

- `rbw` installed (`rbw --version` to verify)
- `pinentry` installed (required for password/2FA prompts)

### Installation

```bash
# Arch Linux
sudo pacman -S rbw

# Debian/Ubuntu
sudo apt install rbw

# Fedora/RHEL
sudo dnf install rbw

# macOS
brew install rbw

# Cargo (requires pinentry)
cargo install --locked rbw
```

## Configuration

Set options via `rbw config`. Available keys:

| Key | Description | Default |
|-----|-------------|---------|
| `email` | Bitwarden account email | **Required** |
| `base_url` | Bitwarden API server URL | `https://api.bitwarden.com/` |
| `identity_url` | Identity server URL | Inferred from `base_url` or `https://identity.bitwarden.com/` |
| `ui_url` | Vault web UI URL | `https://vault.bitwarden.com/` |
| `notifications_url` | Notifications server URL | Inferred from `base_url` or `https://notifications.bitwarden.com/` |
| `lock_timeout` | Seconds to keep master keys in memory | `3600` |
| `sync_interval` | Auto-sync interval in seconds (`0` to disable) | `3600` |
| `pinentry` | Path to pinentry executable | `pinentry` |
| `sso_id` | SSO organization ID | None (regular login) |

### Example Setup

```bash
rbw config set email your@email.com
rbw config set base_url https://api.bitwarden.com/
rbw config set lock_timeout 3600
```

### Profiles

Use `RBW_PROFILE` to switch between multiple vaults (work/personal). Each profile uses separate config, local database, and agent.

```bash
RBW_PROFILE=work rbw config set email work@company.com
RBW_PROFILE=work rbw login
RBW_PROFILE=work rbw list
```

View current config:

```bash
rbw config show
```

## First-Time Setup (Official Bitwarden Server)

The official server may flag CLI traffic as bot activity. **You must register the device first** using your personal API key before normal password logins work.

1. Get your personal API key from: https://bitwarden.com/help/article/personal-api-key/
2. Register the device:

```bash
rbw register
# Enter email, then personal API key (not master password)
```

3. Log in and sync:

```bash
rbw login      # Now prompts for master password
rbw sync
```

## Daily Workflow

Most commands auto-trigger the necessary unlock/login steps. You typically don't need to run `unlock` or `login` manually before every command.

### Check Status

```bash
rbw unlocked   # Exit 0 if unlocked
rbw login      # Log in if not already
rbw unlock     # Unlock the local vault
rbw sync       # Sync local database with server
```

### List Entries

```bash
rbw list                    # Default: show names
rbw list --fields name,user # Show name + username, tab-separated
rbw list --fields id,name,user,folder
```

### Search Entries

```bash
rbw search github
rbw search "my bank" --folder Finance
```

### Get Password / Entry Details

```bash
# Get password for an entry (matches name, URI, or UUID)
rbw get github
rbw get github myusername

# Get a specific custom field
rbw get github --field "API Token"

# Get full details (password + notes)
rbw get github --full

# Output as JSON
rbw get github --raw

# Copy to clipboard
rbw get github --clipboard

# Case-insensitive match
rbw get GitHub -i
```

### Get TOTP Code

```bash
rbw code github
rbw totp github --clipboard
```

### Add a New Entry

`rbw add` opens `$VISUAL` or `$EDITOR`. The **first line** of the file becomes the password; everything after becomes the note.

```bash
rbw add "My Service" myusername --uri https://example.com --folder Personal
```

### Generate a Password

```bash
# Generate only
rbw generate 20

# Generate and save
rbw generate 20 "My Service" myusername --uri https://example.com

# No symbols
rbw generate 16 --no-symbols

# Numbers only
rbw generate 6 --only-numbers

# Avoid visually similar characters
rbw generate 20 --nonconfusables

# Diceware passphrase (LEN = number of words)
rbw generate 5 --diceware
```

### Edit an Entry

Opens the entry in `$EDITOR`. First line = password, rest = notes.

```bash
rbw edit "My Service"
rbw edit "My Service" myusername --folder Personal
```

### Remove an Entry

```bash
rbw remove "My Service"
rbw rm "My Service" myusername
```

### View Password History

```bash
rbw history "My Service"
```

### Lock / Purge

```bash
rbw lock           # Lock the vault (keep agent running)
rbw purge          # Remove local database (log out)
rbw stop-agent     # Kill the background agent
```

## SSH Agent Integration

`rbw-agent` can act as an SSH agent for signing challenges with keys stored in Bitwarden.

```bash
rbw unlock
export SSH_AUTH_SOCK="${XDG_RUNTIME_DIR}/rbw/ssh-agent-socket"
# If using a profile: ${XDG_RUNTIME_DIR}/rbw-<profile>/ssh-agent-socket
ssh git@github.com
```

## Hermes Integration Notes

- `rbw` may prompt for master password or 2FA via `pinentry`. In non-interactive contexts, ensure the agent is already unlocked (`rbw unlocked`) or use PTY mode for prompts.
- Use `--raw` for JSON output when parsing programmatically.
- Use `--clipboard` to copy secrets without printing them to stdout.
- Commands auto-cascade: `rbw get` will call `rbw unlock` if needed; `rbw sync` will call `rbw login` if needed.

## 2FA Support

Supported:
- Email
- Authenticator App (TOTP)
- Yubico OTP

**Unsupported:** WebAuthn / Passkey / Duo. If your account relies only on unsupported methods, add a supported 2FA method to use `rbw`.

## Tips

- `rbw ls` is an alias for `rbw list`
- `rbw gen` is an alias for `rbw generate`
- `rbw rm` is an alias for `rbw remove`
- `rbw totp` is an alias for `rbw code`
- Use `rbw get <uuid>` to target an exact entry by UUID
