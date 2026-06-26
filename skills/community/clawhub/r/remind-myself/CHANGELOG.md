# Changelog

## 1.0.6

Rewrite description to be a proper trigger phrase (remove system prompt hack). Declare `openclaw` in `requires.bins`. Add confirmation step before scheduling. Fix install slug.

## 1.0.5

Add remind.sh script that handles cron creation, chat ID resolution, and verification. Simplify SKILL.md to just call the script.

## 1.0.4

Add mandatory step to resolve Telegram chat ID from TOOLS.md before creating cron job. Mark --to flag as critical.

## 1.0.3

Fix cron command: use --session isolated + --message instead of --token + --system-event.

## 1.0.2

Add cron verification step and explicit error handling rules.

## 1.0.1

Translate all prompts and examples to English.

## 1.0.0

Initial release.
