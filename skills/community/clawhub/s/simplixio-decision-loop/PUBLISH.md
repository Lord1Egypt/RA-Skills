# Publish Notes

## Local install

Place this folder in one of these locations:

- `<workspace>/skills/simplixio-decision-loop`
- `~/.openclaw/skills/simplixio-decision-loop`

Then restart OpenClaw or run the relevant skills refresh command.

## Validate

From the workspace root:

```bash
openclaw skills list
openclaw skills check
```

## Publish to ClawHub

Install the ClawHub CLI if needed:

```bash
npm i -g clawhub
```

Login:

```bash
clawhub login
```

Publish:

```bash
clawhub publish --skill ./skills/simplixio-decision-loop
```

## Notes

ClawHub skills are text-based bundles. Keep this skill small, readable, and safe.
