# Setup Guide

## Prerequisites

Before using this skill, ensure you have:

1. **OpenClaw CLI installed**
   ```bash
   npm install -g openclaw
   ```

2. **Telegram Bot created**
   - Message [@BotFather](https://t.me/BotFather) on Telegram
   - Send `/newbot` and follow the prompts
   - Save your bot token (looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

3. **Bash shell** (usually pre-installed on Linux/macOS)

4. **Python 3** (optional, for validation script)
   ```bash
   python3 --version
   ```

## Configuration

### 1. Configure OpenClaw

Edit your OpenClaw configuration file:

**Global config:** `~/.openclaw/config.json`  
**Or workspace config:** `~/your-workspace/openclaw.json`

Add Telegram channel configuration:

```json
{
  "channels": {
    "telegram": {
      "enabled": true,
      "botToken": "YOUR_BOT_TOKEN_HERE"
    }
  }
}
```

### 2. Get Your Chat ID

Start a conversation with your bot, then:

**Method 1 - Via OpenClaw:**
```bash
# Check OpenClaw logs after sending a message to your bot
openclaw logs
```

**Method 2 - Via Telegram API:**
```bash
curl "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates"
```

Look for `"chat":{"id":123456789}` in the response.

### 3. Test Your Setup

```bash
openclaw message send \
  --target "telegram:YOUR_CHAT_ID" \
  --message "🎉 OpenClaw is working!"
```

If you see the message in Telegram, you're ready!

## Environment Variables (Optional)

For better security, you can use environment variables instead of storing the token in config files:

```bash
export OPENCLAW_TELEGRAM_BOT_TOKEN="your_token_here"
```

Then reference it in your config:

```json
{
  "channels": {
    "telegram": {
      "enabled": true,
      "botToken": "${OPENCLAW_TELEGRAM_BOT_TOKEN}"
    }
  }
}
```

## Security Best Practices

1. **Never commit bot tokens to version control**
   - Add `openclaw.json` to `.gitignore`
   - Use environment variables for CI/CD

2. **Restrict bot permissions**
   - Only add bot to chats you control
   - Regularly rotate tokens via BotFather

3. **Review scripts before running**
   - All scripts in this skill are readable and short
   - Check for placeholder replacements (`YOUR_CHAT_ID`)

4. **Use separate bots for dev/prod**
   - Create different bots for testing and production
   - Never test with production chat IDs

## Troubleshooting

### "Command not found: openclaw"

```bash
# Check if installed
which openclaw

# Install if missing
npm install -g openclaw
```

### "Error: Unauthorized"

- Check your bot token is correct
- Ensure bot token is properly set in config
- Verify you've started a conversation with the bot

### "Chat not found"

- Verify your chat ID is numeric (no quotes in commands)
- Ensure you've sent at least one message to the bot first
- Check the target format: `telegram:CHAT_ID` (no spaces)

### Buttons not appearing

- Validate JSON with `python3 scripts/validate_buttons.py 'YOUR_JSON'`
- Check for proper quoting in shell commands
- Review SKILL.md Troubleshooting section

## Next Steps

Once setup is complete:

1. **Read SKILL.md** - Main documentation with patterns and examples
2. **Try examples** - Run scripts in `assets/examples/`
3. **Explore REFERENCE.md** - Advanced usage and all parameters

## Support

- **OpenClaw Docs:** https://docs.openclaw.ai
- **Telegram Bot API:** https://core.telegram.org/bots/api
- **Skill Issues:** Report on ClawHub or GitHub
