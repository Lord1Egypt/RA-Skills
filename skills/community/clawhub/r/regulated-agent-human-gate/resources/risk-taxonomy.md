# Risk Taxonomy

Risk levels:

- `LOW`: read-only, authorized, reversible, no funds movement, no sensitive identity change.
- `MEDIUM`: small value transfer, sensitive read, routine known beneficiary, mild device or confidence concern.
- `HIGH`: high value, new beneficiary, missing evidence, low confidence, agent scope gap, loan approval recommendation, duplicate payment.
- `CRITICAL`: sanctions hit, identity mismatch, account-control change, beneficiary account change, prompt injection, amount mutation, rejected approval retry, AML high risk.

Risk factors to inspect:

- Action type and requested execution authority.
- Amount, currency, and user historical behavior.
- New beneficiary or changed beneficiary account.
- Device, IP, geography, and session freshness.
- Identity status, liveness, and authority verification.
- AML, sanctions, and provider certainty.
- Reversibility and regulated-finance activity.
- Evidence completeness and audit-store availability.

