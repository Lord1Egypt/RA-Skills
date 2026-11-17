## Description:

TMR Land personal agent for an AI business marketplace. Use when: (1) searching for AI/data businesses, (2) publishing purchase intentions, (3) placing and managing escrow orders, (4) evaluating business credit scores, (5) browsing Grand Apparatus predictions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cpy1990](https://clawhub.ai/user/cpy1990)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to search TMR Land businesses, publish buying intentions, manage negotiations and escrow orders, review credit and reputation signals, handle wallet and KYC workflows, and inspect marketplace notifications and disputes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform money-moving actions, including wallet charges, wallet withdrawals, order payment, and escrow release.

Mitigation: Use the narrowest API-key permissions available, keep wallet exposure low, and require explicit user confirmation before payment, withdrawal, or delivery acceptance actions.

Risk: The skill can submit KYC identity data through shell commands and agent-visible transcripts.

Mitigation: Avoid submitting identity numbers through agent workflows unless the user accepts the logging risk; prefer trusted first-party interfaces for sensitive KYC entry.

Risk: The skill forwards TMR_API_KEY to a configurable TMR_BASE_URL.

Mitigation: Leave TMR_BASE_URL unset or set it only to the official HTTPS TMR endpoint before running the scripts.

Risk: The skill can delete or cancel marketplace records and change negotiation or order state.

Mitigation: Confirm destructive or state-changing operations with the user and explain the consequence before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cpy1990/skills/tmrland-personal-demo)
- [TMR Land](https://tmrland.com)
- [TMR Land API](https://tmrland.com/api/v1)
- [API Keys API](references/api-keys-api.md)
- [Authentication API](references/auth-api.md)
- [Businesses API](references/businesses-api.md)
- [Intentions API](references/intentions-api.md)
- [Negotiations API](references/negotiations-api.md)
- [Orders API](references/orders-api.md)
- [Wallet API](references/wallet-api.md)
- [Disputes API](references/disputes-api.md)
- [Credit API](references/credit-api.md)
- [Reviews API](references/reviews-api.md)
- [Grand Apparatus API](references/apparatus-api.md)
- [Error Codes](references/error-codes.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Node.js shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and TMR_API_KEY; TMR_BASE_URL is optional and defaults to the TMR Land HTTPS API.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
