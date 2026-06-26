# SHIP.md — OpenClaw Guard Skill v2.1 (Clawhub)

## Purpose
Ship the **OpenClaw Guard Skill v2.1** via Clawhub. This skill provides the UX surface and operational tooling for VAIBot Guard. It is intentionally redundant with the OpenClaw plugin and MCP server; the skill delivers a simple, opinionated interface for configuration, status, and local operator workflows.

## Release Summary
- **Product:** OpenClaw Guard Skill (v2.1)
- **Distribution:** Clawhub
- **Status:** In progress (pre-publish validation underway)
- **Scope:** Skill-only distribution (plugin already shipped separately)

## What’s In v2.1
- Skill wrapper for VAIBot Guard workflows
- Operator-facing commands / scripts / docs
- Default policy templates + examples
- Local testing instructions aligned with v2.1 governance posture

## What’s Out of Scope
- Plugin enforcement (already shipped)
- API / MCP server (already shipped)
- Any data-plane or backend change

## Packaging Checklist
- [x] Confirm skill contents (no runtime logs)
- [x] Ensure `SKILL.md` + `scripts/` + `references/` included
- [x] Confirm systemd templates are **not** in `systemd/*.service` (Clawhub strips them)
  - [x] Placed under `references/systemd/*.service.txt`
- [ ] Update changelog section in `SKILL.md` (if applicable)
- [ ] Verify version number for Clawhub publish

## Build Artifact (.skill)
From skill directory:

```bash
cd /home/cybercampbell/clawd/vaibot-v2/packages/openclaw-guard-skill

# Build .skill bundle (zip archive with .skill extension)
zip -r -X /home/cybercampbell/clawd/output-skills/openclaw-guard-skill.skill . \
  -x ".git/*" ".vaibot-guard/*" "tests/*"
```

## Publish to Clawhub
```bash
cd /home/cybercampbell/clawd/vaibot-v2/packages/openclaw-guard-skill

clawhub publish . \
  --slug openclaw-guard-skill \
  --name "OpenClaw Guard Skill" \
  --version 2.1.0 \
  --changelog "Ship v2.1 skill wrapper for VAIBot Guard" \
  --tags latest
```

## Post-Ship Validation
- [ ] `clawhub info openclaw-guard-skill` shows v2.1.0
- [ ] Install from Clawhub in a clean environment
- [x] Run unit tests: `node --test tests/guard-service.test.mjs`
- [ ] Run quick smoke test commands from `SKILL.md`
- [ ] Confirm any required service/unit templates are accessible via `references/`

## Notes
- This skill is intentionally redundant with the plugin and MCP server; it is a **distribution + UX surface** only.
- Any enforcement logic must remain in the OpenClaw plugin.
