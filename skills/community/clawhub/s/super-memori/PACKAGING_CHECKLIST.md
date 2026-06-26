# Packaging Checklist — super-memori

Before setting publish-ready state, confirm:
- [x] Package root contains `SKILL.md`
- [x] Package root contains `_meta.json`
- [x] Package root contains `.clawhubignore`
- [x] Package root contains `CHANGELOG.md`
- [x] Package root contains `PACKAGING_CHECKLIST.md`
- [x] Package root contains required public entrypoints: `query-memory.sh`, `memorize.sh`, `index-memory.sh`, `health-check.sh`
- [x] Package root contains the startup self-heal entrypoint: `startup-self-check.sh`
- [x] Package root contains the session-start hook assets: `hooks/super-memori-session-start/HOOK.md` and `hooks/super-memori-session-start/handler.js`
- [x] Maintenance-only entrypoints are present and documented without being mistaken for weak-model public commands: `audit-memory.sh`, `repair-memory.sh`, `list-promotion-candidates.sh`, `validate-release.sh`
- [x] Package root contains required runtime helper code under `scripts/`
- [x] Package root contains required references used by the skill
- [x] Publish evidence files exist under `references/verification-evidence.md` and `references/reference-test-log.md`
- [x] `.clawhubignore` excludes transient/local state (`.clawhub/`, `__pycache__/`, `*.pyc`, `*.tmp`, `*.pending`, `*.lock`, `.index_state`, `backups/`, full `reports/` review artifacts, `reports/test-generated/`, and root temporary validation leftovers such as `tmp_round2_strict.txt`)
- [x] Skill heading version matches `_meta.json`
- [x] Release health policy is explicit: `FAIL` blocks publish; `WARN` is allowed only when it reflects documented optional/degraded host conditions and the release surface does not imply semantic-ready or fully healthy baseline
- [x] If release proceeds while the reference host is in `WARN`, the qualification is recorded deterministically from observed health-check fields/state, not free-text intuition alone
- [x] If release proceeds while the reference host is in `WARN`, `CHANGELOG.md` explains why that WARN is still compatible with honest publication
- [x] Stable promotion is blocked until an equipped host passes `references/stable-host-readiness.md`; candidate publication may proceed with explicit host-state qualification
- [x] No fake `.clawhub/origin.json` is created before a real publish; publish metadata is synced only after actual ClawHub publication

Release checks (workspace context, not isolated package-root context):
- `python3 skills/skill-creator-canonical/scripts/quick_validate.py skills/super_memori`
- `python3 skills/skill-creator-canonical/scripts/validate_weak_models.py skills/super_memori`
- `cd skills/super_memori && ./health-check.sh`
- `cd skills/super_memori && ./validate-release.sh --strict`
- `cd skills/super_memori && ./tests/regression/run-all.sh`
- `test -f skills/super_memori/_meta.json`
- `test -f skills/super_memori/.clawhubignore`
- `test -f skills/super_memori/CHANGELOG.md`
- `test -f skills/super_memori/PACKAGING_CHECKLIST.md`
- `test -f skills/super_memori/startup-self-check.sh`

Publish gate note:
- Treat the checklist as a support surface, not the source of truth. Real publish-readiness requires the actual package tree plus strict validation to agree in the intended OpenClaw workspace context.
- `validate-release.sh --strict` is a workspace-coupled release gate: it depends on sibling validator tooling under `../skill-creator-canonical/` and is not designed as an isolated package-directory check.
- If any checked file listed above is missing from the real package root, block publish and advance to a new version instead of mutating an already-published line.
