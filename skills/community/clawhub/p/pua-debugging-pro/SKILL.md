---
name: pua-debugging-pro
description: Professional anti-giveup debugging protocol for coding tasks where the agent starts looping, deflecting to users, or trying to end early without evidence. Use when there are repeated failures, weak root-cause analysis, missing verification, vague environment blame, or low-agency behavior. Enforces evidence-first debugging, bounded escalation, structured stop conditions, and dignified communication without humiliation language.
---

# PUA Debugging Pro (Dignified Edition)

Use this protocol to increase execution quality under failure, while preserving professional tone.

## Non-negotiables

1. **No premature surrender**
   - Do not conclude "cannot solve" before completing escalation checklist.

2. **Evidence before questions**
   - Use available tools first.
   - If user input is still required, ask with concrete evidence and narrowed uncertainty.

3. **Verification before completion**
   - No "done" claims without explicit validation output.

4. **Dignified communication**
   - Never use humiliation or threatening rhetoric.
   - Use calm, direct, engineering language.

## Trigger signals

Activate when one or more are present:
- 2+ failed attempts on same objective
- Repeated micro-tweaks with no new information
- Deflection to user without prior tool-based diagnosis
- Unverified environment blame (permissions/network/version) 
- Completion claim without tests/checks
- Stopping at surface fix with no impact scan

## Escalation ladder (bounded)

### L1 (after 2 failed attempts)
- Switch to a **substantially different hypothesis**.
- Record: what failed, what changed, what signal to watch.

### L2 (after 3 failed attempts)
- Mandatory triage pack:
  - full error text
  - relevant context window (code/log around failure)
  - one external lookup or doc check
  - one assumption inversion test

### L3 (after 4+ failed attempts)
- Run full 7-point checklist (below).
- Produce structured decision: continue / pivot / stop.

## 7-point checklist

- [ ] Captured exact error/output
- [ ] Read relevant source/config context
- [ ] Verified runtime prerequisites (version/path/permission/dependency)
- [ ] Tried a materially different approach
- [ ] Defined clear pass/fail criteria for latest attempt
- [ ] Ran validation (test/command/request) and recorded result
- [ ] Scanned adjacent risk (same pattern in nearby code/config)

## Output contract

When progressing:
- **Current hypothesis**
- **Actions executed**
- **Observed evidence**
- **Next step**

When blocked after L3:
- **Facts established**
- **Options eliminated**
- **Smallest unresolved uncertainty**
- **Recommended next action with cost/risk**

For reusable output format, read:
- `references/checklist-template.md`

For one-page handoff/retrospective artifact, use:
- `assets/postmortem-onepager.md`

## Stop conditions (required)

If all conditions are true, stop trying and escalate to user:
1. 7-point checklist completed
2. Last attempt produced no new diagnostic signal
3. Further attempts require missing external secret/access/business decision

Use this closing format:
- "I completed bounded escalation and cannot safely proceed without X."
- "Evidence gathered: ..."
- "Recommended next action: ..."

## Style rules

- Prefer concise, factual updates over motivational talk.
- Be direct; avoid apology loops.
- Keep tone firm, respectful, and professional.
