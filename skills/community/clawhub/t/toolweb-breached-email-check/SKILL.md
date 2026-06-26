# Breached Email Check

Check whether an email address has appeared in known data breaches. Submit any email address and get back a breach history report — including which breaches exposed the address, what data types were compromised, breach dates, and remediation recommendations. Essential for user onboarding security checks, employee credential monitoring, and threat exposure assessments.

---

## Usage

```json
{
  "tool": "breached_email_check",
  "input": {
    "email": "user@example.com"
  }
}
```

---

## Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `email` | string | ✅ | The email address to check against known data breach databases |

---

## What You Get

- **Breach status** — whether the email has been found in any known breaches
- **Breach list** — names of breaches the email appeared in, with dates
- **Compromised data types** — what was exposed per breach (passwords, phone numbers, physical addresses, credit cards, etc.)
- **Breach severity rating** — overall risk level based on sensitivity of exposed data
- **Paste exposure** — whether the email has appeared in public paste sites (Pastebin, etc.)
- **Remediation guidance** — specific actions to take based on breach findings (password reset, MFA, account monitoring)

---

## Example Output

```json
{
  "email": "user@example.com",
  "breached": true,
  "breach_count": 3,
  "severity": "High",
  "breaches": [
    {
      "name": "LinkedIn (2012)",
      "date": "2012-06-05",
      "compromised_data": ["Email Addresses", "Passwords"],
      "description": "Password hashes exposed in large-scale breach; later cracked and published",
      "verified": true
    },
    {
      "name": "Adobe (2013)",
      "date": "2013-10-04",
      "compromised_data": ["Email Addresses", "Password Hints", "Passwords", "Usernames"],
      "description": "Source code and encrypted credentials exposed for 153 million accounts",
      "verified": true
    },
    {
      "name": "DataBreach.com (2020)",
      "date": "2020-03-21",
      "compromised_data": ["Email Addresses", "Phone Numbers", "Physical Addresses"],
      "description": "Aggregated breach data compilation including PII from multiple sources",
      "verified": false
    }
  ],
  "paste_exposure": true,
  "paste_count": 1,
  "remediation": [
    "Change passwords on all accounts using this email address immediately",
    "Enable multi-factor authentication (MFA) on all associated accounts",
    "Check for unauthorized account activity on LinkedIn and Adobe",
    "Consider using a unique email alias for sensitive accounts going forward",
    "Monitor credit report if physical address was exposed"
  ]
}
```

### When email is clean

```json
{
  "email": "safe@example.com",
  "breached": false,
  "breach_count": 0,
  "severity": "None",
  "breaches": [],
  "paste_exposure": false,
  "paste_count": 0,
  "remediation": [
    "No known breaches found — continue using strong, unique passwords",
    "Enable MFA as a proactive measure"
  ]
}
```

---

## Use Cases

- **User onboarding** — check if a new user's email is in known breaches at signup
- **Employee security audits** — identify staff with exposed credentials before they become an attack vector
- **Threat exposure assessment** — assess corporate email domain exposure across your workforce
- **Password reset triggers** — automatically prompt users with breached emails to reset credentials
- **Security awareness** — show users their personal breach history to drive MFA adoption

---

## API Reference

**Base URL:** `https://portal.toolweb.in/apis/security/breached-email-check`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/check-breach` | POST | Check an email address against known data breach databases |

**Authentication:** Pass your API key as `X-API-Key` header or `mcp_api_key` argument via MCP.

---

## Pricing

| Plan | Daily Limit | Monthly Limit | Price |
|------|-------------|---------------|-------|
| Free | 5 / day | 50 / month | $0 |
| Developer | 20 / day | 500 / month | $39 |
| Professional | 200 / day | 5,000 / month | $99 |
| Enterprise | 100,000 / day | 1,000,000 / month | $299 |

---

## About

**ToolWeb.in** — 200+ security APIs, CISSP & CISM certified, built for enterprise security practitioners.

Platforms: Pay-per-run · API Gateway · MCP Server · OpenClaw · RapidAPI · YouTube

- 🌐 [toolweb.in](https://toolweb.in)
- 🔌 [portal.toolweb.in](https://portal.toolweb.in)
- 🤖 [hub.toolweb.in](https://hub.toolweb.in) (MCP Server)
- 🦞 [toolweb.in/openclaw/](https://toolweb.in/openclaw/)
- ⚡ [rapidapi.com/user/mkrishna477](https://rapidapi.com/user/mkrishna477)
- 📺 [youtube.com/@toolweb-009](https://youtube.com/@toolweb-009)
