## Description:

SA Master helps architects turn BA or product requirement assets into standardized system architecture design documents, interface documentation, deployment implementation guides, and detailed design review reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leo21cn](https://clawhub.ai/user/leo21cn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, architects, and engineering teams use this skill to generate architecture design deliverables from confirmed business requirements and to review detailed designs for architecture consistency and requirement coverage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Project requirements and architecture context may be sent to a fixed remote MCP service.

Mitigation: Use only with trusted projects, confirm data-sharing approval, and avoid confidential inputs unless the endpoint is approved.

Risk: The release ships an embedded bearer token.

Mitigation: Revoke or replace the token with per-user secure authentication before installation.

Risk: The remote service can supply part of the runtime protocol.

Mitigation: Pin or locally validate the expected protocol before relying on tool responses.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leo21cn/skills/sa-master)
- [Remote MCP service endpoint](https://mcp.smartmoves.com.cn/sa/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown documents with Mermaid diagrams, configuration guidance, and review conclusions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce staged architecture deliverables, interface specifications, deployment guidance, and detailed design review reports.]

## Skill Version(s):

1.8.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
