---
name: upkuajing-contact-info-validity-check
description: Official skill for upkuajing (跨境魔方). Check the validity of contact information including phone numbers, email addresses, and domains. Returns status, type, and additional metadata for each contact.
metadata: {"version":"1.0.0","homepage":"https://www.upkuajing.com","clawdbot":{"emoji":"📞","requires":{"bins":["python"],"env":["UPKUAJING_API_KEY"]},"primaryEnv":"UPKUAJING_API_KEY"}}
---

# UpKuaJing Contact Info Validity Check

Check the validity of contact information using the UpKuaJing Open Platform API. This skill provides three detection interfaces: phone validity, email validity, and domain validity.

## Overview

This skill provides access to UpKuaJing's contact validity detection through:
- **Phone Validity Check** (`phone_validity_check.py`): Check phone number validity, type, and WhatsApp status
- **Email Validity Check** (`email_validity_check.py`): Check email address validity
- **Domain Validity Check** (`domain_validity_check.py`): Check domain validity and security

## Running Scripts

### Environment Setup

1. **Check Python**: `python --version`
2. **Install dependencies**: `pip install -r requirements.txt`

Script directory: `scripts/*.py`
Run example: `python scripts/*.py`

**Important**: Always use direct script invocation like `python scripts/phone_validity_check.py`. **Do NOT use** shell compound commands like `cd scripts && python phone_validity_check.py`.

## Three Detection APIs

### Phone Validity Check (`phone_validity_check.py`)

Check phone number validity, type, and WhatsApp status.

**Parameters**: See [Phone Validity API](references/phone-api.md)

**Examples**:
```bash
# Check single phone number
python scripts/phone_validity_check.py --phones "+8613812345678"

# Check multiple phone numbers
python scripts/phone_validity_check.py --phones "+8613812345678 +14155551234 +442071234567"
```

### Email Validity Check (`email_validity_check.py`)

Check email address validity.

**Parameters**: See [Email Validity API](references/email-api.md)

**Examples**:
```bash
# Check single email
python scripts/email_validity_check.py --emails "test@example.com"

# Check multiple emails
python scripts/email_validity_check.py --emails "test@example.com valid@gmail.com invalid-email"
```

### Domain Validity Check (`domain_validity_check.py`)

Check domain validity and security status.

**Parameters**: See [Domain Validity API](references/domain-api.md)

**Examples**:
```bash
# Check single domain
python scripts/domain_validity_check.py --domains "google.com"

# Check multiple domains
python scripts/domain_validity_check.py --domains "google.com fake-domain-xyz123456.com github.com"
```

## API Key and UpKuaJing Account

- **API Key**: Stored in `~/.upkuajing/.env` file as `UPKUAJING_API_KEY`
- **First check**: If not set, prompt user to provide or apply at [UpKuaJing Open Platform](https://developer.upkuajing.com/)

### **API Key Not Set**
First check if the `~/.upkuajing/.env` file has UPKUAJING_API_KEY;
If UPKUAJING_API_KEY is not set, prompt the user to choose:
1. User has one: User provides it (manually add to ~/.upkuajing/.env file)
2. User doesn't have one: Guide user to apply at [UpKuaJing Open Platform](https://developer.upkuajing.com/)
Wait for user selection;

### **Account Top-up**
When API response indicates insufficient balance, explain and guide user to top up:
1. Create top-up order (`auth.py --new_rec_order`)
2. Based on order response, send payment page URL to user, guide user to open URL and pay, user confirms after successful payment;

### **Get Account Information**
Use this script to get account information for UPKUAJING_API_KEY: `auth.py --account_info`

## Fees

**All validity check API calls incur fees**.
**Latest pricing**: Users can visit [Detailed Price Description](https://www.upkuajing.com/web/openapi/price.html)
Or use: `python scripts/auth.py --price_info` (returns complete pricing for all interfaces)

### Fee Confirmation Principle

**Any operation that incurs fees must first inform and wait for explicit user confirmation. Do not execute in the same message as the notification.**

## Workflow

### Decision Guide

| User Intent | Use API |
|-------------|---------|
| "Check if phone number is valid" | Phone Validity Check |
| "Verify email address exists" | Email Validity Check |
| "Check if domain is safe" | Domain Validity Check |

## Error Handling

- **API key invalid/non-existent**: Check `UPKUAJING_API_KEY` in `~/.upkuajing/.env` file
- **Insufficient balance**: Guide user to top up
- **Invalid parameters**: **Must first check the corresponding API documentation in references/ directory**, get correct parameter names and formats from documentation, do not guess

### API Documentation Reference

- Phone Validity: Check [references/phone-api.md](references/phone-api.md)
- Email Validity: Check [references/email-api.md](references/email-api.md)
- Domain Validity: Check [references/domain-api.md](references/domain-api.md)

## Notes

- File paths use forward slashes on all platforms
- **Do not guess parameter names**, get accurate parameter names and formats from documentation
- **Prohibit outputting technical parameter format**: Do not display code-style parameters in responses, convert to natural language
- **Do not estimate or guess fees** — use `python scripts/auth.py --price_info` to get accurate pricing information

## Related Skills

Other UpKuaJing skills you might find useful:

- upkuajing-global-company-people-search — Global company and people search
- upkuajing-customs-trade-company-search — Search customs trade companies
- upkuajing-map-merchants-search — Map-based merchant search
- upkuajing-email-tool — Send emails and manage email tasks
- upkuajing-sms-tool — Send SMS and manage SMS tasks
