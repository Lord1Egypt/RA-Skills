## Description:

Discover SameDayDesk's twenty-two account-free machine services and produce a verified, non-spending purchase intent from the live OpenAPI contract and unpaid HTTP 402 challenge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[epistemedeus](https://clawhub.ai/user/epistemedeus)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to discover SameDayDesk paid machine services and prepare a point-in-time purchase intent before a separate payment executor is authorized. It is for preflighting operations such as extraction, enrichment, repository scans, audits, DeFi analysis, paid-service search, settlement verification, and wallet-policy conformance without credentials, signing, payment, or replay.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A generated purchase intent may contain a stale or incorrect URL, amount, recipient, network, asset, or operation.

Mitigation: Review the exact target URL, operation, amount, recipient, network, asset, and challenge expiry before handing the intent to a separate payment executor.

Risk: Providing credentials, wallet sessions, private keys, or confidential targets would exceed the skill's non-spending preflight boundary.

Mitigation: Do not provide private keys, wallet sessions, credentials, or confidential targets; use the skill only for credential-free discovery and purchase-intent preparation.

Risk: A purchase intent is point-in-time evidence and does not prove that payment was sent or that the paid service ran.

Mitigation: Treat the intent as planning output only and require separate authorization, execution, and receipt verification for any payment flow.

## Reference(s):

- [SameDayDesk service origin](https://agents.samedaydesk.com)
- [SameDayDesk OpenAPI contract](https://agents.samedaydesk.com/openapi.json)
- [ClawHub skill page](https://clawhub.ai/epistemedeus/skills/samedaydesk-machine-commerce)
- [ClawHub publisher profile](https://clawhub.ai/user/epistemedeus)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or JSON-like purchase intent with operation details, payment challenge fields, and explicit non-payment status flags.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stops before payment and reports credentialsUsed: false, paymentSigned: false, and paymentSent: false.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
