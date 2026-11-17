## Description:

AI-powered energy sector knowledge management. Search power generation records, grid management data, regulatory filings, and safety protocols with structured extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roojenkins](https://clawhub.ai/user/roojenkins)

### License/Terms of Use:

MIT-0

## Use Case:

Energy operations, compliance, engineering, environmental, and regulatory affairs teams use this skill to search organization-specific power generation, grid management, regulatory filing, safety, and environmental documentation. It supports workflows such as NERC audit preparation, outage investigation, rate case research, safety incident review, and retrieval of current operational directives.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill accesses sensitive energy-sector records, including safety-critical and CEII-related knowledge.

Mitigation: Verify user role and clearance before queries, enforce classification tiers, and use least-privilege UPLO tokens.

Risk: The configured MCP package is auto-downloaded and may expose broad export or conversation logging capabilities.

Mitigation: Use a pinned and reviewed MCP package version, verify HTTPS endpoints, and enable exports or logging only when allowed by role and retention policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/roojenkins/skills/uplo-energy)
- [UPLO](https://uplo.ai)
- [UPLO schemas](https://uplo.ai/schemas)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured UPLO instance URL and least-privilege MCP token; responses should respect role, clearance, and classification tiers.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
