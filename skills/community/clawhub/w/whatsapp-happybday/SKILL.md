---
name: whatsapp-happybday
version: 1.0.2
description: Monitor WhatsApp groups to dynamically detect people who should be congratulated. It identifies keywords (e.g., "birthday", "congratulations") and the person's name using a score-based system, then automatically sends a random customizable congratulatory message.
triggers:
  - whatsapp happybday
  - monitor whatsapp group
  - send congratulations
  - whatsapp congratulate
metadata:
  openclaw:
    requires:
      bins:
        - python3
      env:
        - BIRTHDAY_MIN_MESSAGES
        - BIRTHDAY_CONFIDENCE_THRESHOLD
        - BIRTHDAY_SIMULATE
    primaryEnv: BIRTHDAY_MIN_MESSAGES
    homepage: https://github.com/zero-astro/whatsapp-happybday
---

# WhatsApp HappyBDay Skill

A skill to automatically detect when someone is being congratulated in WhatsApp groups and send them a random, customizable congratulatory message. 

It dynamically checks recent messages across all active groups, uses a score-based NLP approach to prevent false positives, and supports any language via customizable dictionaries.

## Features

- **Dynamic Group Monitoring**: Automatically fetches active groups and recent messages via `wacli`. No need to hardcode group names.
- **Score-Based Keyword Detection**: Uses a weighted scoring system (e.g., "birthday" = +40 pts, "family" = -50 pts) to accurately detect congratulatory intent.
- **Name Identification**: Extracts the name of the person being congratulated from the messages using Regex and dictionary filtering.
- **Enhanced Skip List**: Supports both permanent skips (e.g., your own name) AND date-based skips (skip only on specific birthdays). Format: `"Name|MM-DD,OtherName"` where names with `|MM-DD` are skipped ONLY on that date, and names without the pipe are permanently skipped.
- **Fully Customizable**: Uses external JSON files (`messages.json` and `scoring_words.json`) so you can adapt it to any language or vibe.
- **Simulation Mode**: Test the logic safely without actually sending messages.

## Dependencies

- **Python 3**: Ensure Python 3 is installed on your system.
- **Python Packages**: The script requires the `python-dotenv` package to read environment variables from `.env`. You can install it using the provided `requirements.txt`:
  ```bash
  pip install -r ~/.openclaw/skills/whatsapp-happybday/requirements.txt
  ```
- **`wacli`**: OpenClaw already provides a `wacli` skill out of the box. Just ensure that the `wacli` skill is activated, available to the agent, and properly configured (i.e., you have completed the authentication process by following its own instructions).

## Setup & Configuration

To make the skill work, you need to configure a few environment variables and (optionally) customize the dictionaries.

### 1. Environment Variables (`.env`)
Create a `.env` file in the skill's root directory (`~/.openclaw/skills/whatsapp-happybday/.env`) or export these variables in your environment:

```bash
# Skip list with enhanced format:
# - "Name|MM-DD" = skip this person ONLY on their birthday (date-based)
# - "Name" (no pipe) = permanently skip this name (e.g., your own name)
# Examples: "John|01-15,Jane,Alice|12-25"
export BIRTHDAY_SKIP_LIST="Urtzi|03-16,Iraide,Xune,Eñaut|08-25"

# Minimum messages mentioning the name before triggering (default: 3)
export BIRTHDAY_MIN_MESSAGES="3"

# Minimum score threshold to trigger the congratulation (default: 120)
export BIRTHDAY_CONFIDENCE_THRESHOLD="120"

# Simulation mode (true = dry-run/logging only, false = actually send messages) (default: true)
export BIRTHDAY_SIMULATE="true"
```

### 2. Dictionaries

The skill uses two JSON files. If they don't exist, it uses English defaults.

**`scoring_words.json`**: Defines the words and their point values.
```json
{
  "birthday": {"words": ["birthday", "years", "candle", "cake"], "points": 40},
  "general": {"words": ["congratulations", "congrats", "celebrate", "day", "happy", "party"], "points": 15},
  "negative": {"words": ["family", "son", "daughter", "child", "kid", "work", "job"], "points": -50}
}
```

**`messages.json`**: Templates for the automated responses.
```json
{
  "greetings": [
    "Happy birthday, {name}!", 
    "Congrats {name}!!"
  ],
  "wishes": [
    "Have a great day!", 
    "Wishing you the best!"
  ],
  "emojis": ["🎉", "🎂", "🥳"]
}
```
*Note: The script combines one greeting, one wish, and 1-4 random emojis.*

## Agent Integration

For the system to work autonomously, your OpenClaw agent needs to continuously sync WhatsApp messages and run the detection script.

### 1. Syncing Messages (`HEARTBEAT.md`)
The Python script reads from the local `wacli` database, so it must be kept up to date. Add the following to your workspace's `HEARTBEAT.md`:

```markdown
## WhatsApp Synchronization and Birthday/Congrats Monitoring

- **Action:** Run `wacli sync --once`. Afterward, check if there are any new congratulatory/birthday messages in the configured WhatsApp groups.
- **Silence Rule (CRITICAL):** If there are no errors AND no new congratulatory messages or new people detected to congratulate, **DO NOT SEND ANY MESSAGE**. Respond ONLY with the exact string `HEARTBEAT_OK`. The user does not want to receive empty notifications or status updates between 08:00 and 20:00. Only report positive findings or critical system errors.
```

### 2. Automated Execution (Cron Job)
Create a cron job to run the monitor script periodically (e.g., every hour between 8 AM and 8 PM). Run this in your terminal:

```bash
openclaw cron add \
  --name "WhatsApp HappyBDay Monitor" \
  --cron "0 8-20 * * *" \
  --message "Run this command: python3 ~/.openclaw/skills/whatsapp-happybday/scripts/whatsapp_happybday.py. Examine the script's output carefully. If the script sent a congratulatory message to someone, reply with a short summary saying who received it. If the script encountered an error, reply explaining the exact error message. If neither happened (no message sent and no errors), reply ONLY with exactly HEARTBEAT_OK."
```

## How It Works Under the Hood

1. **Message Fetching**: Iterates through all active WhatsApp groups and fetches recent messages for the current day.
2. **Scoring**: Calculates a score for each message based on `scoring_words.json`. Messages with a score <= 0 are ignored.
3. **Name Extraction**: Uses Regex to find capitalized proper nouns, filtering out dictionary words.
4. **Validation**: Checks if the name has reached the `BIRTHDAY_MIN_MESSAGES` count and the combined `BIRTHDAY_CONFIDENCE_THRESHOLD` score. It also checks the `BIRTHDAY_SKIP_LIST`.
5. **State Tracking**: Stores its progress in `data/name_counter.json`. This file tracks which messages have been processed, the accumulated scores and message counts for each detected name, and a list of people who have already been congratulated today (to prevent duplicate messages). Older data is automatically purged after 7 days.
6. **Dispatch**: Formats a random message from `messages.json` and sends it using `wacli` (unless `BIRTHDAY_SIMULATE` is true).