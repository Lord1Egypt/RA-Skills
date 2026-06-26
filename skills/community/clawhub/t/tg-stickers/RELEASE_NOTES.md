# Release Notes

## v0.1.0 (2026-03-06)

Initial release! 🎉

### Features

- ✅ **Sticker Collection** - Collect stickers sent by users
- ✅ **Smart Sending** - Context-aware sticker selection
- ✅ **Frequency Limits** - Respect conversation flow (1 per 5-10 messages)
- ✅ **Native Telegram API** - Direct `sendSticker` API calls
- ✅ **Usage Tracking** - Monitor sticker collection and usage
- ✅ **Rule-Based Decision** - Based on OpenClaw Reactions guidelines

### Files Included

- `SKILL.md` - Complete documentation
- `README.md` - Quick start guide
- `LICENSE` - MIT License
- `stickers.json.example` - Template configuration
- `send-sticker.sh` - Sticker sending script
- `add-sticker.sh` - Collection management
- `should_send_sticker.py` - Decision logic
- `.gitignore` - Git configuration

### Requirements

- OpenClaw 2026.3.0+
- Telegram channel configured
- Python 3.6+
- `jq` (for JSON manipulation)

### Installation

```bash
cd ~/.openclaw/workspace/skills
tar -xzf tg-stickers.tar.gz
cd tg-stickers
cp stickers.json.example stickers.json
chmod +x *.sh
```

### Quick Test

```bash
# Add a test sticker
./add-sticker.sh "YOUR_FILE_ID" "😀" "TestSet" "happy"

# Check decision
python3 should_send_sticker.py "test" "Great job!"

# Send sticker
./send-sticker.sh "YOUR_FILE_ID" YOUR_CHAT_ID "Testing"
```

### Known Issues

None yet! Please report any issues on GitHub.

### Roadmap

- [ ] Auto-collect stickers from incoming messages
- [ ] Emoji-based smart selection
- [ ] Tag-based filtering
- [ ] Statistics dashboard
- [ ] Integration with OpenClaw message tool

### Credits

Created with love for the OpenClaw community. Special thanks to all contributors!

---

**Enjoy! 🎨**
