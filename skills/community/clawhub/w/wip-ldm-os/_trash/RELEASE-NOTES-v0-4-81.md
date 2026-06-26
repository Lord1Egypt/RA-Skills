# Release Notes: wip-ldm-os v0.4.81

## Installer reliability

This patch prevents `ldm install` from deploying malformed agent skill files.

`installSkill()` now validates `SKILL.md` frontmatter before copying a skill into LDM, Claude Code, OpenClaw, or Codex skill directories. If frontmatter is malformed, the installer refuses that skill deployment and reports the source path plus the exact line that failed.

## Fixed case

The regression that triggered this release was an unquoted YAML scalar:

```yaml
description: Read when: guard blocks a tool call
```

That shape can make Codex skip loading the entire skill. The fixed installer catches it before deployment, and the valid quoted form still passes:

```yaml
description: "Read when: guard blocks a tool call"
```

## Verification

- `node --check lib/deploy.mjs`
- `node --check scripts/test-skill-frontmatter.mjs`
- `npm run test:skill-frontmatter`

## Tracking

- Public issue: #270, https://github.com/wipcomputer/wip-ldm-os/issues/270
- Private bug file: `ai/product/bugs/installer/2026-04-24--codex--installer-deploys-invalid-skill-yaml.md`
