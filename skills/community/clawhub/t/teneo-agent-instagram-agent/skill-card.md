## Description:

The Instagram Agent extracts public Instagram profile, post, hashtag, and comment data through Teneo Protocol commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teneoprotocoldev](https://clawhub.ai/user/teneoprotocoldev)

### License/Terms of Use:

MIT-0

## Use Case:

External users, businesses, researchers, and developers use this skill to retrieve public Instagram data for profile audits, hashtag monitoring, competitor research, and sentiment analysis. Developers can integrate the Teneo SDK commands into monitoring or analysis workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connecting a real wallet can authorize wallet-backed automatic USDC payments.

Mitigation: Use an external or hardware signer and independently confirm the network, token, recipient, amount, and spending limits before approving payments.

Risk: Installing an unpinned SDK can pull mutable dependency code.

Mitigation: Pin package versions, commit a lockfile, and review dependency changes before running the skill in a production workflow.

Risk: Monitoring targets or retrieved public identifiers may involve sensitive or regulated data handling.

Mitigation: Submit only authorized public targets and avoid regulated personal data unless Teneo-operated infrastructure is approved for that use.

## Reference(s):

- [Teneo Agent SDK on ClawHub](https://clawhub.ai/teneoprotocoldev/teneo-agent-sdk)
- [Teneo Protocol SDK on npm](https://www.npmjs.com/package/@teneo-protocol/sdk)
- [Teneo Agent SDK GitHub Repository](https://github.com/TeneoProtocolAI/teneo-agent-sdk)
- [Teneo Protocol](https://teneo-protocol.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash and TypeScript code blocks; runtime agent responses may include formatted text or structured content.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands accept an Instagram target, optional count, and selected Teneo payment network.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
