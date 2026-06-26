# Checkpoint: Phase 2 — Planning Alignment

**Project**: {{project_name}}  
**Checkpoint**: Phase 2 — Planning  
**Timestamp**: {{timestamp}}  
**Agent**: {{agent_id}}

---

## 📋 Deliverables Reviewed

- [ ] `docs/architecture.md` exists (or equivalent design doc)
- [ ] WBS task ledger created at `docs/spm/ledger.md`
- [ ] All tasks have:
  - [ ] Clear description
  - [ ] Exit criteria (how we know it's done)
  - [ ] Dependencies mapped (task IDs)
  - [ ] Evidence placeholders defined
- [ ] Task count reasonable: 1-2 days of work per task (no 10-task monolithic items)
- [ ] Critical path identified (highest risk / longest duration tasks marked)
- [ ] External dependencies timeline documented (when we need API access, credentials, etc.)

---

## 🔍 WBS Ledger Review (sample check)

| ID | Work Package | Dependencies | Exit Criteria | Evidence | Status |
|----|-------------|-----------|---------------|----------|--------|
| 1 | {{example_task}} | - | {{example_criteria}} | {{file/snippet}} | todo |
Pick 3 random tasks from the ledger and verify:

**Task {{random_id_1}}**: {{description}}
- Exit criteria specific? ✅ / ❌
- Evidence traceable? ✅ / ❌
- Estimate reasonable? ✅ / ❌

**Task {{random_id_2}}**: {{description}}
- Exit criteria specific? ✅ / ❌
- Evidence traceable? ✅ / ❌
- Estimate reasonable? ✅ / ❌

**Task {{random_id_3}}**: {{description}}
- Exit criteria specific? ✅ / ❌
- Evidence traceable? ✅ / ❌
- Estimate reasonable? ✅ / ❌

---

## 💬 Assumptions Re-check

Revisit assumptions from Phase 1. Have any changed?

| Assumption | Still valid? | Comments |
|------------|--------------|----------|
| {{ assumption_1 }} | ✅ / ❌ | {{}} |
| {{ assumption_2 }} | ✅ / ❌ | {{}} |
| {{ assumption_3 }} | ✅ / ❌ | {{}} |

If any **No**, update `DECISIONS.md` before proceeding.

---

## ✅ User Confirmation

**Is the plan realistic and aligned with your expectations?**

- ✅ **Yes, proceed to Phase 3 (Execution)**
- ⏳ **Need revisions** (see comments below)
- ❌ **Re-plan** (too ambitious / missing something)

**Comments / Concerns**:
```
{{user_comments}}
```

**Confirmation timestamp**: _____________  
**Confirmed by**: _____________

---

### 🛠️ Next Actions (for Agent)

Once confirmed:
1. Create `docs/spm/ledger.md` as the active WBS tracker (if not exists)
2. Set `project_state.json` phase status to `in_progress` for execution
3. Begin first task in execution phase (usually "Setup Git worktree" or "Initialize project structure")
