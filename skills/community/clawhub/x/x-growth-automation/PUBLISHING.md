# ClawHub Publishing Guide

## Recommended initial release

- **Slug:** `x-growth-automation`
- **Display name:** `X Growth Automation`
- **Version:** `0.1.0`
- **Tags:** `latest,x,twitter,automation,growth,openclaw`

## Why this slug?
It matches the skill folder and reads cleanly on ClawHub.
A quick search did not show an obvious exact conflict at preparation time.

## Pre-publish checklist

- [x] `SKILL.md` exists
- [x] bilingual `README.md` exists
- [x] setup questionnaire exists
- [x] rollout guide exists
- [x] scaffold script exists and was tested
- [x] no private Telegram/group hardcoding remains
- [x] skill packaged successfully once

## Publish command

Run from the skill folder or use the absolute path:

```bash
clawhub publish /root/.openclaw/workspace/public-skills/x-growth-automation \
  --slug x-growth-automation \
  --name "X Growth Automation" \
  --version 0.1.0 \
  --tags latest,x,twitter,automation,growth,openclaw \
  --changelog "Initial public release: multilingual X automation skill scaffold with setup questionnaire, rollout guidance, and reusable project generator."
```

## Suggested next versions

- `0.1.1` → docs polish / wording fixes
- `0.2.0` → more scaffold options, more presets
- `0.3.0` → stronger multilingual and source-branching templates

## GitHub repo

- <https://github.com/roskva000/openclaw-x-automation-skill>

## Notes

- This public skill is intentionally generic.
- Community CTA, source branching, niche, and language are user-configured at setup time.
- Do not add private production links or private community assumptions before publishing.
