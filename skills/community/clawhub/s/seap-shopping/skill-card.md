## Description:

Supports OpenClaw shopping flows for immediate and scheduled product purchases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pingjiang](https://clawhub.ai/user/pingjiang)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users can use this skill to search for products, choose an item, and request either immediate purchase or a scheduled purchase task.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill combines payment and scheduled-purchase authority with broad activation on purchase-related language.

Mitigation: Require narrow explicit purchase intent and a final confirmation that shows item, price, address, time, and total charge before any purchase or scheduled task runs.

Risk: Credential and payment token handling may expose sensitive purchase authority.

Mitigation: Store secrets in a secure secret manager, avoid committing real credentials to configuration files, and restrict access to payment tokens.

Risk: Scheduled purchase tasks may be difficult to reverse.

Mitigation: Provide a clear cancellation path and show the scheduled task identifier and execution time to the user.

Risk: A mock purchase path can report success, which may mislead users about whether a real transaction occurred.

Mitigation: Label simulation behavior clearly or require provider-confirmed transaction status before reporting a purchase as successful.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pingjiang/skills/seap-shopping)
- [ClawHub publisher profile](https://clawhub.ai/user/pingjiang)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown product listings, JSON command output, and setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses session-scoped JSON files for search and purchase state.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
