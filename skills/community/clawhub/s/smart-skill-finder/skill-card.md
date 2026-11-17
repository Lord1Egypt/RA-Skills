## Description:

Finds and recommends relevant AI agent skills across multiple ecosystems (Skills CLI, Clawhub, GitHub) using intelligent semantic understanding to match user needs with available capabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edkuo7](https://clawhub.ai/user/edkuo7)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to discover relevant agent skills across Skills CLI, ClawHub, and GitHub from natural language requests and receive ranked recommendations with installation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe local command execution is reported for the npx-based Skills CLI search path.

Mitigation: Review and fix the command invocation before installation or use, and avoid running the skill in sensitive workspaces until corrected.

Risk: The skill may overstate security verification for recommended third-party skills.

Mitigation: Treat all recommendations as unverified leads and manually review each suggested skill, source, and scan status before installing.

Risk: Search queries may reveal sensitive project names or confidential task descriptions to external services.

Mitigation: Use non-confidential queries unless the external data flows and CLI behavior are disclosed, reviewed, and controlled.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/edkuo7/skills/smart-skill-finder)
- [Publisher profile](https://clawhub.ai/user/edkuo7)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown response with ranked recommendations and inline installation commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Limits recommendations to the most relevant results and includes security status when available.]

## Skill Version(s):

1.0.0 (source: package.json, CHANGELOG, and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
