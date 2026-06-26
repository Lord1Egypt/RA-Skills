# Report Templates

Templates for diagnostic reports and selection interfaces.

---

## Diagnostic Report Template

```markdown
# Skill Diagnostic Report: [skill-name]

**Path:** [file path]
**Overall Grade:** [A/B/C/D/F]
**Issues Found:** X total (Y high, Z medium, W low)

---

## Summary

[One paragraph overview of main findings]

---

## High Priority Issues (Y)

### Issue 1: [Problem Title]

**Category:** Metadata / Architecture / Text / Code
**Check ID:** [M1/A1/T1/C1 etc.]
**Severity:** HIGH
**Location:** [specific file and section]

**Current State:**
```
[Show current content or code]
```

**Expected State:**
```
[Show what it should be]
```

**Impact:** [Why this matters]

**Fix:**
```
[Specific action to take]
```

**Reference:** [Link to quality standard]

---

[Repeat for each HIGH issue]

---

## Medium Priority Issues (Z)

[Same format as HIGH issues]

---

## Low Priority Issues (W)

[Same format as HIGH issues]

---

## Optimization Suggestions

[Holistic recommendations for skill improvement]

---

## Next Steps

1. Review issues and select items to fix
2. Execute optimization workflow
3. Verify fixes with subagent testing
4. Re-run diagnostic if needed
```

---

## Selection Interface Template

```markdown
## Select Issues to Fix

Found X issues. Select which to address:

### High Priority (Y issues) ⚠️

**Must fix - affects skill discovery/execution:**

- [ ] **1.** [Problem description]
  - Impact: [Brief impact statement]
  
- [ ] **2.** [Problem description]
  - Impact: [Brief impact statement]

---

### Medium Priority (Z issues) ⚙️

**Should fix - improves quality/usability:**

- [ ] **3.** [Problem description]
  - Impact: [Brief impact statement]

- [ ] **4.** [Problem description]
  - Impact: [Brief impact statement]

---

### Low Priority (W issues) 💡

**Nice to fix - minor improvements:**

- [ ] **5.** [Problem description]
  - Impact: [Brief impact statement]

---

### Quick Actions

Choose one:

1. **`Fix all high priority`** - Automatically select and fix all HIGH issues
2. **`Fix selected`** - Process only checked items
3. **`Fix all`** - Fix every issue found
4. **`View details [N]`** - See detailed analysis for issue N
5. **`Ignore [N]`** - Remove issue N from consideration
6. **`Export report`** - Save full report to file

---

### Your Selection

Reply with:
- Numbers of issues to fix (e.g., "1, 3, 5")
- Or a quick action command
- Or type "skip" to abort
```

---

## Change Log Template

```markdown
# Optimization Change Log

**Skill:** [skill-name]
**Date:** [timestamp]
**Issues Fixed:** X

---

## Changes Made

### Change 1: [Description]

**Issue ID:** [M1/A1/T1/C1]
**File:** [file path]
**Type:** [Edit / Add / Delete]

**Before:**
```
[Original content]
```

**After:**
```
[New content]
```

**Reason:** [Why this change was made]

---

[Repeat for each change]

---

## Summary

- X files modified
- Y lines changed
- Z issues resolved
- Grade improved: [Before] → [After]

## Backup

Original skill backed up to: `[skill-name].backup-[timestamp]`
```

---

## Verification Report Template

```markdown
# Verification Report

**Skill:** [skill-name]
**Optimization Date:** [timestamp]
**Test Scenarios:** 4

---

## Test Results

| Test | Status | Time | Notes |
|------|--------|------|-------|
| Trigger | ✅ PASS | 2s | Skill correctly discovered |
| Understanding | ✅ PASS | 5s | Workflow interpreted correctly |
| Execution | ⚠️ PARTIAL | 8s | See issues below |
| Regression | ✅ PASS | 3s | Original functions work |

**Overall:** PASS with warnings

---

## Detailed Results

### 1. Trigger Test

**Scenario:** [Test description]
**Input:** [Test input]
**Expected:** [Expected behavior]
**Actual:** [Actual behavior]
**Status:** ✅ PASS

---

### 2. Understanding Test

**Scenario:** [Test description]
**Input:** [Test input]
**Expected:** [Expected behavior]
**Actual:** [Actual behavior]
**Status:** ✅ PASS

---

### 3. Execution Test

**Scenario:** [Test description]
**Input:** [Test input]
**Expected:** [Expected behavior]
**Actual:** [Actual behavior]
**Status:** ⚠️ PARTIAL

**Issue Found:**
- Problem: [Specific issue]
- Location: [Where in skill]
- Fix: [Recommended action]

---

### 4. Regression Test

**Scenario:** [Test description]
**Input:** [Test input]
**Expected:** [Same as before optimization]
**Actual:** [Actual behavior]
**Status:** ✅ PASS

---

## Issues Summary

### Critical Issues (0)
None

### Warnings (1)

1. **Execution partial:**
   - **Issue:** [Description]
   - **Impact:** MEDIUM
   - **Fix:** [Recommendation]
   - **Priority:** Should fix before deployment

---

## Recommendations

1. [Recommendation 1]
2. [Recommendation 2]
3. [Recommendation 3]

---

## Conclusion

**Optimization successful:** ✅ Yes / ⚠️ Partially / ❌ No

**Grade improvement:** [Before] → [After]

**Ready for deployment:** ✅ Yes / ⚠️ With fixes / ❌ No

**Next steps:**
- [Action 1]
- [Action 2]
```

