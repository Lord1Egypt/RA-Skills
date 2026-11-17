# Test Design Guide

> How to design tests that actually find problems.

## Test Design Principles

1. **Test the boundaries** — Edge cases reveal the most bugs
2. **Test the unexpected** — Users do things you don't anticipate
3. **Test the integration** — Skills must work together
4. **Test the user** — Both novices and experts
5. **Test the negative** — What should NOT happen is as important as what should

## Test Case Template

```
TEST ID: [Unique identifier]
NAME: [Descriptive name]
PURPOSE: [What this test validates]
PRECONDITIONS: [What must be true before test]

INPUT:
→ [Specific input]

EXPECTED OUTPUT:
→ [What should happen]

ACTUAL OUTPUT:
→ [What actually happened]

PASS/FAIL: [Status]
SEVERITY: [Critical/Major/Minor]
NOTES: [Additional observations]
```

## Edge Case Categories

1. **Empty/Null Input** — What happens with nothing?
2. **Extreme Values** — Maximum, minimum, overflow
3. **Invalid Format** — Wrong type, wrong structure
4. **Unexpected Content** — Nonsense, malicious, irrelevant
5. **Concurrent Use** — Multiple simultaneous requests
6. **Long-Running** — Extended use, memory buildup
7. **Interrupted** — Stopped mid-execution

## Regression Test Checklist

```
□ All previous functionality still works
□ New functionality works correctly
□ No performance degradation
□ No new bugs introduced
□ Documentation is accurate
□ Examples still work
□ Integration points intact
```
