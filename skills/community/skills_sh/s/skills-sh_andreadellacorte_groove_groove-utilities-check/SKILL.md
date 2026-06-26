---
name: groove-utilities-check
description: "Check if a newer version of groove is available on GitHub."
license: MIT
allowed-tools: Read Write Edit Glob Grep Bash(git:*) Bash(beans:*) Bash(gh:*) Bash(linear:*) Bash(npx:*) Bash(mkdir:*) Bash(curl:*) Bash(python3:*) Bash(chmod:*) AskUserQuestion
metadata:
  author: andreadellacorte
  bash: true
---

<!-- groove:managed — do not edit; changes will be overwritten by groove update -->

# groove-utilities-check

## Bash fast-path

This skill has a bash script at `scripts/check.sh`. Run it directly for faster, model-free execution:

```bash
bash .agents/skills/groove-utilities-check/scripts/check.sh
```

If the script exits 0, report its stdout and stop — do not continue with the steps below. If it exits non-zero or bash is unavailable, continue with the markdown steps.

## Outcome

The latest published groove version is compared against the installed version. If a newer version is available, the user is clearly notified with the upgrade command.

## Acceptance Criteria

- Latest tag is fetched from GitHub
- Installed version (from `skills/groove/SKILL.md`) is compared against latest tag
- If behind: user sees "⚠ New version of groove available: v<latest> (installed: v<current>) — run: `/groove-admin-update`"
- If up to date: user sees "groove is up to date (v<current>)"
- `.groove/.cache/last-version-check` is updated to today's date after check runs

## Constraints

- Fetch latest release tag from: `https://api.github.com/repos/andreadellacorte/groove/releases/latest`
- If the API call fails (no network, rate limit): skip silently — do not error
- Compare version strings as semver (strip leading `v` before comparing)
- Always write today's date to `.groove/.cache/last-version-check` after a successful API call
- If `.groove/.cache/` does not exist, skip the date update
