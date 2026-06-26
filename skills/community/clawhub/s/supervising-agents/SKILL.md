---
name: supervising-agents
description: Use when YOU are dispatching tasks to subagents (Agent tool, openclaw, parallel workers). You become the supervisor by default. This skill guides how to monitor, intervene, and verify your subagents.
---

# Supervising Agents

## Core Principle

**The dispatcher IS the supervisor.** When you dispatch a task, you own the outcome.

```
YOU dispatch → YOU monitor → YOU verify → YOU report

If the subagent fails, YOU are responsible for catching it.
If you don't verify, YOU are responsible for the bad output.
```

---

## Part 1: The 5-Phase Workflow

```
PREPARE ──► DISPATCH ──► MONITOR ──► VERIFY ──► REPORT
    │           │           │           │          │
    ▼           ▼           ▼           ▼          ▼
 Define      Lock in     Active      Evidence    To human
 clearly    commitment   checking    required   accountable
```

---

## Part 2: PREPARE Phase

### Pre-Dispatch Checklist (MUST COMPLETE)

```
□ TASK DEFINED
  Goal (one sentence): _______________________________
  Requirements (list ALL): _______________________________
  Deliverables (specific files): _______________________________

□ TIME SET
  Budget: _____ minutes
  Check interval: _____ minutes (rule: budget/5, min 3 min)

□ VERIFICATION PLANNED
  How to check output exists: _______________________________
  How to verify correctness: _______________________________

□ RED FLAGS DEFINED
  What "going wrong" looks like: _______________________________
```

### Decision: Should You Dispatch?

| Condition | Decision |
|-----------|----------|
| Task is trivial (< 5 min) | Do it yourself |
| Task requires judgment you don't have | Ask human first |
| Task has clear requirements and deliverables | ✓ Dispatch with supervision |

---

## Part 3: DISPATCH Phase

### Dispatch Prompt Template

```
TASK: [One sentence - what success looks like]

REQUIREMENTS (complete ALL):
1. [requirement 1]
2. [requirement 2]
3. [requirement 3]

DELIVERABLES:
- [file 1] - [expected content]
- [file 2] - [expected content]

TIME: [X] minutes

─── BEFORE YOU START ───
Reply to confirm:
1. What is the goal? (your words)
2. What steps will you take?
3. How will you know you're done?

Do NOT start until you confirm.
```

### After Dispatch: Record Agent ID

```typescript
// Agent tool returns: agentId: 'abc123'
// SAVE THIS - you need it for SendMessage

const agentId = 'abc123';  // Keep track of this
```

---

## Part 4: MONITOR Phase (CRITICAL)

### The #1 Mistake: Passive Waiting

```
❌ WRONG: Dispatch → Wait → Check at end
✓ RIGHT: Dispatch → Active monitor → Intervene early
```

### Active Monitoring Techniques

#### Technique 1: Output File Watching

```bash
# Check if output files exist
ls -la [expected output directory]

# Check file sizes (should be > 0)
wc -l [expected files]

# Check modification times
find . -name "*.md" -mmin -5  # Files modified in last 5 min
```

**If no output after 1 check interval → INTERVENE NOW**

#### Technique 2: SendMessage Probe

```typescript
// Use SendMessage to check progress
SendMessage({
  to: agentId,
  message: `
    📊 PROGRESS CHECK
    
    Report NOW:
    1. What have you completed? (specific files/lines)
    2. What are you doing right now?
    3. Any blockers?
    
    Reply in under 30 seconds.
  `
});
```

#### Technique 3: Timestamp Tracking

```
Time 0:00 - Dispatch
Time 3:00 - First check (output files exist?)
Time 6:00 - Second check (progress visible?)
Time 9:00 - Third check (near completion?)
Time 12:00 - Final verification

If any check fails → intervene immediately
```

### Monitoring Decision Matrix

