## Description:

Verifies claims against external state such as GitHub, on-chain transactions, Kalshi markets, HTTP/JSON endpoints, and price feeds, then returns Ed25519-signed, hash-chained receipts that can be checked offline.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stillmarcus24](https://clawhub.ai/user/stillmarcus24)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill when they need a machine-checkable claim verdict and a signed receipt for settlement disputes, agent handoffs, or other workflows where the claim must be checked against external state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Claim text, resolver metadata, and an agent identifier may be sent to the external StillOS/Nola Wealth Financial notary endpoint during live verification.

Mitigation: Use the skill only for claims suitable for that external service, and avoid submitting sensitive or confidential claim details unless the endpoint is approved for that data.

Risk: The offline verifier checks receipt integrity and signature validity, but it does not re-check whether the underlying claim is still true.

Mitigation: Use live resolver verification when current claim truth matters, and use the offline verifier only to confirm that an existing receipt was not forged or modified.

Risk: Installing the Python client with an unconstrained package version can increase supply-chain review burden.

Mitigation: Use an isolated environment and pin or review the stillos package version before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/stillmarcus24/skills/stillos-notary)
- [Claim vocabulary specification](https://nolawealthfinancial.com/evidence/notary-doctrine/claim-vocabulary-spec.json)
- [StillOS Notary API](https://nolawealthfinancial.com/notary)
- [Notary export](https://nolawealthfinancial.com/notary/export)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with inline code, shell commands, JSON examples, and verification guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call an external notary endpoint for live claim resolution; includes an offline Node.js verifier for receipt integrity.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
