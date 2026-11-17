# Supplier Payment Agent

An agent proposes a USD 8,000 cross-border supplier payment to a new beneficiary. The frozen action is in `supplier-payment-action.json`; the completed control decision is in `supplier-payment-decision.json`.

Expected authorization plan:

- Routing decision: `HUMAN_APPROVAL`.
- Risk: `HIGH`.
- Cumulative controls: standard audit logging, user confirmation, identity verification, authority verification, beneficiary verification, and independent human approval.
- Action binding: decision and delegation receipt contain the exact action hash.
- Execution: blocked until every control passes and the authorized service verifies and consumes a short-lived receipt.
- Mutation behavior: any amount, currency, target, tenant, subject, agent, or action change invalidates the receipt.
- Replay behavior: a second use of the same nonce or receipt ID is rejected.

This example illustrates the control contract, not a claim that an HMAC key stored beside an agent is production-safe. Keep production signing keys in a trusted managed boundary.
