---
name: skill-sharer
description: Share a skill publicly to the Enterprise-Crew-skills GitHub repo. Strips personal/security info, generates a README, and updates the repo index.
---

# Skill Sharer

Publishes a local skill to **<your-github-user>/Enterprise-Crew-skills** on GitHub.

## What it does

1. Copies the skill into a sanitized folder
2. Strips personal information, secrets, IPs, paths, and credentials
3. Generates a standalone README for the skill
4. Updates the repo's root README with the new skill entry
5. Commits and pushes

## Usage

```bash
# Share a skill (interactive — reviews sanitization before pushing)
~/agent-workspace/skills/skill-sharer/scripts/share-skill.sh <skill-folder-path> [--description "Short description"]
```

### Examples

```bash
# Share session-cleaner
~/agent-workspace/skills/skill-sharer/scripts/share-skill.sh ~/agent-workspace/scripts/session-cleaner/ --description "Converts session JSONL to clean markdown"

# Share a skill from the skills directory
~/agent-workspace/skills/skill-sharer/scripts/share-skill.sh ~/agent-workspace/skills/weather/ --description "Get weather forecasts with no API key"
```

## Sanitization rules

The script strips:
- **IP addresses** — Tailscale IPs, public IPs, local IPs (replaced with `<REDACTED_IP>`)
- **Paths with usernames** — `/home/user/`, `/home/user/` → generic paths
- **API keys and tokens** — anything matching key/token/secret patterns
- **Email addresses** — real emails replaced with `user@example.com`
- **SSH connection strings** — `ssh user@host` → `ssh user@<your-host>`
- **Server URLs with real hosts** — internal URLs replaced with placeholders
- **Secret file references** — `~/agent-workspace/secrets/*` → `<YOUR_SECRET_FILE>`
- **Tailscale hostnames** — machine names replaced
- **Environment variable values** — actual values stripped, variable names kept

## Agent workflow

When Henry asks to share a skill:

1. **Identify** the skill folder path
2. **Run** `share-skill.sh <path> --description "..."`
3. **Review** the sanitized output (script pauses for review)
4. **Confirm** to push
5. **Report** the GitHub URL to Henry

## Repo structure

```
Enterprise-Crew-skills/
├── README.md              ← Root index (auto-updated)
├── session-cleaner/
│   ├── README.md
│   └── ...
├── new-skill/
│   ├── README.md
│   └── ...
```