---

## Example Reports

### Example 1: High Quality Skill

```markdown
# Skill Diagnostic Report: pdf-processing

**Path:** /skills/pdf-processing/SKILL.md
**Overall Grade:** A
**Issues Found:** 3 total (0 high, 2 medium, 1 low)

## Summary

Well-structured skill with minor optimization opportunities. 
Core functionality is solid; improvements would enhance maintainability.

## Medium Priority Issues (2)

### Issue 1: Missing Keywords in Description

**Category:** Metadata
**Check ID:** M5
**Severity:** MEDIUM

**Current:**
```yaml
description: Use when working with PDF files
```

**Expected:**
```yaml
description: Use when extracting text from PDFs, filling PDF forms, or merging PDF documents. Triggers on PDF-related tasks.
```

**Fix:** Add specific trigger keywords for better discovery.

---

### Issue 2: Undocumented Constant

**Category:** Code
**Check ID:** C2
**Severity:** MEDIUM

**Location:** scripts/extract.py, line 42

**Current:**
```python
MAX_PAGES = 100
```

**Expected:**
```python
# Limit to 100 pages to prevent memory issues on large documents
# Increase if processing larger PDFs is needed
MAX_PAGES = 100
```

**Fix:** Add justification comment.

---

## Low Priority Issues (1)

### Issue 3: Minor Terminology Inconsistency

**Category:** Text
**Check ID:** T3

**Location:** SKILL.md lines 23 and 45

**Current:** Uses both "PDF file" and "PDF document"

**Fix:** Standardize to "PDF file" throughout.

---

## Recommendations

1. Update description with trigger keywords
2. Add comments to constants in scripts
3. Standardize terminology in next revision
```

---

### Example 2: Needs Improvement

```markdown
# Skill Diagnostic Report: data-helper

**Path:** /skills/data-helper/SKILL.md
**Overall Grade:** D
**Issues Found:** 8 total (3 high, 3 medium, 2 low)

## Summary

Multiple critical issues prevent effective skill use. 
Metadata problems block discovery; code issues risk errors.

## High Priority Issues (3)

### Issue 1: Invalid Name Format

**Category:** Metadata
**Check ID:** M1
**Severity:** HIGH

**Current:**
```yaml
name: Data_Helper (v2)
```

**Expected:**
```yaml
name: processing-data
```

**Impact:** Skill may not be discovered by Claude.

**Fix:** Rename to lowercase-hyphen format.

---

### Issue 2: Missing "Use when" in Description

**Category:** Metadata
**Check ID:** M3
**Severity:** HIGH

**Current:**
```yaml
description: Processes and validates data
```

**Expected:**
```yaml
description: Use when processing data files, validating data formats, or transforming data structures
```

**Impact:** Claude cannot determine when to load this skill.

**Fix:** Rewrite description with "Use when" format.

---

### Issue 3: No Error Handling in Script

**Category:** Code
**Check ID:** C1
**Severity:** HIGH

**Location:** scripts/process.py, line 18

**Current:**
```python
data = open(file_path).read()
```

**Expected:**
```python
try:
    with open(file_path) as f:
        data = f.read()
except FileNotFoundError:
    print(f"File not found: {file_path}")
    data = ""
```

**Impact:** Script crashes on missing file.

**Fix:** Add try/except error handling.

---

## Immediate Actions Required

1. Fix name format
2. Rewrite description with trigger conditions
3. Add error handling to scripts
```

---

## Template Usage

1. Copy appropriate template
2. Fill in [placeholders]
3. Customize as needed for specific skill
4. Ensure all required sections are complete
5. Review for clarity and actionability