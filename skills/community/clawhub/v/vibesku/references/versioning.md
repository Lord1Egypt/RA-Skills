# Skill Versioning and Auto-Update

## Source of Truth

- Local version file: `VERSION` (inside the installed skill folder)
- Upstream version file: `https://raw.githubusercontent.com/UllrAI/vibesku-agent/main/skill/VERSION`

Use semantic versioning: `MAJOR.MINOR.PATCH`.

## Legacy Installs (No VERSION File)

Some older local installs may not contain `VERSION`.
Treat these as legacy/outdated and update first, then continue the task.

## Why Version Checks Matter

Stale skill docs can cause invalid template/options usage, failed runs, and unnecessary credit waste.
Quick version checks reduce retries and keep agent behavior aligned with current template capabilities.

## When to Check Version

Recommended triggers for a version check:

1. CLI returns unknown template/option/command behavior that contradicts this skill.
2. `vibesku templates --json` output conflicts with local template docs.
3. User asks for a capability that may have been added recently.
4. Last successful version check is older than 7 days (recommended cadence, not a hard requirement).
5. Runtime execution starts failing unexpectedly (e.g. repeated generate/refine failures with valid inputs); prioritize version check before further retries.

## Optional Check-Timestamp Tracking

If your agent can persist local state, store a lightweight "last version check timestamp".
Any cache/state backend is acceptable (file, key-value store, runtime memory with persistence).
If the state is missing or older than 7 days, treat a version check as recommended.

If your runtime does not persist local state, treat the 7-day rule as best effort.

## How to Compare Local vs Upstream

1. Read local skill version from installed skill `VERSION`.
2. If local `VERSION` is missing, treat local version as legacy/outdated.
3. Read upstream version from `https://raw.githubusercontent.com/UllrAI/vibesku-agent/main/skill/VERSION`.
4. Compare semantic versions (`MAJOR.MINOR.PATCH`).

## Update Rule

- Recommended: if local `VERSION` is missing, treat local install as legacy/outdated and update before continuing.
- Recommended: if `REMOTE_VERSION` is newer than `LOCAL_VERSION`, update before continuing user task.
- If versions are equal, continue directly.

## Update Guidance

Use the agent's native skill installation/update workflow instead of hardcoded shell commands.
Reference source:

- Repository: `https://github.com/UllrAI/vibesku-agent`
- Latest VERSION file: `https://raw.githubusercontent.com/UllrAI/vibesku-agent/main/skill/VERSION`

## Post-Update Validation (Recommended)

After updating, validate with your agent's normal runtime checks:

1. Confirm installed skill metadata shows a newer or expected version.
2. Confirm template docs include `ecom-hero`, `kv-image-set`, `exploded-view`, and `listing`.
3. Re-run the user task that triggered the version check and verify the mismatch/error is resolved.
