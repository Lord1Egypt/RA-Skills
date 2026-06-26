---
name: simplelogin-cli
description: Create and manage SimpleLogin email aliases from the command line. Protect your real email with secure, private aliases.
license: MIT
metadata:
  clawdbot:
    emoji: "📧"
  openclaw:
    emoji: "📧"
    os: ["linux", "darwin", "win32"]
    requires:
      bins: ["curl", "jq"]
      install: []
    secrets:
      - path: "~/.openclaw/secrets/simplelogin.json"
        description: "SimpleLogin API key (fallback if SIMPLELOGIN_API_KEY env var not set)"
        fields: ["password", "api_key"]
  clawhub:
    category: "privacy"
    tags: ["email", "alias", "privacy", "simplelogin"]
---

# SimpleLogin CLI

Create and manage privacy-focused email aliases with SimpleLogin. Protect your real email address when signing up for services, newsletters, or online shopping.

## Features

- ✅ Create custom aliases (you choose the prefix)
- ✅ Create random aliases (generated automatically)
- ✅ List all your aliases with status
- ✅ Enable/disable aliases on demand
- ✅ Smart hostname detection (auto-suggests alias based on website)
- ✅ Multiple mailbox support
- ✅ **Create contacts & get reverse aliases** (reply to forwarded emails)
- ✅ **List contacts** for any alias
- ✅ Secure API key management

## Prerequisites

1. **SimpleLogin account** - Sign up at https://simplelogin.io
2. **API key** - Generate in SimpleLogin dashboard → API Keys
3. **Store API key securely** - Use environment variable or password manager

## Installation

```bash
# Install via ClawHub (when published)
clawhub install simplelogin-cli

# Or clone manually
git clone https://github.com/mcclawd/simplelogin-cli.git
```

## Configuration

### Option 1: Environment Variable (Quick)

```bash
export SIMPLELOGIN_API_KEY="your-api-key-here"
```

### Option 2: Bitwarden/Password Manager (Recommended)

Store your API key in your password manager:
- **Name:** `SimpleLogin API Key`
- **Custom Field:** `api_key` = your API key

The skill will automatically retrieve this if Warden or similar credential management is available.

## Usage

### Create a Custom Alias

```bash
# Create alias with your chosen prefix
simplelogin create shopping
# → shopping@yourdomain.com

# With note
simplelogin create amazon --note "Amazon purchases"
# → amazon@yourdomain.com

# For specific website
simplelogin create --for github.com
# → github-xyz@simplelogin.com
```

### Create Reverse Alias (Send-From)

**Reverse aliases let you send emails FROM your alias identity.** Create a contact for each recipient:

```bash
# Create contact for a recipient
simplelogin contact-create shopping@example.com amazon-support@amazon.com
# → Reverse alias: abc123@simplelogin.co
# → Send emails to this address → forwards through shopping@example.com

# With JSON output (for automation)
export SIMPLELOGIN_JSON=true
simplelogin contact-create shopping@example.com vendor@company.com
# → Returns full JSON with reverse_alias and reverse_alias_address
```

**How it works:**
1. `contact-create` calls SimpleLogin API: `POST /api/aliases/{id}/contacts`
2. API returns `reverse_alias` field with obfuscated address
3. Send email to reverse alias → forwards through your alias → appears from alias

**Use case:** Enable refund requests, support inquiries, or any email sending from hidden identity.

### Create a Random Alias

```bash
# Generate random alias
simplelogin random
# → random_word123@simplelogin.com

# With note
simplelogin random --note "Newsletter signup"
```

### List Aliases

```bash
# Show recent aliases
simplelogin list

# Show all
simplelogin list --all

# Filter by domain
simplelogin list --domain simplelogin.com
```

### List Contacts for an Alias

```bash
# Show all contacts (recipients) for an alias
simplelogin contact-list shopping@example.com
# → amazon-support@amazon.com → abc123@simplelogin.co
# → support@store.com → xyz789@simplelogin.co
```

### Manage Aliases

```bash
# Disable alias
simplelogin disable shopping@yourdomain.com

# Enable alias
simplelogin enable shopping@yourdomain.com

# Delete alias
simplelogin delete shopping@yourdomain.com
```

### Create Contacts & Get Reverse Aliases

When you receive a forwarded email and want to **reply** to the sender, you need to create a contact for your alias. This gives you a reverse alias email address that forwards through your alias.

```bash
# Create contact for an alias (get reverse alias)
simplelogin contact-create <alias_email> <contact_email>
# → Reverse alias: xxxxx@simplelogin.co
# → Send emails to this address → forwards through your alias

# List all contacts for an alias
simplelogin contact-list <alias_email>
# → support@example.com → xxxxx@simplelogin.co
```

**Use case:** You signed up for a service using `shopping@yourdomain.com`. They sent an email to your real mailbox. To reply, create a contact:

