# Gmail IMAP Setup

## Step 1: Enable IMAP in Gmail
1. Go to Gmail → Settings (gear icon) → See all settings
2. Click the **Forwarding and POP/IMAP** tab
3. Under "IMAP access," select **Enable IMAP**
4. Click Save Changes

## Step 2: Create an App Password
Requires 2-Step Verification to be enabled first.

1. Go to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
2. Click **Create app password** (or Select app → Other → type a name like "openclaw")
3. Copy the 16-character password (format: `xxxx xxxx xxxx xxxx`)

## Step 3: Config values
```json
{
  "email": "yourname@gmail.com",
  "password": "xxxx xxxx xxxx xxxx",
  "imap_host": "imap.gmail.com",
  "imap_port": 993
}
```

---

# Other IMAP Providers

| Provider | imap_host | imap_port |
|----------|-----------|-----------|
| Outlook/Hotmail | imap-mail.outlook.com | 993 |
| Yahoo | imap.mail.yahoo.com | 993 |
| QQ Mail | imap.qq.com | 993 |
| 163 Mail | imap.163.com | 993 |
| Custom/Self-hosted | (your server) | 993 |

For non-Gmail providers, use your regular account password (or generate an app password if 2FA is enabled).
