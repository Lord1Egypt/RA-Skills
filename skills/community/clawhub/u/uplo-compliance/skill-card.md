## Description:

AI-powered compliance intelligence spanning legal, financial, and government regulatory requirements with unified search across compliance obligations, audit findings, and regulatory filings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roojenkins](https://clawhub.ai/user/roojenkins)

### License/Terms of Use:

MIT-0

## Use Case:

GRC teams, compliance officers, outside counsel, auditors, and finance controllers use this skill to search organizational compliance knowledge, assess regulatory change impact, prepare audits, and propose updates to compliance records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs an unpinned MCP package and depends on the @agentdocs1 npm package supply chain.

Mitigation: Use a pinned, reviewed MCP server version before deployment.

Risk: The skill uses a secret token to connect to a UPLO endpoint.

Mitigation: Configure a least-privilege, revocable token and install only when the endpoint is trusted.

Risk: The skill can expose broad organizational compliance context, including regulated or restricted compliance data.

Mitigation: Require explicit approval before exporting organizational context or using regulated compliance data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/roojenkins/skills/uplo-compliance)
- [Publisher profile](https://clawhub.ai/user/roojenkins)
- [UPLO](https://uplo.ai)
- [UPLO schemas](https://uplo.ai/schemas)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline tool calls, shell commands, and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May surface regulated compliance context subject to configured classification tiers and token scope.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
