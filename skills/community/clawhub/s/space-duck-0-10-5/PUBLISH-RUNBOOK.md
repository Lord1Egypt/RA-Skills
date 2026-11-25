# PUBLISH RUNBOOK — space-duck 0.10.5 (staged 2026-10-25, publish HELD)

**Hold condition:** ClawHub scan gate holds every space-duck version ≥0.10.1
(openclaw/clawhub#4044). Do NOT publish 0.10.5 until **0.10.4 reads 200** on
the registry read side. Never bump the fleet pointer to a version that is not
read-side 200.

**Gate check (run first, every time):**
```bash
curl -s "https://clawhub.ai/api/v1/skills/space-duck/versions" \
  | python3 -c "import json,sys; print([i['version'] for i in json.load(sys.stdin)['items']][:5])"
# Gate cleared when 0.10.4 (or any 0.10.1+) appears. As of staging: ['0.10.0', ...] = still held.
```

**What 0.10.5 is:** 0.10.4 baseline (git `1cc37a7e`) + exactly 3 files:
`scripts/peck_listener.py` (update-notice responder exemption, [AUTOUP-EXEMPT]),
`references/grants.md` (check→deny recovery section), `CHANGELOG.md` (0.10.5
entry). Rig: `coordination/rig_update_notice_0105.py` (27 checks, all green
2026-10-25). Worker report: `coordination/WORKER-0105-REPORT.md`.
Staging `_meta.json` already says 0.10.5. The live `skills/space-duck/` git
tree carries the same 3 hunks (committed); its `_meta.json` stays 0.10.4 until
this runbook completes.

## Publish sequence (only after gate clears)

1. **Re-verify artifact** — staging diff vs `1cc37a7e` must still be exactly
   the 3 files + `_meta.json`; `python3 coordination/rig_update_notice_0105.py`
   must exit 0. No `__pycache__`/`*.pyc` anywhere in staging (`.gitignore` is
   present; packer honors it).
2. **skill-card.md guard** — `mv skills-staging/space-duck-0.10.5/skill-card.md /tmp/`
   before publish (ClawHub guard rejects shipped skill-card.md); restore after.
3. **Publish space-duck** (inside container, HOME=/data already authed as askegor;
   path must be under the workspace):
   ```bash
   clawhub publish skills-staging/space-duck-0.10.5 --version 0.10.5 \
     --tags "latest,space-duck,lane-a" \
     --changelog "0.10.5 [AUTOUP-EXEMPT]: update_request system notices exempt from --on-peck responder (grant-notice doctrine); grants.md documents check->deny recovery (v1104 next_step hint; only revoked = stop). Lockstep relay no-op bump."
   ```
4. **Publish relay lockstep** — `skills/space-duck-kimi-relay` no-op bump to
   0.10.5: sync its `_meta.json` version, add CHANGELOG line, purge pycache,
   same publish command with `--tags "latest,kimi,lane-a,space-duck"`.
5. **Verify read-side 200 BOTH skills** (index lag up to ~15 min — do NOT
   panic-republish; phantom slots exist: 0.10.1, 0.10.2 — if 0.10.5 lands
   phantom, bump past it, never republish into the slot).
6. **Sync live tree:** `skills/space-duck/_meta.json` → 0.10.5; restart JP's
   listener (host-side) so the pulse reports 0.10.5 (memory:
   reference_skill_version_reporting_meta).
7. **Pointer bump:** new `coordination/deploy_skill_latest_0105.py` following
   the 0911/094 pattern — base zip on the LIVE prod Lambda package (never the
   repo tree), swap only the pointer line, publish version, flip `prod` alias.
   Verify `curl https://beak.spaceduckling.com/beak/skill/latest` → 0.10.5.
   Record old alias version for rollback.
8. **Git:** commit _meta/CHANGELOG syncs + DEPLOY-LOG entry; push `clean-origin`
   (branch + ff `main`) per the ship checklist.
9. **Field test:** Grok Bot 1 asked to re-test the MC update card when a new
   version goes live — one tap on his card's "Queue update peck" exercises the
   whole Stage-2 lane; also proves THIS release's responder exemption on any
   responder duck that receives the update notice.
10. **Report to Josh** with version IDs, pointer proof, rollback line.
