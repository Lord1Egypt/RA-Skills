# Report Structure Reference

## Report title format

`[{skill-name}] Regression Test Report — {YYYY-MM-DD}`

## Report structure

```markdown
# [{skill-name}] Regression Test Report

| Field | Value |
|-------|-------|
| Test time | YYYY-MM-DD HH:MM |
| Test runner | skill-regression (open-source) |
| Total cases | N |
| Case source | TEST.md | LLM-generated | default-placeholders |
| Script-layer pass rate | X/N (XX%) |
| AI-layer pass rate | X/N (XX%) |
| Combined pass rate | X/N (XX%) |
| Semantic score threshold | 7.0 |
| Scoring caveat | LLM-as-judge with same family ⚠️ |
| Report mode | Simple | Detailed |

---

## 📋 Conclusion

**Overall status**: 🟢 Healthy | 🟡 Needs attention | 🔴 At risk

Status decision rules:
- 🟢 Healthy: combined pass rate ≥ 90% AND no normal-flow failures
- 🟡 Needs attention: combined pass rate 70%-90%, or any failures present
- 🔴 At risk: combined pass rate < 70%, or normal-flow case failed

**Core functionality**: ✅ OK | ❌ Failed

**Summary**:
[2-3 sentences summarizing test results, calling out main issues]

---

## 🧪 Case Execution Details

| # | Name | Type | Script | AI | Score | Conclusion |
|---|------|------|--------|----|----|-----------|
| 1 | Basic upload | normal | ✅ | ✅ | 8.5 | Pass |
| 2 | File not found | error | ✅ | ❌ | 5.0 | Fail |

### Case 2 Failure Detail: File not found

**Type**: error
**Trigger**: `Upload this image /tmp/does_not_exist.jpg`

**Script Layer**: ✅ Pass
- Command: `bash scripts/upload.sh /tmp/does_not_exist.jpg`
- Actual output: `Error: file not found`
- Match rule: regex `error|not found|missing`

**AI Layer**: ❌ Failed (score 5.0, threshold 7.0)
- Actual response: `Upload failed, please check the path.`
- Expected: `Tells the user the file is missing and suggests a fix`
- Score reason: Response too brief, lacks actionable guidance

---

## 🐛 Known Issues / TODO

| # | Severity | Description | Related cases |
|---|----------|-------------|---------------|
| 1 | Medium | AI-layer error response too brief, lacks guidance | Case 2 |

---

## 💡 Improvement Suggestions

1. **SKILL.md**: clarify error handling in the trigger description
2. **TEST.md**: add edge cases for network timeout, permission denied, etc.
3. **Script messages**: consider localizing error output if appropriate

---

## 📎 Appendix

- Skill path: `<path-to-target-skill>`
- Case source: TEST.md | LLM-generated | default-placeholders
- Report generated at: {timestamp}
```
