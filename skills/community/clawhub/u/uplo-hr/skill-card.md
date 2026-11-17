## Description:

AI-powered HR knowledge management. Search employee handbooks, org charts, company policies, benefits documentation, and onboarding materials with structured extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roojenkins](https://clawhub.ai/user/roojenkins)

### License/Terms of Use:

MIT-0

## Use Case:

HR, people operations, managers, and employees use this skill to search organization-specific HR policies, benefits documentation, onboarding materials, org charts, and workforce guidance through UPLO.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose sensitive HR search and export capabilities.

Mitigation: Use least-privilege UPLO tokens restricted to the HR data and classification levels the user actually needs, and avoid broad exports unless explicitly authorized.

Risk: The skill runs an unpinned npm MCP server automatically.

Mitigation: Prefer a pinned, reviewed MCP server version or isolated runtime before using the skill with confidential HR data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/roojenkins/skills/uplo-hr)
- [UPLO](https://uplo.ai)
- [UPLO schemas](https://uplo.ai/schemas)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May query HR knowledge, directives, organizational context, knowledge owners, gaps, and proposed updates through the configured UPLO MCP server.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
