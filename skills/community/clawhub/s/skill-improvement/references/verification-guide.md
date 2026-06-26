# Verification Guide

Guide for testing skill optimization effectiveness using subagents.

---

## Overview

**Purpose:** Verify that skill optimizations actually improve functionality without introducing regressions.

**Method:** Use subagents to simulate real-world skill usage scenarios.

**Coverage:** 4 test types covering discovery, understanding, execution, and regression.

---

## Test Types

### 1. Trigger Test

**Objective:** Verify skill is discovered and loaded when relevant.

**What it tests:**
- Description quality
- Keyword coverage
- Trigger conditions

**How to run:**

```typescript
// Subagent prompt
"You are testing skill discovery. The user has a skill named [skill-name] 
with description: '[description]'. 

Simulate this scenario: [scenario description]

Task: [task that should trigger the skill]

Do NOT explicitly mention the skill name. Just present the task naturally.

Report:
1. Was the skill discovered?
2. Was it loaded?
3. How confident are you in the trigger match?"
```

**Pass criteria:**
- ✅ Skill discovered from description
- ✅ Skill loaded into context
- ✅ High confidence in relevance

**Fail indicators:**
- ❌ Skill not found
- ❌ Wrong skill loaded
- ❌ Low confidence in match

---

### 2. Understanding Test

**Objective:** Verify subagent correctly interprets skill workflow.

**What it tests:**
- Workflow clarity
- Instruction quality
- Step comprehension

**How to run:**

```typescript
// Subagent prompt
"You have loaded the [skill-name] skill. Read SKILL.md and any referenced files.

Answer these questions:
1. What is the main workflow?
2. What are the key steps?
3. What should you do first?
4. What should you do last?
5. What tools/scripts are available?

Be specific. Quote relevant sections if needed."
```

**Pass criteria:**
- ✅ Workflow correctly identified
- ✅ Steps in correct order
- ✅ Tools/scripts understood
- ✅ No confusion or ambiguity

**Fail indicators:**
- ❌ Wrong workflow described
- ❌ Steps out of order
- ❌ Tools misunderstood
- ❌ Confusion in answers

---

### 3. Execution Test

**Objective:** Verify skill can be applied to a real task.

**What it tests:**
- Workflow execution
- Tool/script functionality
- Output quality

**How to run:**

```typescript
// Subagent prompt
"Execute the [skill-name] skill on this task:

Task: [specific task matching skill purpose]

Input: [provided input]

Follow the skill's workflow. Use any scripts or tools as instructed.

Report:
1. What steps did you take?
2. What tools/scripts did you use?
3. What output did you produce?
4. Did you encounter any issues?"
```

**Pass criteria:**
- ✅ Workflow followed correctly
- ✅ Tools/scripts executed successfully
- ✅ Expected output produced
- ✅ No errors or issues

**Fail indicators:**
- ❌ Steps skipped or done wrong
- ❌ Script errors
- ❌ Unexpected output
- ❌ Blocking issues encountered

---

### 4. Regression Test

**Objective:** Verify optimizations didn't break existing functionality.

**What it tests:**
- Backward compatibility
- Existing use cases
- Known working scenarios

**How to run:**

```typescript
// Subagent prompt
"You have a skill that was recently optimized. Test these scenarios that 
worked before the optimization:

Scenario 1: [original working scenario 1]
Input: [input]
Expected: [expected output]

Scenario 2: [original working scenario 2]
Input: [input]
Expected: [expected output]

Execute each scenario. Report:
1. Did it work as before?
2. Any differences from expected?
3. Any new errors?"
```

**Pass criteria:**
- ✅ All scenarios work as before
- ✅ No new errors introduced
- ✅ Output matches expected

**Fail indicators:**
- ❌ Scenario no longer works
- ❌ Different output produced
- ❌ New errors appear

---

## Verification Workflow

### Step 1: Prepare Test Scenarios

Define 4 test scenarios:

1. **Trigger scenario:**
   - Task that should discover skill
   - Natural language request
   - No explicit skill mention

2. **Understanding scenario:**
   - Questions about workflow
   - Tool/script comprehension
   - Step order verification

3. **Execution scenario:**
   - Real task using skill
   - Input data provided
   - Expected output known

4. **Regression scenarios:**
   - 2-3 known working cases
   - Before optimization behavior
   - Expected outputs documented

### Step 2: Dispatch Subagents

Run tests in parallel:

```typescript
// Parallel subagent dispatch
const triggerTest = task(subagent_type="explore", prompt="[trigger test]", run_in_background=true)
const understandingTest = task(subagent_type="explore", prompt="[understanding test]", run_in_background=true)
const executionTest = task(subagent_type="explore", prompt="[execution test]", run_in_background=true)
const regressionTest = task(subagent_type="explore", prompt="[regression test]", run_in_background=true)

// Collect results
const results = await Promise.all([
  background_output(triggerTest),
  background_output(understandingTest),
  background_output(executionTest),
  background_output(regressionTest)
])
```

### Step 3: Analyze Results

