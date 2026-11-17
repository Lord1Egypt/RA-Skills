## Description:

Search candidates, manage jobs, view pipelines, track billing and team performance in Recruitly CRM via MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[willgary](https://clawhub.ai/user/willgary)

### License/Terms of Use:


## Use Case:

Recruiting teams and agents use this skill to connect to Recruitly CRM, search candidates, contacts, companies, jobs, and pipelines, and summarize CRM activity through MCP.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill lets an agent access Recruitly CRM through a bearer token.

Mitigation: Use a token scoped to the account access you are comfortable granting, and revoke or rotate it if you stop using the skill.

Risk: Tenant-specific status and type labels can make filtered searches inaccurate if the agent assumes fixed values.

Mitigation: Call list_options before filtering jobs, candidates, or activities by status or type.

## Reference(s):

- [Recruitly](https://recruitly.io)
- [Recruitly MCP Server](https://recruitly.io/mcp)
- [Recruitly MCP Sign-In](https://mcp.recruitly.dev)
- [ClawHub Skill Page](https://clawhub.ai/willgary/skills/recruitly-mcp)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, Shell commands]

**Output Format:** [Markdown instructions with JSON configuration and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires mcporter and RECRUITLY_TOKEN; search results are capped at 50 per request.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
