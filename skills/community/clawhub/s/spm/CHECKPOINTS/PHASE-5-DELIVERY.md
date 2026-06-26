# Checkpoint: Phase 5 — Delivery & Deployment Gate

**Project**: {{project_name}}  
**Checkpoint**: Phase 5 — Delivery  
**Timestamp**: {{timestamp}}  
**Agent**: {{agent_id}}

---

## 📋 Pre-Deployment Verification

### Automated E2E Test Results

Run `./scripts/e2e.sh` and attach summary:

```
{{e2e_output}}
```

**Status**: ✅ PASS / ❌ FAIL

If FAIL, list failing tests:
```
{{failed_tests}}
```

---

## 🔍 Final Quality Checklist

**Tier 1 — Always Do**
- [ ] All tests pass (`npm test` green)
- [ ] Type check passes (`npm run type-check`)
- [ ] Lint passes (`npm run lint`)
- [ ] No secrets in codebase (`grep -r "API_KEY\|SECRET" src/` clean)
- [ ] Environment variables documented (`.env.example` up to date)
- [ ] `docs/API.md` matches deployed API (or generated from spec)
- [ ] README updated with usage instructions
- [ ] CHANGELOG updated (if public project)

**Tier 2 — Ask First** (Production deployment only)
- [ ] Database backup taken (timestamp: _____________)
- [ ] Rollback plan documented (how to revert within 10 minutes)
- [ ] Monitoring/alerting configured (errors → Slack/Email)
- [ ] Performance baseline established (p95 latency, error rate)
- [ ] Stakeholders notified (email sent to: _____________)

---

## 📦 Artifacts to Deploy

| Artifact | Version / Hash | Destination | Verified? |
|----------|----------------|-------------|-----------|
| Backend service | {{backend_version}} | {{deploy_target}} | ✅ / ❌ |
| Database | {{db_version}} | {{db_target}} | ✅ / ❌ |
| Frontend site | {{frontend_version}} | {{deploy_target}} | ✅ / ❌ |
| Scripts / Tools | {{script_version}} | GitHub / CI | ✅ / ❌ |

---

## 💬 Deployment Plan

**Target environment**: {{environment}} (staging / production)  
**Deployment window**: {{window}} (if production)  
**Deployment method**: (e.g., `wrangler deploy`, GitHub Actions)

**Rollback procedure** (brief):
```
{{rollback_steps}}
```

---

## ✅ User Confirmation

**Do you authorize deployment to {{environment}}?**

- ✅ **Yes, deploy now**
- ⏳ **Schedule later** (deploy at: _____________ )
- ❌ **Hold — fix issues first**

**Additional notes / special instructions**:
```
{{user_notes}}
```

**Confirmation timestamp**: _____________  
**Confirmed by**: _____________

---

### 🛠️ Agent Next Actions

If confirmed to deploy now:
1. Run deployment commands (see `workflows/shipping-and-launch.md`)
2. Monitor deployment health (`wrangler tail`, Pages analytics)
3. Run post-deployment smoke test (curl health endpoint, check Pages)
4. Update `project_state.json` status to `deployed`
5. Notify stakeholders (if configured)

If scheduled:
1. Add to calendar / CI schedule
2. Set reminder 15 minutes before window
3. Re-run this checkpoint at scheduled time
