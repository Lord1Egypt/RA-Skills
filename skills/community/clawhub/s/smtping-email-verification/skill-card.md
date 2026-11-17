## Description:

Verifies individual email addresses or contact lists with SMTPing and recommends which addresses to send to, remove, or review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smtping](https://clawhub.ai/user/smtping)

### License/Terms of Use:

MIT-0

## Use Case:

People managing contact lists use this skill to check addresses before sending or importing them, review risk verdicts, and check their SMTPing credit balance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Verifying addresses sends them to SMTPing's API.

Mitigation: Process only addresses the user has a legitimate reason to check and confirm they are comfortable sharing them with SMTPing.

Risk: An exposed API key could allow unauthorized use.

Mitigation: Set SMTPING_API_KEY privately and never paste or reveal it in chat.

Risk: Bulk verification and threat checks spend account credits.

Mitigation: Deduplicate addresses and confirm the count and estimated credit cost before checks of more than 100 addresses.

Risk: Installing the suggested MCP package runs third-party code.

Mitigation: Review or pin the package before using the suggested npx installation path.

## Reference(s):

- [SMTPing documentation](https://smtping.com/docs)
- [SMTPing email verification for AI agents](https://smtping.com/email-verification-ai-agent)
- [SMTPing MCP integration](https://smtping.com/email-verification-mcp)
- [ClawHub skill listing](https://clawhub.ai/smtping/skills/smtping-email-verification)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown summaries with optional CSV or shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single-address verdicts or list totals and removal candidates; optional email,status,band CSV for longer lists.]

## Skill Version(s):

1.0.2 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
