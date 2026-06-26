# Change Proposals

## #001 - Fix Stop hook JSON schema (hookSpecificOutput not supported)
- **Status:** implemented
- **Date:** 2026-05-06
- **Trigger:** Stop hook threw validation error in production — `hookSpecificOutput` is only valid for PreToolUse/PostToolUse/UserPromptSubmit, not Stop
- **Proposal:** Replace `hookSpecificOutput` with `systemMessage` in check-skill-candidate.sh
- **Breaking?:** no
- **Resolution:** Fixed in commit cf0386b

## #002 - Add hook output validation test
- **Status:** implemented
- **Date:** 2026-05-06
- **Trigger:** #001 was a preventable bug — no schema validation was done before deployment
- **Proposal:** Add a `scripts/test-hooks.sh` that validates both hook scripts' JSON output against the Claude Code schema before committing. Run it as a pre-commit check or manual verification step.
- **Breaking?:** no
