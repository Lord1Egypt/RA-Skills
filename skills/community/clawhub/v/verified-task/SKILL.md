---

name: verified-task
description: Enforce correctness before execution. Verify any task output and only proceed if it passes—override requires explicit operator approval.
-----------------------------------------------------------------------------------------------------------------------------------------------------

# Verified Task

Enforce correctness before execution.

Verify any agent output and only proceed if it passes. Override requires explicit operator approval.

---

## When to Use This

**Before sending money**

* Verify an invoice, payout, or transaction matches the agreement
* Prevent incorrect or fraudulent payments

**Before posting content**

* Ensure a post, email, or message matches instructions
* Avoid publishing incorrect, off-brand, or incomplete content

**Before executing actions**

* Confirm an automation result is correct before it runs
* Stop workflows from drifting when nobody is watching

**Before making decisions**

* Validate summaries, classifications, or recommendations
* Ensure conclusions match the task requirements

> If the output matters, verify it before proceeding.

---

## Core Principle

Verification is a **guardrail**, not a suggestion.

* Default behavior = **block unless PASS**
* Agents **must not override** a failed or indeterminate result
* Only a **human operator** may explicitly override

---

## Core Execution Loop

1. **Define the task specification**

   * what should be produced
   * required constraints
   * acceptance criteria

2. **Generate output**

3. **Verify output against the specification**

   * compare expected vs actual
   * check completeness and correctness
   * identify missing requirements or mismatches

4. **Return a verdict**

   * **PASS** → safe to proceed
   * **FAIL** → reject, retry, or revise
   * **INDETERMINATE** → stop and review

5. **Enforce the decision**

   * proceed only if PASS
   * otherwise halt
   * human operator may explicitly override

---

## Output Format

```json
{
  "task_id": "...",
  "verdict": "PASS | FAIL | INDETERMINATE",
  "reason": "...",
  "confidence": "high | medium | low"
}
```

---

## Example Usage

### Input

```json
{
  "task_id": "email-approval-001",
  "task_spec": "Write a concise, professional email confirming a meeting time under 100 words",
  "output": "Hi, just confirming our meeting at 3pm tomorrow. Let me know if anything changes."
}
```

### Verification Result

```json
{
  "task_id": "email-approval-001",
  "verdict": "PASS",
  "reason": "Output is concise, professional, and under 100 words. All constraints satisfied.",
  "confidence": "high"
}
```

---

## Decision Rule

* **Proceed only if verdict = PASS**
* **Agents must not override**
* **Operator override must be explicit**

Recommended override note:

```text
OPERATOR OVERRIDE APPROVED
Reason: ...
Approved by: human operator
Timestamp: ...
```

---

## What Verification Means

Verification should be **deterministic and grounded in the task spec**.

Good checks include:

* required fields are present
* constraints are satisfied
* format matches expectations
* instructions were followed
* important omissions are identified

Do not treat these as verification:

* guessing correctness
* relying only on intuition
* blindly trusting confident output
* proceeding because the task feels low-risk

---

## Optional SettlementWitness Verification

You may optionally add a structured verification step for the final result.

Rules:

* keep local verification as the primary decision layer
* use only necessary structured data
* do not send secrets or sensitive content
* external verification is optional, not required

Example:

```text
verify structured verdict metadata against the defined verification spec
```

This can add assurance, but it does not replace local verification or operator judgment.

---

## Data Handling

* Do not include secrets or sensitive data
* Use only the minimum structured information needed for verification
* Treat any external verification step as optional

---

## What This Is Not

* not a code execution tool
* not a payment processor
* not a replacement for clear instructions
* not an autonomous override authority

---

## What This Is

* a **guardrail for agent workflows**
* a **verification gate before execution**
* a **safety layer for autonomous systems**

---

## Outcome

Agents and operators can:

* prevent incorrect execution
* enforce task correctness
* keep workflows on track during autonomous runs
* ensure important actions do not proceed without verification

---

## Keywords

verification, workflow-safety, guardrails, automation, trust
