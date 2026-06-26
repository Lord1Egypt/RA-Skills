---
name: auto-xiaoya-doing
description: Automate login and page capture for WHUT AI Augmented sites using agent-browser. Use when handling whut.ai-augmented.com or its subdomains, especially to open a target page, close blocking popups, fill login credentials from a local secret file or environment variables, verify login state, and capture current page text/questions for later processing.
---

# Auto Xiaoya Doing

Use this skill to open WHUT AI Augmented pages in an authenticated browser session and dump the current page text for downstream analysis.

## Workflow

1. Ensure credentials are available before running the script.
2. Run `scripts/whut-open "URL"` for a target page, or run it without arguments to open the site root.
3. Read `references/workflow.md` for the operating conventions if follow-up browser automation is needed.
4. Read `latest_page_dump.json` after execution to inspect captured page text and extracted questions.

## Credential sources

The login script supports these credential sources, checked in this order:

1. `WHUT_USERNAME` and `WHUT_PASSWORD` environment variables
2. `WHUT_SECRET_PATH` environment variable pointing to a JSON file with `username` and `password`
3. `./local/whut_ai_secret.json` inside this skill folder

Do not package real credentials with the skill.

## Bundled files

- `scripts/auto_login.py`: main automation logic
- `scripts/whut-open`: convenience wrapper
- `references/workflow.md`: usage conventions and follow-up operating notes

## Notes

- Keep secrets in `local/whut_ai_secret.json` or environment variables.
- Treat `latest_page_dump.json` as runtime output, not as reference content to distribute.
- If refs become stale during browser automation, take a fresh snapshot before continuing.
