# Provider matrix (starter template)

Use this file to compare candidate providers before committing.

## Comparison table

| Field | Provider A | Provider B | Provider C |
| --- | --- | --- | --- |
| Sandbox quality |  |  |  |
| Onboarding/KYC time |  |  |  |
| UPI collect support |  |  |  |
| UPI intent support |  |  |  |
| Dynamic QR support |  |  |  |
| Mandates/autopay support |  |  |  |
| Webhook reliability |  |  |  |
| Reconciliation exports/API |  |  |  |
| Refund API maturity |  |  |  |
| Dispute tooling |  |  |  |
| Pricing model |  |  |  |
| Settlement cycle |  |  |  |
| Support SLA |  |  |  |
| Production cutover support |  |  |  |

## Mandatory questions to answer

- What are provider-side transaction limits and risk controls?
- Which identifiers can support use for tracking (UTR, provider ID, order ID)?
- How are duplicates and retries represented in provider status APIs?
- What is the expected webhook retry behavior and max retry duration?
- How quickly can support confirm final payment status during incidents?

## Decision rule

Choose provider only after all fields above have evidence links and owners.

