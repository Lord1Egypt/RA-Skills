# Release Notes: wip-ldm-os v0.4.47

AIs now present release notes in plain language instead of developer changelog.

## What changed

- Updated SKILL.md to instruct AIs to translate developer release notes into user-facing language
- Added good/bad examples: "Your AIs now explain what LDM OS does" vs "Restored rich product content to SKILL.md"
- AIs should now answer "what changed for ME?" not "what did the developers do internally"

## Why

When dogfooding v0.4.46, the AI fetched release notes via `gh release view` and parroted back developer text: "dead weight audit", ".publish-skill.json iCloud path fix", "workspace-boundaries.md staff/ -> team/". None of that means anything to a user. The instruction now tells AIs to translate into Apple-style release notes.

## Issues closed

- #211

## How to verify

```bash
# In a fresh Claude Code session with LDM OS installed:
# Read https://wip.computer/install/wip-ldm-os.txt
# Check if LDM OS is already installed...
# AI should show user-facing release notes, not dev changelog
```