| Check Result | What It Means | Your Action |
|--------------|---------------|-------------|
| Output files exist, have content | On track | Continue monitoring |
| No output files after 2 intervals | Not started or stuck | SendMessage NOW |
| Output files empty | Fake work or error | SendMessage NOW |
| Subagent silent > 2x interval | May have abandoned | Escalate to human |

### Real-Time Red Flags

| Signal | Probability | Immediate Action |
|--------|-------------|------------------|
| No file changes in [interval] | 80% stuck | Check now |
| Subagent asks unrelated questions | 70% distracted | Redirect |
| Subagent says "almost done" but no files | 90% fake completion | Demand evidence |
| Time > 1.5x budget with no output | 95% failed | Intervene or take over |

---

## Part 5: INTERVENE Phase

### Intervention Protocol

```
┌─────────────────────────────────────────────────────────────┐
│                  INTERVENTION DECISION                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  CHECK FAILED?                                               │
│       │                                                      │
│       ├── No output at all ──────────────► Level 1: Probe   │
│       │                                  "What are you doing?"│
│       │                                                      │
│       ├── Wrong direction ───────────────► Level 2: Redirect │
│       │                                  "Stop X, do Y"      │
│       │                                                      │
│       ├── No response to probe ──────────► Level 3: Takeover│
│       │                                  "I'm handling it"   │
│       │                                                      │
│       └── Repeated failures ─────────────► Escalate to human│
│                                          "This agent can't..."│
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Level 1: Probe (Mild Concern)

```
📊 STATUS CHECK

I don't see any output files yet.

Report in 30 seconds:
1. What exactly have you done? (file names, not descriptions)
2. What are you doing right now? (specific action)
3. When will I see output?

Be specific. "Working on it" is not an answer.
```

### Level 2: Redirect (Clear Deviation)

```
⚠️ CORRECTION REQUIRED

Issue: [specific problem]

STOP: [wrong activity]
DO: [correct activity]

You have [X] minutes to show progress.

Do not explain. Execute.
```

### Level 3: Takeover (Critical Failure)

```
🔴 TAKING OVER

This task is not progressing.

I will complete it myself.

You: Stop everything. Provide list of what you actually completed (if anything).

This is recorded.
```

---

## Part 6: VERIFY Phase

### The Verification Gate

**NEVER accept "I'm done" without evidence.**

```
□ EVIDENCE CHECK
  - Show me the file: [read the actual file]
  - Show me the test output: [run the tests]
  - Show me it works: [demonstrate functionality]

□ REQUIREMENTS CHECK
  | Req | Done? | Evidence |
  |-----|-------|----------|
  | 1   | ✓/✗   | [proof]  |
  | 2   | ✓/✗   | [proof]  |
  | 3   | ✓/✗   | [proof]  |

□ QUALITY CHECK
  - Is output non-empty?
  - Does it actually work?
  - Are edge cases handled?
```

### Verification Commands

```bash
# File exists and has content?
ls -la [file] && wc -l [file]

# Code has actual implementation?
grep -E "(function|class|def |export )" [file]

# Tests pass?
npm test 2>&1 | tail -20

# Recent changes?
git status && git diff
```

### Common Verification Failures

| Claim | Reality | How to Catch |
|-------|---------|---------------|
| "Created the file" | File is empty | `wc -l file` |
| "Tests pass" | Tests don't exist | Run tests yourself |
| "Feature works" | Only happy path | Test edge cases |
| "All requirements done" | Some skipped | Check each one |

---

## Part 7: REPORT Phase

### Report Template

```markdown
📋 TASK REPORT

**Task:** [name]
**Status:** ✓ COMPLETE / ⚠ ISSUES / ✗ FAILED
**Time:** [actual] / [budget] minutes

**Verification:**
- Output exists: [yes/no + evidence]
- Tests pass: [yes/no + output]
- All requirements met: [yes/no + checklist]

**Evidence:**
- Files: [list with sizes]
- Key content: [paste relevant parts]

**Issues:** [if any]

