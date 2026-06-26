# Use Case Examples

## 1. Payment Approval

Task: Pay an approved contractor invoice.

Verification spec:
- invoice amount matches the approved amount
- payee matches the approved vendor
- due date and currency are correct
- required approvals are present

Decision rule:
- PASS -> proceed
- FAIL or INDETERMINATE -> halt until reviewed

## 2. Email Before Sending

Task: Draft and send a client email.

Verification spec:
- recipient is correct
- requested points are included
- no incorrect claims are present
- tone matches the instructions

Decision rule:
- PASS -> send
- FAIL or INDETERMINATE -> revise before sending

## 3. Social Post Before Publishing

Task: Publish a promotional post.

Verification spec:
- message matches campaign brief
- product details are accurate
- no banned claims appear
- required link or call to action is included

Decision rule:
- PASS -> publish
- FAIL or INDETERMINATE -> stop and correct

## 4. Autonomous Workflow Guardrail

Task: Continue an automated workflow step.

Verification spec:
- previous step completed successfully
- output matches required format
- no critical fields are missing
- action is still within scope

Decision rule:
- PASS -> continue workflow
- FAIL or INDETERMINATE -> halt and notify operator
