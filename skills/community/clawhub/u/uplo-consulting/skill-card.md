## Description:

AI-powered consulting knowledge management. Search engagement records, methodology frameworks, deliverable templates, and best practices with structured extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roojenkins](https://clawhub.ai/user/roojenkins)

### License/Terms of Use:

MIT-0

## Use Case:

Consulting teams and developers use this skill to query UPLO-backed engagement records, methodology frameworks, deliverable templates, case studies, proposal archives, and best-practice libraries. It supports proposal development, engagement kickoff, staffing research, knowledge transfer, and lessons-learned workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs an unpinned external MCP package at runtime with npx -y.

Mitigation: Prefer a pinned, reviewed MCP server package or controlled deployment before installing.

Risk: The skill can access sensitive firm and client context through UPLO.

Mitigation: Use only with an UPLO instance and token scoped to the user's authorized practice, clients, and classification tiers.

Risk: Organization exports and logs may expose client-identifying or proprietary information.

Mitigation: Avoid full organization exports or client-identifying logs unless they are necessary and authorized.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/roojenkins/skills/uplo-consulting)
- [UPLO](https://uplo.ai)
- [UPLO schemas](https://uplo.ai/schemas)
- [Publisher profile](https://clawhub.ai/user/roojenkins)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline tool-call and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an UPLO instance URL and API key scoped to authorized content.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
