# Deployment Readiness Checklist

**Project**: {{project_name}}  
**Target Environment**: {{environment}} (staging / production)  
**Timestamp**: {{timestamp}}  
**Agent**: {{agent_id}}

---

## 🚦 Pre-Deployment Automated Checks

Run `./scripts/e2e.sh` (or individual steps):

- [ ] E2E pipeline passed (build → test → deploy → verify)
- [ ] Staging environment health: `/api/health` returns 200
- [ ] Database connectivity verified (can query primary tables)
- [ ] Frontend renders without errors (console clean)
- [ ] API rate limits configured (if applicable)
- [ ] Static assets (CSS/JS) have cache-busting hashes

**E2E output reference**:
```
{{e2e_output_link}}
```

---

## 🔐 Security & Access

- [ ] All secrets stored in environment variables or secret manager (none in code)
- [ ] `.env` file ignored by git (`.gitignore` includes it)
- [ ] API tokens / service accounts have least privilege (read-only if possible)
- [ ] CORS configured correctly (frontend origin allowed, not `*` in production if auth required)
- [ ] HTTPS enforced (no HTTP endpoints in production)
- [ ] No debug flags enabled (`DEBUG=` unset in production)

---

## 💾 Data & Database

- [ ] Database backup completed (staging: optional; production: mandatory)
  - Backup timestamp: _____________
  - Backup location: _____________
- [ ] Migration scripts tested on staging (if schema changes)
- [ ] Data retention policy applied (old data purge if needed)
- [ ] D1 / DB billing / quota not exceeded (capacity check)

---

## 📊 Monitoring & Observability

- [ ] Error reporting configured (Sentry / Logflare / custom)
- [ ] Metrics dashboard available (Grafana / Cloudflare Analytics)
- [ ] Alerts configured for:
  - [ ] Error rate > 1%
  - [ ] P95 latency > 1000ms
  - [ ] Data ingestion lag > 15 minutes
- [ ] Log retention set (at least 7 days)

---

## 🌐 Frontend & CDN

- [ ] Build succeeded (`npm run build` no errors)
- [ ] Assets uploaded / deployed (Pages deployment successful)
- [ ] Custom domain points to correct deployment (if applicable)
- [ ] SSL certificate valid (no expired certs)
- [ ] `index.html` has correct meta tags / title / description
- [ ] No broken links (run `link-checker` on deployed site)

---

## 🔙 Rollback Plan

**Rollback triggers**:
- [ ] Error rate > 5% for 5 minutes
- [ ] Critical bug reported by users
- [ ] Performance degradation > 50%

**Rollback steps** (customize for your deployment platform):
1. Service rollback: `{{your_deploy_tool}} rollback --version {{previous_version}}`
2. Frontend rollback: `{{your_deploy_tool}} rollback --project {{project}} --branch {{previous_branch}}`
3. Database rollback (if needed): `{{your_db_tool}} restore --backup {{backup_uuid}}`
4. Verify rollback health: curl `/api/health` and check frontend

**Rollback drill performed?** ✅ / ❌ (recommended on staging before first production deploy)

---

## 📣 Communication

- [ ] Stakeholders notified of deployment window (email sent to: _____________)
- [ ] Maintenance page ready (if downtime expected)
- [ ] Post-deployment announcement prepared ("All systems go" or "Issue identified")

---

## ✅ Go/No-Go Decision

**Deployment authorized?**
- ✅ **YES — proceed with deployment**
- ⏸️ **DEFERRED** (schedule for later: _____________)
- ❌ **NO — fix issues first** (see reasons below)

**Deployment window**: _____________ (if constrained)  
**Approved by**: _____________  
**Timestamp**: _____________

---

### ⚠️ Issues / Risks (if any)

```
{{issues_list}}
```

**Mitigation plan** (if deploying with known issues):
```
{{mitigation}}
```
