# Gmail Setup Guide

## Overview

Step-by-step configuration for connecting himalaya to Gmail, Outlook, or Hostinger (custom domain). Run `scripts/setup-email.sh` after completing the credential steps below.

---

## Provider Auto-Detection

The setup script detects providers by email domain:

| Domain | Provider | IMAP Server | SMTP Server |
|--------|----------|-------------|-------------|
| `gmail.com` | Gmail | `imap.gmail.com:993` | `smtp.gmail.com:587` |
| `outlook.com`, `hotmail.com`, `live.com` | Outlook | `outlook.office365.com:993` | `smtp.office365.com:587` |
| `[other]` | Hostinger (default) | `imap.hostinger.com:993` | `smtp.hostinger.com:587` |

For custom domains on Google Workspace or Microsoft 365, follow Gmail or Outlook steps respectively — the server settings are the same even with a custom domain.

---

## Gmail Setup

### Step 1: Enable IMAP

1. Open Gmail in browser
2. Click gear icon → **See all settings**
3. Go to **Forwarding and POP/IMAP** tab
4. Under "IMAP access": select **Enable IMAP**
5. Click **Save Changes**

### Step 2: Generate App Password

> Required if 2-Factor Authentication is enabled (strongly recommended).

1. Go to [myaccount.google.com](https://myaccount.google.com)
2. Navigate to **Security**
3. Under "How you sign in to Google": click **2-Step Verification**
4. Scroll to bottom → click **App passwords**
5. Enter app name: `himalaya` (or any label)
6. Click **Create**
7. Copy the 16-character password — you will not see it again

> If "App passwords" is not visible, 2FA is not enabled. Enable it first, or use your regular password (less secure).

### Step 3: Run Setup Script

```bash
./scripts/setup-email.sh you@gmail.com "Your Name" "abcd efgh ijkl mnop"
```

Replace `abcd efgh ijkl mnop` with your app password (spaces optional).

---

## Outlook / Microsoft 365 Setup

### Step 1: Enable IMAP

IMAP is enabled by default for Outlook.com personal accounts.

For Microsoft 365 (work/school accounts), an admin may need to enable IMAP:
- Admin center → Users → [user] → Mail → Email apps → enable IMAP

### Step 2: Generate App Password

For personal Outlook.com accounts with 2FA:
1. Go to [account.microsoft.com/security](https://account.microsoft.com/security)
2. Click **Advanced security options**
3. Under "App passwords": click **Create a new app password**
4. Copy the password

For Microsoft 365 with Modern Authentication, app passwords may be disabled by your admin. Contact IT or use OAuth (not covered here).

### Step 3: Run Setup Script

```bash
./scripts/setup-email.sh you@outlook.com "Your Name" "your-app-password"
```

---

## Hostinger (Custom Domain)

### Step 1: Get Email Credentials

1. Log in to [hpanel.hostinger.com](https://hpanel.hostinger.com)
2. Navigate to **Emails** → your email account
3. Note your email address and password
4. IMAP/SMTP settings are available under **Email Settings** in hPanel

### Step 2: Run Setup Script

```bash
./scripts/setup-email.sh you@yourdomain.com "Your Name" "your-email-password"
```

> Hostinger does not require app passwords — use the direct email account password.

---

## Manual Configuration (Fallback)

If the script fails, manually write the himalaya config. Location: `~/.config/himalaya/config.toml`

```toml
[accounts.work]
display-name = "Your Name"
email = "you@example.com"
backend.type = "imap"
backend.host = "imap.example.com"
backend.port = 993
backend.encryption = "tls"
backend.login = "you@example.com"
backend.passwd.cmd = "echo 'your-password'"

sender.type = "smtp"
sender.host = "smtp.example.com"
sender.port = 587
sender.encryption = "start-tls"
sender.login = "you@example.com"
sender.passwd.cmd = "echo 'your-password'"
```

Replace `imap.example.com` and `smtp.example.com` with actual server values from the table above.

> **Security note:** Storing passwords in plain text in config is acceptable for local/private setups. For production or shared environments, use a password manager or keychain integration.

---

## Testing the Connection

After running the setup script, verify with:

```bash
# List inbox
himalaya envelope list --account work --folder INBOX

# List folders
himalaya folder list --account work
```

Expected output: a table of recent emails or a list of mailbox folders.

---

## Troubleshooting

### "Authentication failed"
- Gmail: Ensure app password is used (not your Google account password)
- Outlook: Check that IMAP is enabled and app password is correct
- Hostinger: Double-check email address spelling and password — no app password needed

### "Connection refused" or "Timeout"
- Verify IMAP is enabled in provider settings
- Check that port 993 is not blocked by a firewall
- Try port 143 (STARTTLS) if 993 fails: change `encryption = "tls"` to `encryption = "start-tls"` and port to `143`

### "SSL certificate error"
- Add `ssl-accept-invalid-certs = true` under `backend` (for self-signed certs on custom servers only)

### Multiple Accounts

To add a second account, add another `[accounts.name]` block to the config with a unique name. Reference it with `--account name` in all himalaya commands.

---

## Google Workspace (Custom Domain on Gmail)

Same setup as Gmail. App password generation is at [myaccount.google.com](https://myaccount.google.com) using the workspace account. IMAP server: `imap.gmail.com:993`.

Some Workspace admins disable app passwords — contact your admin if the option is missing.
