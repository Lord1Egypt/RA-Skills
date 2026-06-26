# Output-Driven Development Skill

## Trigger
Define success criteria and verification BEFORE coding. Agents prove their work.

**Trigger phrases:** "define success criteria", "output-driven", "verify before done", "prove it works", "acceptance criteria"

## Process

1. **Define output**: What exactly should the result look like?
2. **Write verification**: How will we prove it works?
3. **Build**: Implement the solution
4. **Verify**: Run verification, show evidence
5. **Ship**: Only after verification passes

## Template

```markdown
# Task: [Description]

## Success Criteria
- [ ] [Specific, measurable criterion 1]
- [ ] [Specific, measurable criterion 2]
- [ ] [Specific, measurable criterion 3]

## Verification Plan
For each criterion, how to verify:
1. [Run command X, expect output Y]
2. [Open URL, see element Z]
3. [Check file, contains content W]

## Build Log
[What was implemented and how]

## Verification Results
- Criterion 1: ✅ PASS — [evidence]
- Criterion 2: ✅ PASS — [evidence]
- Criterion 3: ❌ FAIL — [what went wrong, fix plan]
```

## Rules

- Never claim "done" without showing verification evidence
- "Should work" is not verification — run it and show the output
- If you can't define success criteria, you don't understand the task
- Verification should be reproducible by anyone
- Failed verification → fix → re-verify (don't skip)
- Screenshots, logs, test output > "I checked and it works"
