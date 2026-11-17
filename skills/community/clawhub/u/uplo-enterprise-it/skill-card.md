## Description:

AI-powered enterprise IT intelligence spanning DevOps, cybersecurity, and engineering. Unified search across infrastructure, security, and architecture documentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roojenkins](https://clawhub.ai/user/roojenkins)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, SREs, security analysts, and enterprise IT teams use this skill to search and connect infrastructure, cybersecurity, architecture, incident, and compliance knowledge. It supports operational lookups, incident triage, audit preparation, directive retrieval, and documentation gap reporting through UPLO-backed MCP tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can export broad organizational infrastructure, security, and engineering context into an agent session.

Mitigation: Use a dedicated least-privilege UPLO token and require human approval before calling export_org_context.

Risk: The MCP server is launched through an unpinned external npm package.

Mitigation: Prefer a pinned, reviewed package version and install only after trusting the UPLO service and MCP package supply chain.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/roojenkins/skills/uplo-enterprise-it)
- [UPLO](https://uplo.ai)
- [UPLO schemas](https://uplo.ai/schemas)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline tool calls, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference UPLO search results, organizational context, directives, and documentation quality signals subject to configured access controls.]

## Skill Version(s):

1.0.0 (source: skill.json and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
