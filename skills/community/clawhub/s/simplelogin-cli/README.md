# SimpleLogin CLI

Create and manage privacy-focused email aliases with SimpleLogin. Protect your real email address when signing up for services, newsletters, or online shopping.

## What is SimpleLogin?

SimpleLogin is an open-source email aliasing service that lets you:
- Create unlimited email aliases (e.g., `shopping@alias.com` → your real email)
- Receive emails anonymously without exposing your real address
- Reply to emails while keeping your identity private
- Track which services sell your data when spam arrives

## Features

- ✅ Create custom aliases (you choose the prefix)
- ✅ Create random aliases (generated automatically)
- ✅ List all your aliases with status
- ✅ Enable/disable aliases on demand
- ✅ Smart hostname detection (auto-suggests alias based on website)
- ✅ Multiple mailbox support
- ✅ Secure API key management
- ✅ JSON mode for programmatic/agent use

## Installation

### Via ClawHub (recommended)

```bash
clawhub install simplelogin-cli
```

### Manual

```bash
git clone https://github.com/yourusername/simplelogin-cli.git
cd simplelogin-cli
# Add scripts/ to your PATH
```

## Prerequisites

1. **SimpleLogin account** - Sign up at https://simplelogin.io
2. **API key** - Generate in SimpleLogin dashboard → API Keys
3. **Store API key securely** - Environment variable or password manager

## Configuration

### Option 1: Environment Variable (Quick)

```bash
export SIMPLELOGIN_API_KEY="your-api-key-here"
```

Add to your `~/.bashrc` or `~/.zshrc` to persist.

### Option 2: Password Manager (Recommended)

Store your API key in Bitwarden, 1Password, or similar:
- **Name:** `SimpleLogin API Key`
- **Custom Field:** `api_key` = your API key

If using OpenClaw with Warden, the skill will auto-retrieve the key.

## Usage

### Create a Custom Alias

```bash
# Create alias with your chosen prefix
simplelogin create shopping
# → shopping@yourdomain.com

# With note
simplelogin create amazon --note "Amazon purchases"

# For specific website (auto-suggests prefix)
simplelogin create --for github.com
# → github-xyz@simplelogin.com
```

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

## Agent/JSON Mode

For programmatic use by agents or scripts, enable JSON mode:

```bash
export SIMPLELOGIN_JSON=true
simplelogin create shopping --note "Test"
# Output: {"email":"shopping@yourdomain.com","id":12345,"status":"created"}
```

This makes it easy to integrate with:
- OpenClaw agents
- Shell scripts
- CI/CD pipelines
- Automation workflows

## Security

- 🔐 **API keys are never stored in the skill** - Use environment variables or password managers
- 🔐 **Aliases are private** - SimpleLogin doesn't log or sell your data  
- 🔐 **Open source** - SimpleLogin code is auditable at https://github.com/simple-login

## Troubleshooting

### "API key not found"
Make sure you've set the `SIMPLELOGIN_API_KEY` environment variable.

### "No suffixes available"
Check your SimpleLogin account status. Free accounts have limited suffixes.

### Emails going to spam
This is normal. Gmail may flag programmatic emails. Check your spam folder.

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Submit a pull request

## License

MIT License - See [LICENSE](LICENSE) file