**Next steps:** [if needed]
```

### When to Escalate to Human

```
🚨 ESCALATE when:
- Subagent completely failed after intervention
- Technical decision needed beyond your authority
- Output quality unacceptable despite verification
- Time significantly over budget with no end in sight
- Subagent behavior concerning (ignoring all instructions)
```

---

## Part 8: Common Failure Patterns

### Pattern 1: Confirmed but Never Started

**What happens:** Subagent confirms understanding, then does nothing.

**Detection:** No output files after 1 interval.

**Fix:**
```
"I see no output. What have you actually done?
Show me a file you created or edited in the last [X] minutes."
```

### Pattern 2: Silent Failure

**What happens:** Subagent encounters error, doesn't report, just stops.

**Detection:** No activity for 2+ intervals.

**Fix:**
```
"Report your status immediately.
If you hit an error, describe it exactly.
If you're stuck, say what you're stuck on."
```

### Pattern 3: Fake Completion

**What happens:** Subagent claims done, output is empty/wrong.

**Detection:** Output files don't match requirements.

**Fix:**
```
"Output verification failed:
- Requirement: [X]
- What I see: [Y]

This is not complete. Fix it or explain exactly why you cannot."
```

### Pattern 4: Scope Drift

**What happens:** Subagent works on something else, ignores original task.

**Detection:** Output unrelated to requirements.

**Fix:**
```
"Stop. You are working on [X] but task requires [Y].
Which part of the original task are you addressing?
If none, return to the original requirements immediately."
```

---

## Part 9: Quick Reference

### Time Estimates

| Task Type | Budget | Check Interval |
|-----------|--------|----------------|
| Quick (< 10 lines) | 5 min | Check at end only |
| Simple function | 10 min | Every 3 min |
| Feature implementation | 30 min | Every 5 min |
| Complex multi-file | 60+ min | Every 10 min + milestones |

### Red Flags Checklist

```
□ No output after 1 interval → SendMessage probe
□ "Almost done" with no files → Demand evidence NOW
□ Silent for 2 intervals → Assume failure, intervene
□ Unrelated questions → Redirect to task
□ Time > 1.5x budget → Escalate or take over
```

### The Iron Rules

```
1. NEVER wait passively - actively check
2. NEVER accept words as proof - verify files
3. NEVER let "basically done" slide - demand specifics
4. NEVER skip verification - your reputation is on the line
5. NEVER report to human without evidence - they trust you
```

---

## Implementation for openclaw

### Setup

```bash
# In openclaw, load this skill
/load supervising-agents

# Or set as default skill
export CLAW_SKILLS=supervising-agents
```

### Usage Pattern

```typescript
// 1. PREPARE
const task = {
  goal: "Create README.md with project overview",
  requirements: ["Project name", "Installation steps", "Usage example"],
  deliverables: ["README.md (min 50 lines)"],
  budget: 10, // minutes
  interval: 3 // minutes
};

// 2. DISPATCH with commitment lock
const result = await Agent({
  description: `Supervising: ${task.goal}`,
  prompt: buildPrompt(task)
});

// 3. MONITOR - check every interval
for (let i = 0; i < task.budget / task.interval; i++) {
  await sleep(task.interval * 60000);
  
  const output = checkOutput(task.deliverables);
  if (!output.exists) {
    await SendMessage(result.agentId, "Progress check: show me what you've created");
  }
}

// 4. VERIFY - don't trust, verify
const file = await Read("README.md");
if (file.lines < 50) {
  // Reject, demand more
}

// 5. REPORT to human
```

---

## Summary

**You dispatch → You own the outcome.**

The subagent is a tool, not a trusted partner. Your job is to:
1. Define clearly
2. Lock in commitment
3. **Actively monitor** (not passive wait)
4. Intervene early
5. Verify with evidence
6. Report with accountability

**Most common failure:** Passive waiting. Fix: Check output files early and often.

**Research foundation:** Persuasion techniques increase compliance 33% → 72% (Meincke et al., 2025, N=28,000).