For each test result:

1. Check pass/fail status
2. Identify specific issues
3. Document findings
4. Assess severity

### Step 4: Generate Report

Create verification report:

```markdown
# Verification Report

[Use report-templates.md format]
```

### Step 5: Handle Failures

If verification fails:

1. **Document the failure:**
   - What test failed
   - What went wrong
   - Expected vs actual

2. **Identify root cause:**
   - What change caused it
   - Why it happened
   - How to fix

3. **Fix and re-test:**
   - Apply fix
   - Re-run failed tests
   - Verify fix works

4. **Iterate until pass:**
   - Continue cycle
   - Document attempts
   - Final verification

---

## Test Scenario Examples

### Example 1: PDF Skill Trigger Test

**Scenario:** User asks to extract text from a PDF

**Subagent prompt:**
```
"Simulate this conversation:

User: 'I have a PDF file called report.pdf and I need to extract all the text from it into a plain text file.'

Task: Help the user extract text from the PDF.

Report:
1. Did you identify the relevant skill?
2. What skill did you consider?
3. Would you load the pdf-processing skill for this?
4. Why or why not?"
```

**Expected result:**
- Skill identified: pdf-processing
- Would load: Yes
- Reason: Task matches trigger conditions (PDF, text extraction)

---

### Example 2: Data Validation Understanding Test

**Scenario:** Understanding a validation workflow

**Subagent prompt:**
```
"You have loaded the data-validation skill. Read the skill and answer:

1. What is the validation workflow?
2. What validation rules are available?
3. How do you validate email addresses?
4. What output format does the skill produce?

Be specific. Show you understand the workflow."
```

**Expected result:**
- Workflow: Load data → Validate → Report errors → Fix → Re-validate
- Rules: Email, phone, date, required fields
- Email validation: Regex pattern or library
- Output: JSON validation report

---

### Example 3: Skill Execution Test

**Scenario:** Execute a code review skill

**Subagent prompt:**
```
"Execute the code-review skill on this code:

Code:
```python
def calc(a, b):
    return a + b
```

Follow the skill's workflow. Perform a code review.

Report:
1. What review steps did you follow?
2. What issues did you find?
3. What suggestions did you make?
4. What was the final output?"
```

**Expected result:**
- Steps: Analyze structure → Check bugs → Review style → Suggest improvements
- Issues: Function name unclear, missing docstring, no type hints
- Suggestions: Rename to `add_numbers`, add docstring, add type hints
- Output: Structured review report

---

### Example 4: Regression Test

**Scenario:** Verify optimization didn't break existing function

**Subagent prompt:**
```
"Test this scenario that worked before the skill optimization:

Before optimization:
- Skill: pdf-processing
- Task: Rotate PDF 90 degrees
- Command: `python scripts/rotate.py input.pdf --degrees 90`
- Result: PDF rotated successfully

Execute the same task now. Does it still work?

Report:
1. Did the script run?
2. Was the output correct?
3. Any differences from before?
4. Any errors?"
```

**Expected result:**
- Script ran: Yes
- Output correct: Yes
- Differences: None
- Errors: None

---

## Verification Checklist

Before declaring optimization complete:

- [ ] All 4 test types executed
- [ ] Trigger test passed
- [ ] Understanding test passed
- [ ] Execution test passed
- [ ] Regression test passed
- [ ] No critical issues found
- [ ] Report generated
- [ ] Documentation updated

---

## Common Issues and Fixes

### Issue: Trigger Test Fails

**Cause:** Description doesn't match task

**Fix:**
1. Review description keywords
2. Add missing trigger terms
3. Clarify "Use when" conditions

---

### Issue: Understanding Test Fails

**Cause:** Workflow unclear or incomplete

**Fix:**
1. Add numbered steps
2. Clarify decision points
3. Link to detailed references

---

### Issue: Execution Test Fails

**Cause:** Scripts broken or instructions wrong

**Fix:**
1. Test scripts manually
2. Fix code errors
3. Update instructions

---

### Issue: Regression Test Fails

**Cause:** Optimization broke existing function

**Fix:**
1. Identify breaking change
2. Revert or fix the change
3. Re-run tests
4. Find alternative optimization

---

## Verification Best Practices

1. **Test early and often:** Don't wait until end of optimization
2. **Test realistic scenarios:** Use actual use cases, not just simple examples
3. **Document everything:** Keep records of all tests and results
4. **Iterate quickly:** Fix issues as soon as they're found
5. **Be thorough:** All 4 test types matter

---

## Integration with Optimization Workflow

Verification fits into the optimization workflow at Phase 5:

```
Phase 1: Diagnose
Phase 2: Report
Phase 3: Select
Phase 4: Execute
Phase 5: Verify ← YOU ARE HERE
```

**If verification passes:**
- Mark optimization complete
- Update skill documentation
- Optionally re-run diagnostic for final grade

**If verification fails:**
- Document failure
- Return to Phase 3 or 4
- Apply fixes
- Re-run verification
- Iterate until pass