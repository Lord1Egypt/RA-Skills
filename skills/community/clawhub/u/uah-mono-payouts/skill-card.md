## Description: <br>
Use when a user wants an agent to convert USDT BEP20 into UAH payout instructions through a verified exchanger flow with approval, expiry, and payment monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[swiftadviser](https://clawhub.ai/user/swiftadviser) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to prepare USDT BEP20 to Monobank UAH payout flows through an MCP-backed exchanger process. It supports route quoting, human approval, exact payment instructions, expiry checks, and order status monitoring. <br>

### Deployment Geography for Use: <br>
Global, for UAH Monobank payout workflows where the user is authorized to use the required payment rails. <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create crypto-to-bank exchange orders and produce payment instructions for USDT BEP20 transfers. <br>
Mitigation: Require human approval before showing send instructions, verify the approval URL, amount, network, memo/comment, expiry time, and support path before funds are sent. <br>
Risk: Wrong network, wrong amount, missing memo/comment, or reuse of an expired order can lead to loss of funds. <br>
Mitigation: Show BEP20 / BNB Smart Chain explicitly, require exact amounts and comments, refuse orders expiring in under 60 seconds, and stop when status is unclear. <br>
Risk: Hardcoded fallback Telegram and email contacts may route payout support or contact details to an unintended third party. <br>
Mitigation: Use contact-specific Telegram and email values when available, and allow the built-in @SwiftAdviser or swiftadviser@gmail.com fallback only when it is intentionally part of the payout flow. <br>
Risk: The workflow depends on an external MCP service and exchanger data. <br>
Mitigation: Install only if the MCP service and exchanger workflow are trusted, and fail closed when MCP availability, quote data, approval state, or provider status is unclear. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/swiftadviser/uah-mono-payouts) <br>
- [Publisher Profile](https://clawhub.ai/user/swiftadviser) <br>
- [MCP Wallet Homepage](https://mcp-wallet.mandate.md) <br>
- [Required MCP Server](https://mcp-wallet.mandate.md/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Guidance] <br>
**Output Format:** [Markdown with operational payout summaries, approval links, exact payment instruction fields, and status updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include exchanger names, order IDs, BEP20 network details, exact amounts, deposit addresses, memo/comment values, expiry times, support paths, and final order states.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
