## Description:

VeryEast Job Assistant helps job seekers search VeryEast service-industry jobs, view job details, submit applications, manage resumes, and analyze job fit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kevinwan12334](https://clawhub.ai/user/kevinwan12334)

### License/Terms of Use:

MIT-0

## Use Case:

External job seekers use this skill to find VeryEast service-industry roles, compare listings, update resume sections, submit applications after confirmation, and receive match analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review marks this skill as suspicious because it handles account credentials, resume data, and job-application actions.

Mitigation: Install only when the VeryEast integration is trusted, avoid shared or heavily logged machines, and clear the stored credential when finished.

Risk: Environment variables can override the VeryEast endpoint or API key used by the skill.

Mitigation: Review VEAST_MCP_URL and VEAST_API_KEY before use and run the skill only in a controlled environment.

Risk: The skill can edit resume sections and submit job applications through authenticated actions.

Mitigation: Require explicit user confirmation for applications and review resume changes before accepting write actions.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/kevinwan12334/skills/veryeast-assistant)
- [VeryEast homepage](https://www.veryeast.cn)
- [Agent guide](references/agent-guide.md)
- [API reference](references/api.md)
- [Common scenarios](references/scenarios.md)
- [Match scoring dimensions](references/scoring.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Human-facing Markdown/text with job tables, links, confirmations, and command-backed API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a VeryEast account credential and may read or update resume data and submit applications after user confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 0.8.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
