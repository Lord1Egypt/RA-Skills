# ymailink Configuration Reference

Configuration file location: `~/.config/ymailink/config.toml`

Multiple config files can be merged with the `-c` flag (later files override earlier ones):
```bash
ymailink -c base.toml -c overrides.toml mail list
```

> **Table of Contents**
> - [Minimal IMAP + SMTP Setup](#minimal-imap--smtp-setup)
> - [Encryption Options](#encryption-options)
> - [Password Options](#password-options)
> - [Outlook (Microsoft Graph API)](#outlook-configuration-microsoft-graph-api)
> - [Gmail (Google API)](#gmail-configuration-google-api)
> - [Exchange Configuration](#exchange-configuration)
> - [Gmail via IMAP (App Password)](#gmail-via-imap-app-password)
> - [Folder Aliases](#folder-aliases)
> - [Multiple Accounts](#multiple-accounts)
> - [Additional Options](#additional-options) (Signature, Downloads, Editor, Proxy)
> - [OAuth2 Token Management](#oauth2-token-management)
> - [AI Configuration](#ai-configuration)

## Minimal IMAP + SMTP Setup

```toml
[accounts.default]
email = "user@example.com"
display-name = "Your Name"
default = true

# IMAP backend for reading emails
backend.type = "imap"
backend.host = "imap.example.com"
backend.port = 993
backend.encryption = "tls"
backend.login = "user@example.com"
backend.auth.type = "password"
backend.auth.raw = "your-password"

# SMTP backend for sending emails
send.backend.type = "smtp"
send.backend.host = "smtp.example.com"
send.backend.port = 587
send.backend.encryption = "start-tls"
send.backend.login = "user@example.com"
send.backend.auth.type = "password"
send.backend.auth.raw = "your-password"
```

## Encryption Options

- `"tls"` — Full TLS connection (typically port 993 for IMAP, 465 for SMTP)
- `"start-tls"` — Upgrade plain connection to TLS (typically port 143 for IMAP, 587 for SMTP)
- `"none"` — No encryption (not recommended)

## Password Options

### Raw password (testing only, not recommended)
```toml
backend.auth.type = "password"
backend.auth.raw = "your-password"
```

### Password from command (recommended)
```toml
backend.auth.type = "password"
backend.auth.cmd = "pass show email/imap"
# backend.auth.cmd = "security find-generic-password -a user@example.com -s imap -w"
```

### System keyring (requires keyring extra)
```toml
backend.auth.type = "password"
backend.auth.keyring = "imap-example"
```

Install with keyring support:
```bash
pip install ymailink[keyring]
```

## Outlook Configuration (Microsoft Graph API)

Uses OAuth2 via Microsoft identity platform.

```toml
[accounts.outlook]
email = "you@outlook.com"
display-name = "Your Name"
default = true

backend.type = "outlook"
backend.client-id = "your-azure-app-client-id"
backend.tenant-id = "common"
# backend.client-secret = "optional-for-native-apps"

send.backend.type = "outlook"
send.backend.client-id = "your-azure-app-client-id"
send.backend.tenant-id = "common"
```

**Setup steps:**
1. Register an app in Azure Portal (App Registrations)
2. Add API permissions: `Mail.ReadWrite`, `Mail.Send`
3. Set redirect URI to `http://localhost` for native app flow
4. Copy the Application (client) ID into config

OAuth2 tokens are cached in `~/.config/ymailink/tokens/outlook_<account>.json`.

Install with Outlook support:
```bash
pip install ymailink[outlook]
```

## Gmail Configuration (Google API)

Uses OAuth2 via Google Cloud Console.

```toml
[accounts.gmail]
email = "you@gmail.com"
display-name = "Your Name"
default = true

backend.type = "gmail"
backend.client-id = "your-google-client-id"
backend.client-secret = "your-google-client-secret"

send.backend.type = "gmail"
send.backend.client-id = "your-google-client-id"
send.backend.client-secret = "your-google-client-secret"
```

**Setup steps:**
1. Create a project in Google Cloud Console
2. Enable the Gmail API
3. Create OAuth2 credentials (Desktop application type)
4. Download credentials and copy client-id / client-secret into config

OAuth2 tokens are cached in `~/.config/ymailink/tokens/gmail_<account>.json`.

Install with Gmail support:
```bash
pip install ymailink[gmail]
```

## Exchange Configuration

Uses exchangelib for on-premises or Exchange Online mailboxes.

```toml
[accounts.exchange]
email = "user@company.com"
display-name = "User Name"
default = true

backend.type = "exchange"
backend.server = "mail.company.com"
backend.username = "DOMAIN\\username"
backend.auth-type = "auto"
# backend.auth-type = "ntlm"
# backend.auth-type = "basic"

send.backend.type = "exchange"
send.backend.server = "mail.company.com"
send.backend.username = "DOMAIN\\username"
send.backend.auth-type = "auto"
```

**Auth types:**
- `"auto"` — Try all supported auth methods
- `"ntlm"` — NTLM authentication (common for on-premises Exchange)
- `"basic"` — Basic authentication

**Server autodiscover:** If `server` is omitted or set to `"autodiscover"`, exchangelib will attempt to autodiscover the Exchange server from the email address. This may take longer on first connection.

Install with Exchange support:
```bash
pip install ymailink[exchange]
```

## Gmail via IMAP (App Password)

If you prefer standard IMAP/SMTP with Gmail:

```toml
[accounts.gmail-imap]
email = "you@gmail.com"
display-name = "Your Name"

backend.type = "imap"
backend.host = "imap.gmail.com"
backend.port = 993
backend.encryption = "tls"
backend.login = "you@gmail.com"
backend.auth.type = "password"
backend.auth.cmd = "pass show google/app-password"

send.backend.type = "smtp"
send.backend.host = "smtp.gmail.com"
send.backend.port = 587
send.backend.encryption = "start-tls"
send.backend.login = "you@gmail.com"
send.backend.auth.type = "password"
send.backend.auth.cmd = "pass show google/app-password"
```

**Note:** Gmail requires an App Password if 2FA is enabled. Generate at https://myaccount.google.com/apppasswords

## Folder Aliases

Map standard folder names to provider-specific folder names:
```toml
[accounts.default.folder.aliases]
inbox = "INBOX"
sent = "Sent"
drafts = "Drafts"
trash = "Trash"
junk = "Junk"
```

This allows using standard names across different providers.

## Multiple Accounts

```toml
[accounts.personal]
email = "personal@example.com"
default = true
# ... backend config ...

[accounts.work]
email = "work@company.com"
# ... backend config ...
```

Switch accounts with `--account`:
```bash
ymailink --account work mail list
```

## Additional Options

### Signature
```toml
[accounts.default]
signature = "Best regards,\nYour Name"
```

### Downloads directory
```toml
# Global default
downloads-dir = "~/Downloads"

# Per-account override
[accounts.default]
downloads-dir = "~/Downloads/ymailink"
```

### Editor for composing
Set via environment variable:
```bash
export EDITOR="vim"
```

### Proxy Support

Outlook (Graph API) and Gmail backends respect the standard `HTTPS_PROXY` / `https_proxy` environment variable:

```bash
export HTTPS_PROXY="http://proxy.company.com:8080"
```

## OAuth2 Token Management

For Outlook and Gmail backends, ymailink handles OAuth2 token acquisition and refresh automatically:

- On first use, a browser window opens for authorization
- Tokens are cached in `~/.config/ymailink/tokens/`
- Tokens are refreshed automatically when expired
- To re-authorize, delete the token file and run any command

Token file paths:
- Outlook: `~/.config/ymailink/tokens/outlook_<account_name>.json`
- Gmail: `~/.config/ymailink/tokens/gmail_<account_name>.json`

## AI Configuration

The AI features (`ymailink ai short-summary`, `summary`, `rapid-reply`) require an `[ai]` section in the config:

```toml
[ai]
api-key = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
# base-url = "https://ai.ymailink.com"   # optional, this is the default
# model = "auto"                          # optional, this is the default
```

### Fields

| Field | Required | Default | Description |
|-------|----------|---------|-------------|
| `api-key` | **Yes** | — | AI API key for authentication |
| `base-url` | No | `https://ai.ymailink.com` | AI API base URL |
| `model` | No | `auto` | Model identifier (e.g. `gpt-4o`, `claude-3.5-sonnet`) |

### Install AI extra

```bash
pip install ymailink[ai]
```

### Usage

```bash
# One-line short summary
ymailink ai short-summary 42

# Detailed summary
ymailink ai summary 42

# Quick reply suggestions (3 options)
ymailink ai rapid-reply 42
```

All three commands fetch the email by ID from the configured account, send it to the AI API, and print the result. The `-f/--folder` flag specifies which folder to look in (default: `INBOX`).
