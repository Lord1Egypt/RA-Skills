# Checkpoint: Phase 3 — Execution Milestone

**Project**: {{project_name}}  
**Checkpoint**: Phase 3 — Execution (Milestone: {{milestone_name}})  
**Timestamp**: {{timestamp}}  
**Agent**: {{agent_id}}

---

## 📋 Milestone Deliverables

**Milestone**: {{milestone_name}} (Task IDs: {{task_ids}})

Completed tasks in this milestone:

| ID | Task | Completed At | Evidence |
|----|------|--------------|----------|
| {{task_id_1}} | {{task_name}} | {{timestamp}} | {{evidence_path}} |
| {{task_id_2}} | {{task_name}} | {{timestamp}} | {{evidence_path}} |
| ... | ... | ... | ... |

---

## 🔍 Quality Gates — Milestone Level

**Tier 1 — Always Do**
- [ ] All completed tasks passed their exit criteria (checked against checklist)
- [ ] Code committed to feature branch (not local only)
- [ ] No secrets in code (`grep -r "API_KEY\|SECRET" src/` clean)
- [ ] Tests added/updated for new functionality
- [ ] Documentation updated (if public APIs changed)

**Tier 2 — Ask First** (if applicable)
- [ ] Database schema changes reviewed (run migration dry-run)
- [ ] New dependencies approved (`package.json` diff reviewed)
- [ ] Performance impact assessed (p95 latency < threshold)

**Tier 3 — Never Do** (verify none)
- [ ] No `console.log` left in production code
- [ ] No force-push to shared branches
- [ ] No credentials in git history (checked with `trufflehog` or equivalent)

---

## 📊 Test & Coverage Summary

- **Unit tests**: {{# passing}} / {{total}} ({{pass_rate}}%)
- **Integration tests**: {{# passing}} / {{total}}
- **Coverage**: {{coverage_percent}}% (threshold: 80%)
- **Lint**: ✅ / ❌
- **Type check**: ✅ / ❌

If any **< threshold**, attach explanation and mitigation plan.

---

## 💬 Current State & Next Steps

**What was accomplished in this milestone?**
```
{{summary}}
```

**What remains for the next milestone?**
```
{{next_milestone_summary}}
```

**Blocker / Risks:**
- [ ] None
- [ ] Yes (listed below)
```
{{blocker_details}}
```

---

## ✅ User Confirmation

**Do you confirm this milestone is complete and we should proceed?**

- ✅ **Yes, continue to next milestone / phase**
- ⏳ **Need minor fixes** (see comments)
- 🔄 **Hold — rework needed** (see blocker)

**Comments**:
```
{{user_comments}}
```

**Confirmation timestamp**: _____________  
**Confirmed by**: _____________

---

### 🛠️ Agent Next Actions

If confirmed:
1. Update WBS ledger: mark all tasks in this milestone `done`
2. Add evidence file references to ledger `evidence` column
3. Create pull request / initiate merge to main (if branching strategy dictates)
4. If this is the **final milestone of Phase 3**, proceed to Checkpoint Phase 4 (Quality)
