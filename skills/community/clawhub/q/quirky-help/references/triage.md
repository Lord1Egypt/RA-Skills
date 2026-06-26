# Triage Guide

Classify the blocker before expanding the fix.

## Common buckets

- **UI confusion**: the user cannot tell what screen they are on or what to click.
- **Auth**: login expired, wrong account, missing permission, blocked verification.
- **Config**: wrong value, missing env var, stale endpoint, mismatched hostname, bad toggle.
- **Network**: timeout, DNS failure, unreachable host, proxy issue, offline state.
- **Install/dependency**: missing package, wrong version, failed build step, missing runtime.
- **Permissions/security**: denied access, sandbox restriction, file ownership, elevated action needed.
- **Product bug**: visible app behavior does not match expected flow after the obvious checks pass.

## Triage sequence

1. Find the exact visible symptom.
2. Find the narrowest likely category.
3. Check for the highest-probability mismatch first.
4. Give one to three concrete next actions.
5. Escalate only after the simple explanation fails.

## Good defaults

- Prefer exact text over paraphrase.
- Prefer reproduction steps over theory.
- Prefer one strong hypothesis over five weak ones.
- Ask for copied text when screenshots hide important detail.
