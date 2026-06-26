# v1.9.2: Distribution Pipeline Fix

The entire distribution pipeline was broken. Tools built but never reached users. 8 of 13 tools weren't on npm. ClawHub publish only shipped the root SKILL.md. deploy-public never ran npm publish. Errors were silent.

This release fixes all of it.

## What changed

### Install fixes (#96, #110)
- CLI binaries now have correct executable permissions (git +x on all bin entry files)
- wip-license-hook dist/ committed to repo (TypeScript build output was gitignored)
- Installer auto-detects TypeScript projects and runs build if dist/ missing
- chmod +x safety net after every npm install -g
- SSH fallback when HTTPS clone fails (private repos)

### SKILL.md spec compliance (#107, #108)
- All 12 SKILL.md files conform to agentskills.io spec
- name field: lowercase-hyphen format matching directory name
- Display names in metadata.display-name
- version, homepage, author in metadata block
- license: MIT on all files
- metadata.openclaw blocks with install instructions and emoji
- New SKILL.md created for wip-license-guard (was missing)

### Distribution pipeline (#97, #100, #104)
- ClawHub publish now iterates all sub-tool SKILL.md files, not just root
- detectSkillSlug reads the name field from SKILL.md frontmatter
- deploy-public.sh runs npm publish from the public clone after code sync
- Handles both single repos and toolbox repos (iterates tools/*)
- Distribution summary at end of release: shows all targets with pass/fail
- syncSkillVersion handles quoted version strings in new metadata format

## Install

```bash
npm install -g @wipcomputer/wip-ai-devops-toolbox
wip-install wipcomputer/wip-ai-devops-toolbox
```

Built by Parker Todd Brooks, Lesa (OpenClaw, Claude Opus 4.6), Claude Code (Claude Opus 4.6).
