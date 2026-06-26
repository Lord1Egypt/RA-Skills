# Code Completion Self-Review Checklist

**Feature**: {{feature_name}}  
**Branch**: {{branch_name}}  
**Agent**: {{agent_id}}  
**Timestamp**: {{timestamp}}  

---

## 🤖 Automated Checks (run `./scripts/verify_checklists.py code`)

- [ ] `npm run type-check` passes (no TypeScript errors)
- [ ] `npm run lint` passes (no ESLint warnings/errors)
- [ ] `npm test` passes (all unit tests green)
- [ ] No secrets in code (`grep -r "API_KEY\|SECRET\|PASSWORD\|TOKEN" src/` returns empty)
- [ ] All new functions have JSDoc comments (if project standard requires)
- [ ] Code coverage ≥ 80% for changed files (`npm run test:coverage` shows at least 80%)
- [ ] No `console.log` statements in production code (only `logger.*`)
- [ ] All files saved with correct line endings (LF, not CRLF)

**Automated results** (paste output or leave blank if running via script):
```
{{automated_output}}
```

---

## 👁️ Manual Review (answer all)

### Correctness & Robustness
- [ ] Edge cases handled (null inputs, network failures, invalid data)
- [ ] Error messages are user-friendly (no stack traces exposed to end users)
- [ ] All `try-catch` blocks log errors with context (symbol, userId, requestId, etc.)
- [ ] No hard-coded values (all configs from `config/` or env vars)

### Performance & Security
- [ ] Database queries use prepared statements (no SQL injection risk)
- [ ] API response time < 200ms (p95) for happy path (benchmark added to tests?)
- [ ] No infinite loops or unbounded recursion
- [ ] Authentication/authorization checked on protected endpoints

### Code Quality
- [ ] Functions ≤ 30 lines (split longer ones)
- [ ] No duplicated code (DRY)
- [ ] Meaningful variable/function names (no `data`, `temp`, `x`)
- [ ] Comments explain "why", not "what" (business logic documented)

### Consistency
- [ ] Follows existing code style (same naming, same pattern for similar tasks)
- [ ] Uses project standard libraries (no duplicate dependencies)
- [ ] All new imports actually used (no dead imports)

---

## 📦 Dependencies (if applicable)

- [ ] New dependencies added to `package.json` are necessary and minimal
- [ ] New dependencies scanned for security (no known vulnerabilities via `npm audit`)
- [ ] License compatibility reviewed (if project has license constraints)

---

## 🧪 Testing

- [ ] Unit tests cover all new functions and branches
- [ ] Integration tests cover API endpoints (if applicable)
- [ ] Edge case tests added for error paths
- [ ] Test data uses fixtures / factories (not hard-coded magic values)

---

## 📚 Documentation

- [ ] README updated (if feature changes user-facing behavior)
- [ ] API docs (`docs/API.md` or `openapi.yaml`) updated
- [ ] Inline JSDoc added for public functions/types
- [ ] CHANGELOG entry added (if public release)

---

## ✍️ Evidence

Attach or reference evidence for key items:

- **TypeScript check**: `{{typecheck_log_path}}`
- **Test coverage**: `{{coverage_report_path}}` ({{coverage_percent}}%)
- **Lint summary**: `{{lint_log_path}}`
- **Test results**: `{{test_log_path}}`
- **Code diff**: `{{git_commit_hash}}`

---

## 🎯 Sign-off

**Status**: ✅ PASS / ⚠️ PASS WITH NOTES / ❌ FAIL

**If FAIL or PASS WITH NOTES, list failures and planned fixes**:
```
{{failures_and_fixes}}
```

**Next action**:
- [ ] Fix issues and re-run checklist
- [ ] Proceed (accept minor risks as documented)
- [ ] Escalate to code review (major concerns)

**Signed off by**: _____________ (agent or human)  
**Timestamp**: _____________
