---
name: workflow-template
---

# Workflow: <workflow-id>

## Meta
- ID:           <workflow-id>
- Task type:    <what kind of task this covers>
- State:        pending
- Created:      YYYY-MM-DD
- Owner:        [workspace owner]
- Scope:        [broad description of when this workflow applies]

## Preconditions
<!-- Must all be true before workflow can start. Any fail = gate. -->
- [ ] <precondition-1>
- [ ] <precondition-2>

## Steps

### Step 1 — <name>
- Description: [what happens in this step]
- Expected output: [what should exist after this step]
- Checkpoint: yes | no
- Can skip: yes (reason: <why>) | no

### Step 2 — <name>
- Description:
- Expected output:
- Checkpoint: yes | no
- Can skip: no

<!-- Add as many steps as needed -->

## Gates
<!-- Hard stops. Workflow cannot proceed past this point until condition met. -->

| Gate ID | Position | Condition | On fail |
|---|---|---|---|
| G-001 | Before step 2 | <condition> | Stop, surface to owner |

## Checkpoints
<!-- See checkpoints/<workflow-id>.md for detailed verification logic -->

| CP ID | After step | Verification | Failure type |
|---|---|---|---|
| CP-001 | 1 | <what to check> | hard | soft |

## Scoped Rules
<!-- Rules specific to this workflow only. See rules/do/ and rules/dont/ -->

### Must Do (scoped)
- <rule>

### Must Not Do (scoped)
- <rule>

## Post-Fix Policy
<!-- What happens if a violation is found after completion -->
- Hard violation found post-completion: [corrective action]
- Soft violation found post-completion: [log only | review | correct]

## Notes
[Any context, edge cases, owner preferences for this workflow]
