# Bug: installer deploys invalid skill YAML frontmatter

**Date:** 2026-04-24
**Filed by:** Codex + Lēsa
**Component:** LDM OS installer (`lib/deploy.mjs`)
**Severity:** High
**Public issue:** https://github.com/wipcomputer/wip-ldm-os/issues/270
**Status:** Open. Fix implemented in worktree, pending PR merge and release.

## Summary

`ldm install --alpha --yes` deployed `wip-branch-guard/SKILL.md` into `~/.codex/skills/wip-branch-guard/SKILL.md` with invalid YAML frontmatter. Codex then skipped loading the skill:

```text
Skipped loading 1 skill(s) due to invalid SKILL.md files.
/Users/lesa/.codex/skills/wip-branch-guard/SKILL.md: invalid YAML: mapping values are not allowed in this context
```

The immediate source bug is an unquoted frontmatter field:

```yaml
description: ... Read when: a tool call was denied ...
```

The colon in `Read when:` is legal text, but not legal in an unquoted YAML scalar for the parser Codex uses.

## Why it matters

The installer is the distribution boundary. If it copies a malformed `SKILL.md` into Claude Code, OpenClaw, or Codex skill directories, the tool can be installed and healthy while the agent instruction layer silently disappears.

This is especially bad for guard and repo tools because their skills carry the operational workflow agents need to recover from blocks safely.

## Root cause

`installSkill()` copies `SKILL.md` to:

- `~/.ldm/extensions/{tool}/SKILL.md`
- `~/.claude/skills/{tool}/SKILL.md`
- `~/.openclaw/skills/{tool}/SKILL.md`
- `~/.codex/skills/{tool}/SKILL.md`

It does not validate the frontmatter before copying. It only checks that the file exists.

## Required fix

1. Add a `validateSkillFrontmatter()` helper in `lib/deploy.mjs`.
2. Before any copy in `installSkill()`, validate that:
   - the file starts with `---`
   - it has a closing `---`
   - top-level `key: value` lines are parseable enough for common agent skill frontmatter
   - unquoted scalar values containing `: ` are rejected with a useful message
3. On validation failure:
   - do not copy the skill to LDM, Claude Code, OpenClaw, or Codex
   - print the source path and exact line that failed
   - continue installing other interfaces where safe
4. Add a regression test with a bad `description: Read when: ...` frontmatter file.
5. Fix the source `wip-branch-guard/SKILL.md` by quoting the `description` value.
6. Reinstall alpha and verify Codex no longer reports skipped invalid skills.

## Acceptance criteria

- `ldm install` refuses to deploy a malformed `SKILL.md`.
- The refusal includes the bad file path and line number.
- A valid quoted description deploys normally.
- `~/.codex/skills/wip-branch-guard/SKILL.md` has valid frontmatter after reinstall.
- A new Codex session no longer shows the invalid `wip-branch-guard/SKILL.md` warning.

## Implementation note

The installer fix adds `validateSkillFrontmatter()` in `lib/deploy.mjs` and calls it inside `installSkill()` before dry-run reporting or any copy into LDM, Claude Code, OpenClaw, or Codex skill directories.

The regression command is:

```bash
npm run test:skill-frontmatter
```

## Related

- Public tracker: https://github.com/wipcomputer/wip-ldm-os/issues/270
- Guard plan: `ai/product/bugs/guard/2026-04-24--codex--guard-and-repo-tools-master-plan.md`
- Source skill: `devops/wip-ai-devops-toolbox-private/tools/wip-branch-guard/SKILL.md`
- Installer deploy path: `wip-ldm-os-private/lib/deploy.mjs`
