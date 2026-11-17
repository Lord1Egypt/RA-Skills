## Description:

Chat with Sally about metabolic health, blood sugar, A1C, nutrition, fasting, supplements, and lab results. Uses the Sally MCP server on Smithery with x402 micropayments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sally-labs](https://clawhub.ai/user/sally-labs)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to ask Sally health-education questions about metabolic health topics and receive Sally's response with any included citations. The skill also guides setup of the Smithery-hosted Sally MCP server using an x402 wallet.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow asks users to place a wallet private key in a command-line connection string for Smithery-hosted x402 payments.

Mitigation: Use a dedicated low-balance wallet, avoid using a primary wallet, and rotate any key that may have been exposed in shell history.

Risk: Health-related messages are forwarded to external services.

Mitigation: Avoid sending names, dates of birth, medical record identifiers, or other unnecessary personal health details.

Risk: The skill provides health education and may discuss labs, supplements, fasting, nutrition, and metabolic health.

Mitigation: Do not add independent medical commentary to Sally's response, and recommend consultation with a healthcare professional for medical decisions.

## Reference(s):

- [Sally AI homepage](https://asksally.xyz)
- [Sally MCP source link from skill documentation](https://github.com/sally-labs/sally-mcp)
- [x402 protocol](https://www.x402.org/)
- [Smithery Sally AI MCP registry](https://smithery.ai/servers/sally-labs/sally-ai-mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and Sally MCP response text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves Sally-provided citations and instructs the agent to pass the user's message exactly as-is.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
