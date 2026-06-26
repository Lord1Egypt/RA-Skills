# CLAUDE.md

## Keep SKILL.md and AGENTS.md in sync

`SKILL.md` (Claude Code) and `AGENTS.md` (other agent runtimes) are parallel entry points for the same skill and must stay in sync in content and structure. Any substantive change to one must be mirrored in the other in the same commit — including the description, "What can you do" intro, "Before you start" setup, "Documentation lookup" routing, and "Guardrails". Format differences are fine (e.g., SKILL.md has YAML frontmatter, AGENTS.md has a `<!-- version: -->` comment), but the meaning, ordering, and coverage must match. If a section exists in one file, it should exist in the other unless there's an explicit reason it doesn't apply.

## Version bumping

Only bump the skill version **once, at the very end** of a change — after all edits are finalized and the user has confirmed they're done. Do not bump mid-change, do not bump after each individual edit, and do not bump speculatively. If the user is still iterating, hold off.

When bumping at the end, update all four places in the same commit:

1. `CHANGELOG.md` — add a new version entry at the top with a summary of changes
2. `SKILL.md` — update the `version:` field in the frontmatter metadata
3. `AGENTS.md` — update the `<!-- version: x.x.x -->` comment
4. `.claude-plugin/plugin.json` — update the `"version"` field

## `references/` are offline-fallback snapshots, not the source of truth

Live docs at `docs.tensorlake.ai` (indexed by [llms.txt](https://docs.tensorlake.ai/llms.txt)) are primary. The files under `references/` are bundled snapshots that the skill points agents at only when network access is unavailable. Some drift between snapshot and live doc is expected; it is not a release blocker. The `Documentation lookup` section in SKILL.md / AGENTS.md, and `references/feature_lookup.md`, are the entry points — keep them coherent with the actual files in `references/`.

When you add, remove, or rename a snapshot file under `references/`, update `references/feature_lookup.md` and `.github/scripts/sources.yaml` in the same commit. Any feature/keyword that was reachable through the old file must still resolve to a snapshot via `feature_lookup.md`.

## SDK version and Last verified go together

Every snapshot under `references/` and every entry in `.github/scripts/sources.yaml` has a paired `SDK version:` / `sdk_version:` and `Last verified:` / `last_verified:` field. These must always move together: if you bump one, bump the other in the same commit. Bumping only the SDK version leaves a lie in the date field — the record claims someone verified against a newer SDK on an older date, which is worse than not bumping at all.

Apply this rule whenever:

- You update a snapshot's `SDK version:` header after a PyPI release
- You edit a snapshot's content to reflect new/changed docs
- You change any URL in that snapshot's `Source:` list (or its entry in `sources.yaml`)

In all three cases, set `Last verified:` to today's date in the same edit, and mirror the same date to the corresponding `last_verified:` field in `sources.yaml`. The `README.md` illustrative example header should also be kept current.

`references/feature_lookup.md` is a curated index, not a doc-page snapshot. It has no `SDK version` / `Last verified` fields and no `sources.yaml` entry; this rule does not apply to it.
