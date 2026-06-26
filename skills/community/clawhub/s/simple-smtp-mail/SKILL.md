# Simple SMTP Mail

Send emails via SMTP using `msmtp` command-line tool.

## Configuration

Create a configuration file at `~/.msmtp/config` with the following format:

```
account default
host <SMTP_SERVER>
port <PORT>
tls on
tls_starttls off
auth on
user <EMAIL_ADDRESS>
password <PASSWORD>
from <EMAIL_ADDRESS>
```

### Common SMTP Settings

**Gmail:**
- SMTP Server: `smtp.gmail.com`
- Port: `465` (SSL) or `587` (TLS)
- Note: Use App Password, not your regular password

**QQ Mail:**
- SMTP Server: `smtp.qq.com`
- Port: `465`

**Outlook/Hotmail:**
- SMTP Server: `smtp.office365.com`
- Port: `587`

**163.com:**
- SMTP Server: `smtp.163.com`
- Port: `465`

## Installation

### 1. Install msmtp

**macOS:**
```bash
brew install msmtp
```

**Linux (Debian/Ubuntu):**
```bash
sudo apt install msmtp
```

**Linux (Fedora/RHEL):**
```bash
sudo dnf install msmtp
```

### 2. Configure SMTP

Edit `~/.msmtp/config`:
```bash
nano ~/.msmtp/config
```

### 3. Set Permissions
```bash
chmod 600 ~/.msmtp/config
```

## Sending Email

### Basic Email
```bash
echo "Body text" | msmtp recipient@example.com
```

### With Subject
```bash
echo -e "Subject: Your Subject\n\nBody text" | msmtp recipient@example.com
```

### With Subject and From Header
```bash
echo -e "Subject: Your Subject\nFrom: your@email.com\n\nBody text" | msmtp recipient@example.com
```

### HTML Content
```bash
echo -e "Subject: Your Subject\nContent-Type: text/html; charset=UTF-8\n\n<html>...</html>" | msmtp recipient@example.com
```

## Testing

Check if SMTP server is reachable:
```bash
msmtp --file=~/.msmtp/config --serverinfo
```

## Troubleshooting

- **"Account not found"**: Check your config file path with `--file` flag
- **"Authentication failed"**: Verify username and password (or App Password)
- **"Connection refused"**: Check port number and firewall settings
- **"TLS certificate error"**: Try `tls_certcheck off` in config (not recommended for production)
