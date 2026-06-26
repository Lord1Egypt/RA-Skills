# WhatsApp HappyBDay Skill ✨

**Version 1.0.2 - Security & Consistency Fixes**

**Monitor WhatsApp groups to dynamically detect people who should be congratulated. It identifies keywords (e.g., "birthday", "congratulations") and the person's name using a score-based system, then automatically sends a random customizable congratulatory message.**

## 🎯 Features

- **Dynamic Group Monitoring**: Automatically fetches active groups via `wacli`. No hardcoding needed.
- **Score-Based Detection**: Weighted scoring system (e.g., "birthday" = +40 pts, "family" = -50 pts) for accuracy.
- **Name Identification**: Extracts names using Regex and dictionary filtering.
- **Fully Customizable**: External JSON files for messages and scoring words.
- **Simulation Mode**: Test safely without sending real messages.

## 📦 Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## ⚙️ Configuration

### Environment Variables (`.env`)

```bash
# Names to skip (your own, close family, etc.)
BIRTHDAY_SKIP_LIST="John,Jane,Alice"

# Minimum messages mentioning name before triggering
BIRTHDAY_MIN_MESSAGES=3

# Confidence threshold score
BIRTHDAY_CONFIDENCE_THRESHOLD=120

# Simulation mode (true=dry-run, false=send real messages)
BIRTHDAY_SIMULATE=true
```

### Custom Dictionaries

**`scoring_words.json`**: Define keywords and point values:
```json
{
  "birthday": {"words": ["birthday", "years", "candle"], "points": 40},
  "general": {"words": ["congrats", "celebrate", "party"], "points": 15},
  "negative": {"words": ["family", "work", "job"], "points": -50}
}
```

**`messages.json`**: Customize congratulatory messages:
```json
{
  "greetings": ["Happy birthday, {name}!", "Congrats {name}!!"],
  "wishes": ["Have a great day!", "Wishing you the best!"],
  "emojis": ["🎉", "🎂", "🥳"]
}
```

## 🚀 Usage

### Manual Test
```bash
python3 scripts/whatsapp_happybday.py
```

### Automated Monitoring (HEARTBEAT.md)

Add to your workspace's `HEARTBEAT.md`:

```markdown
## WhatsApp Birthday Monitor

- **Time Window**: 08:00-20:00 local time only
- **Action**: Run `wacli sync --once`, then execute the happybday script
- **Silence Rule**: If no congratulations sent and no errors, respond ONLY with `HEARTBEAT_OK`
```

### Cron Job Setup

```bash
openclaw cron add \
  --name "WhatsApp HappyBDay Monitor" \
  --cron "0 * * * *" \
  --message "Run python3 ~/.openclaw/skills/whatsapp-happybday/scripts/whatsapp_happybday.py. Report any congratulations sent or errors encountered. If no action taken, respond with HEARTBEAT_OK."
```

## 📝 How It Works

1. **Sync**: Pulls recent messages from all WhatsApp groups via `wacli`
2. **Score**: Analyzes each message with weighted keywords
3. **Identify**: Extracts names using regex and dictionary filtering
4. **Validate**: Confirms threshold scores and minimum message counts
5. **Celebrate**: Sends a random congratulatory message with emojis

## 🔒 Safety Features

- ✅ Simulation mode for testing
- ✅ Skip lists to exclude specific names
- ✅ Rate limiting (one message per person per day)
- ✅ Threshold validation prevents false positives
- ✅ State tracking prevents duplicate messages

## 🌍 Language Support

Fully language-agnostic! Just update `scoring_words.json` and `messages.json` for your target language. Currently includes **Basque** support out of the box.

## 📦 Files

- `scripts/whatsapp_happybday.py` - Main script
- `messages.json` - Congratulatory message templates
- `scoring_words.json` - Keyword scoring dictionary
- `data/name_counter.json` - State tracking (auto-purged after 7 days)

## 🤝 Contributing

Feel free to submit PRs with:
- New language dictionaries
- Additional scoring keywords
- Bug fixes or improvements

## 📄 License

MIT License

---

**Built with ❤️ for busy WhatsApp groups everywhere**
