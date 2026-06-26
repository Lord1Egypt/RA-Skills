# Checkpoint: Phase 4 — Quality Gate

**Project**: {{project_name}}  
**Checkpoint**: Phase 4 — Quality  
**Timestamp**: {{timestamp}}  
**Agent**: {{agent_id}}

---

## 📋 Deliverables Reviewed

- [ ] All WBS tasks marked `done` ({{done_count}}/{{total_count}} completed)
- [ ] Full test suite passes (`npm test` green)
- [ ] Lint clean (`npm run lint` zero errors)
- [ ] Type check passes (`npm run type-check` zero errors)
- [ ] Code review completed for all changed files

---

## 🔍 Three-Stage Code Review Summary

### Stage 1: Spec Compliance
- [ ] All tasks match spec exactly — no YAGNI violations
- [ ] All acceptance criteria verified with fresh evidence

### Stage 2: Engineering Quality
- [ ] Tests cover new code (target ≥ 80%)
- [ ] No hardcoded secrets or unsafe patterns
- [ ] Clean code: no console.log, no TODO, no magic numbers
- **Findings**: {{review_summary}}

### Stage 3: Final Verification
- [ ] Full test suite: {{test_output}}
- [ ] Lint: {{lint_output}}
- [ ] No regressions detected
- [ ] All WBS evidence collected and verified

---

## 🛡️ Quality Gates

**Tier 1 — Always Do**
- [ ] All tests passing
- [ ] Naming conventions followed
- [ ] Input validation present
- [ ] Documentation synced

**Tier 2 — Ask First (verify all approved)**
- [ ] Database changes reviewed and approved
- [ ] New dependencies approved
- [ ] API contract changes approved
- [ ] CI/CD modifications reviewed

**Tier 3 — Never Do (verify none)**
- [ ] No secrets in code or git history
- [ ] No skipped reviews for complex changes
- [ ] No force-push to shared branches
- [ ] No removed tests without approval

---

## 💬 Issues & Risks

```
{{issues_list}}
```

---

## ✅ User Confirmation

**Is the quality gate satisfied and ready to proceed to delivery?**

- ✅ **Yes, proceed to Phase 5 (Delivery)**
- ⏳ **Need fixes** (see comments below)
- ❌ **Blocked — quality issues must be resolved**

**Comments**:
```
{{user_comments}}
```

**Confirmation timestamp**: _____________  
**Confirmed by**: _____________
