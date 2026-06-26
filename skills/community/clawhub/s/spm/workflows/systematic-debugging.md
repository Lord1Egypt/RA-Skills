# Systematic Debugging

## Overview

**Iron Law:** NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST

Symptom fixes are failure. Complete all 4 phases before attempting any fix.

## Phase 1: Root Cause Investigation

1. Read error messages completely (stack trace, line numbers)
2. Reproduce consistently (exact steps)
3. Check recent changes (git diff, recent commits)
4. Gather evidence (diagnostic commands, logs at each component boundary)
5. Trace data flow backward from failure point

## Phase 2: Pattern Analysis

1. Find working examples in same codebase
2. Compare reference implementations completely
3. Identify ALL differences between working and broken
4. Understand dependencies

## Phase 3: Hypothesis and Testing

1. Form single hypothesis: "I think X is root cause because Y"
2. Test with MINIMAL change (one variable at a time)
3. Verify result
4. Didn't work? New hypothesis. Don't stack fixes.

## Phase 4: Fix and Verify

1. Create failing test case that reproduces the bug
2. Implement single fix (address root cause, not symptom)
3. Verify: original test passes, no regressions
4. If fix doesn't work after 3 attempts: STOP — this is an architectural problem

## 3+ Fixes Failed: Question Architecture

If you've tried 3+ fixes and none worked:
- Each fix reveals new shared state/coupling?
- Fixes require massive refactoring?
- New symptoms appear elsewhere?

STOP and discuss with the user. This is a wrong architecture, not a bug.
