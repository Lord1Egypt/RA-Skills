## Description:

Use when a user wants an agent to convert USDT BEP20 into UAH payout instructions through a verified exchanger flow with approval, expiry, and payment monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[swiftadviser](https://clawhub.ai/user/swiftadviser)

### License/Terms of Use:

MIT-0

## Use Case:

External users and personal-agent operators use this skill to route USDT on BEP20 / BNB Smart Chain into UAH Monobank card or IBAN payout instructions through an MCP-backed exchanger flow with approval and status monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles real payout data and sends bank/card or IBAN details, recipient names, Telegram handles, and email fields to an MCP service.

Mitigation: Install only if the MCP service operator is trusted, and require the agent to show the exact destination, amount, recipient banking fields, contact fields, exchanger route, expiry, and approval link before funds move.

Risk: Hardcoded fallback Telegram and email contacts may be used when recipient contact details are missing.

Mitigation: Require contact details from local agent context or direct user input, and do not allow hardcoded fallback contacts for missing recipient information.

Risk: Wrong network, wrong amount, missing memo/comment, unclear approval, or reused expired orders can lose funds.

Mitigation: Show BEP20 / BNB Smart Chain, exact amount, memo/comment, expiry, and approval state; stop if the MCP service is unavailable, status is unclear, approval is missing, or the order expires in under 60 seconds.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/swiftadviser/skills/uah-mono-payouts)
- [MCP wallet homepage](https://mcp-wallet.mandate.md)
- [MCP wallet server](https://mcp-wallet.mandate.md/mcp)
- [Publisher profile](https://clawhub.ai/user/swiftadviser)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Short Markdown-style operational messages with structured payout details and MCP tool calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes exact amount, network, exchanger route, approval URL, expiry, payment instructions, support details, and final status when available.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
