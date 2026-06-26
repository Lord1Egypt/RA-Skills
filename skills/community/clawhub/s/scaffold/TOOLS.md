<!--
TOOLS.md - Local Tool Notes

WHAT THIS IS: Your agent's cheat sheet for YOUR specific setup.
Skills define how tools work. This file is for the stuff unique to your environment.

HOW TO CUSTOMIZE:
  - Add entries as you wire up devices, services, and infrastructure
  - Your agent will populate this over time - just tell it to "update TOOLS.md"
  - Keep sensitive credentials OUT - use environment variables instead
  - This file is safe to commit to git if you scrub credentials
-->

# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics - the stuff that's unique to your setup.

---

## What Goes Here

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- API endpoint URLs (no keys - use env vars)
- Anything environment-specific your agent needs to remember

---

## Template Sections

Fill these in as you wire things up. Delete the ones you don't use.

### Cameras
```
- [camera-name] → [location/description], [FOV/type]
```

### SSH Hosts
```
- [alias] → [IP or hostname], user: [username]
```

### TTS / Voice
```
- Preferred voice: [voice name] - [description]
- Default output: [speaker or device name]
```

### Telegram
```
- Your chat ID: [YOUR_TELEGRAM_ID]
- Groups: [name] → [chat ID]
```

### Services & APIs
```
- [Service name]: endpoint [URL], authenticated via [env var name]
```

### Cron Jobs

**Keep this updated.** A log of your active crons here means your agent can reference them without reading your jobs config. When you add or remove a cron, update this list.

```
Keep a log of your active crons here so your agent can reference them.
- [job ID] → [description], [schedule], [model]
```

### Confirmed Models

Run `openclaw models list` and paste the models available on your setup:

```
- Tier 1 (cheap/fast): [model name]
- Tier 2 (balanced): [model name]
- Tier 3 (premium): [model name]
```

See MULTI-MODEL-ROUTING.md for which models belong in which tier.

---

## Notes on Security

- **Never** store API keys, passwords, or tokens in this file
- Use environment variables: `export MY_API_KEY="..."` in `~/.zshrc` or equivalent
- Reference by env var name here: "Auth: $MY_API_KEY"
- Credentials in files get committed to git - credentials in env vars don't

---

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

*Add whatever helps you do your job. This is your cheat sheet.*
