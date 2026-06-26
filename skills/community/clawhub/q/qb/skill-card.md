## Description: <br>
This release is labeled as a QuickBooks/accounting skill, but the artifact content implements CreditClaw payment and wallet workflows for agent shopping, checkout pages, invoices, and owner-approved encrypted-card purchases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TripleHippo](https://clawhub.ai/user/TripleHippo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use the artifact's CreditClaw workflows to register an agent wallet, check spending permissions, request purchases, create payment links, issue invoices, and manage wallet status with owner approval. Reviewers should note the mismatch between the public QuickBooks/accounting listing and the payment-commerce behavior in the artifact. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The public listing suggests QuickBooks/accounting, while the artifact enables CreditClaw payment and commerce workflows. <br>
Mitigation: Install only when the intended use is CreditClaw payment, wallet, checkout, invoice, or purchasing functionality. <br>
Risk: The skill grants broad financial authority and can initiate purchases, payment links, invoices, seller-profile updates, and wallet operations. <br>
Mitigation: Use a limited and revocable API key, keep human approval required for purchases and public seller actions, and review spending rules before each transaction. <br>
Risk: Encrypted-card checkout can expose sensitive card, identity, billing, and shipping data if run in the main agent context or logged. <br>
Mitigation: Use an ephemeral checkout sub-agent where available, never store or log decrypted card data, and run checkout in a disposable sandbox with restricted filesystem, logging, and network access. <br>
Risk: The CreditClaw API key authorizes sensitive payment operations. <br>
Mitigation: Store CREDITCLAW_API_KEY in a secure secrets manager and send it only to CreditClaw API endpoints. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/TripleHippo/qb) <br>
- [Publisher profile](https://clawhub.ai/user/TripleHippo) <br>
- [CreditClaw skill documentation](https://creditclaw.com/creditcard/skill.md) <br>
- [CreditClaw checkout guide](https://creditclaw.com/creditcard/checkout.md) <br>
- [CreditClaw encrypted-card guide](https://creditclaw.com/creditcard/encrypted-card.md) <br>
- [CreditClaw spending guide](https://creditclaw.com/creditcard/spending.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls] <br>
**Output Format:** [Markdown with inline shell commands, JSON request and response examples, and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CREDITCLAW_API_KEY and access to CreditClaw payment endpoints.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata); artifact package version 2.3.1 <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
