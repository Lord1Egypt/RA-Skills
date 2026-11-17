## Description:

Connects OpenClaw agents to SatGate Cloud for credit-budgeted MCP tool calls and signed decision receipts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[matt-dean-git](https://clawhub.ai/user/matt-dean-git)

### License/Terms of Use:

MIT-0

## Use Case:

Developers configuring OpenClaw agents use this skill to connect to SatGate Cloud with separately minted, budgeted tokens and check signed receipts for allowed or budget-refused tool calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An exposed agent token can be used to access its configured tools and budget.

Mitigation: Mint a fresh token per agent, confirm its tool access and budget, and never print or commit the config containing it.

Risk: A signed receipt could be mistaken for proof of an upstream tool's actions.

Mitigation: Treat receipts as evidence of SatGate's recorded decision, not of downstream tool behavior.

## Reference(s):

- [SatGate homepage](https://satgate.io)
- [SatGate receipt verification](https://satgate.io/verify-evidence-pack)
- [SatGate public verification keys](https://satgate-mcp-saas.fly.dev/.well-known/jwks.json)
- [SatGate ClawHub release](https://clawhub.ai/matt-dean-git/skills/satgate)

## Skill Output:

**Output Type(s):** [Configuration guidance, Shell commands, Text]

**Output Format:** [Markdown with command and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance for checking signed decisions; receipts do not establish what an upstream tool did after an allowed call.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