```bash
simplelogin contact-create shopping@yourdomain.com support@example.com
# → Reverse alias: bncxsoitvfvzjlxtohfzzq@simplelogin.co

# Now send your reply to the reverse alias
echo "My reply" | mail -s "Re: Your subject" bncxsoitvfvzjlxtohfzzq@simplelogin.co
```

The email will appear to come from `shopping@yourdomain.com`, keeping your real mailbox private.

## API Reference

### simplelogin create [prefix]

Create a custom alias.

**Options:**
- `prefix` - The alias prefix (before @)
- `--note, -n` - Add a note/description
- `--for, -f` - Suggest alias based on hostname (e.g., `amazon.com`)
- `--mailbox, -m` - Specify mailbox ID (default: first available)

**Examples:**
```bash
simplelogin create shopping
simplelogin create amazon --note "Prime member"
simplelogin create --for netflix.com --note "Streaming"
```

### simplelogin random

Create a random alias.

**Options:**
- `--note, -n` - Add a note/description
- `--word, -w` - Use word-based random (default: uuid-style)
- `--mailbox, -m` - Specify mailbox ID

**Examples:**
```bash
simplelogin random
simplelogin random --note "Forum signup"
simplelogin random --word
```

### simplelogin contact-create <alias> <contact>

Create a contact (recipient) for an alias, enabling you to send emails FROM the alias identity.

**Arguments:**
- `alias` - The alias email address
- `contact` - The recipient email address

**Returns:** `reverse_alias` - Send emails to this address to send from your alias

**Options:**
- (JSON mode) Set `SIMPLELOGIN_JSON=true` for full JSON response

**Examples:**
```bash
simplelogin contact-create amazon@alias.com refunds@merchant.com
simplelogin create --for nordvpn.com support@nordvpn.com  # Auto-suggests alias
```

### simplelogin contact-list <alias>

List all contacts (recipients) configured for an alias.

**Arguments:**
- `alias` - The alias email address

**Returns:** List of contact emails and their reverse aliases

### simplelogin list

List your aliases.

**Options:**
- `--all, -a` - Show all aliases (not just recent)
- `--domain, -d` - Filter by domain
- `--enabled` - Show only enabled
- `--disabled` - Show only disabled

### simplelogin disable|enable|delete <alias>

Manage existing aliases.

**Examples:**
```bash
simplelogin disable shopping@yourdomain.com
simplelogin enable shopping@yourdomain.com
simplelogin delete temp@simplelogin.com
```

### simplelogin contact-create <alias> <contact>

Create a contact for an alias and get the reverse alias address.

**Arguments:**
- `alias` - Your alias email (e.g., `shopping@yourdomain.com`)
- `contact` - The contact's email address (e.g., `support@vendor.com`)

**Examples:**
```bash
simplelogin contact-create shopping@yourdomain.com support@vendor.com
# → Contact already exists for support@vendor.com
# → Reverse alias: bncxsoitvfvzjlxtohfzzq@simplelogin.co
# → Send emails to this address → forwards through shopping@yourdomain.com
```

**What is a reverse alias?**
A reverse alias is a special email address that, when you send to it, forwards through your SimpleLogin alias and appears to come from your alias (hiding your real mailbox). This is how you reply to emails that were forwarded to you.

### simplelogin contact-list <alias>

List all contacts for an alias with their reverse aliases.

**Arguments:**
- `alias` - Your alias email

**Examples:**
```bash
simplelogin contact-list shopping@yourdomain.com
# → support@vendor.com → bncxsoitvfvzjlxtohfzzq@simplelogin.co
# → info@newsletter.com → atltfoczaqdtplypkciksufkpsnjpiqzvrnqrfptjjyxgomx@simplelogin.co
```

## Agent/JSON Mode

For programmatic use (agents, scripts), set `SIMPLELOGIN_JSON=true`:

```bash
export SIMPLELOGIN_JSON=true
simplelogin create shopping --note "Test"
# → {"email":"shopping@yourdomain.com","id":12345,"status":"created"}
```

## Security Notes

- 🔐 **API keys are never stored in the skill** - Always use environment variables or password managers
- 🔐 **Aliases are private** - SimpleLogin doesn't log or sell your data
- 🔐 **Open source** - SimpleLogin code is auditable at https://github.com/simple-login

## Troubleshooting

### "API key not found"
Make sure you've set the `SIMPLELOGIN_API_KEY` environment variable or stored the key in your password manager.

### "No suffixes available"
Check your SimpleLogin account status. Free accounts have limited suffixes.

### Emails going to spam
This is normal for test emails. Gmail may flag programmatic emails. Check your spam folder.

## Contributing

Contributions welcome! Please follow the existing code style and add tests for new features.

## License

MIT License - See LICENSE file
