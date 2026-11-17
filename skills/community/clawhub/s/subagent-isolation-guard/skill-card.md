## Description:

Subagent Isolation Guard documents workspace isolation and semantic routing bypass practices for subagent sessions to reduce cross-agent context contamination and unintended model switching.

This skill is ready for commercial/non-commercial use.

## Publisher:

[halfmoon82](https://clawhub.ai/user/halfmoon82)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to keep subagent workspaces separate and ensure subagent sessions marked with `:subagent:` bypass semantic routing logic only for the intended isolation workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Routing bypass behavior could skip semantic routing controls outside the intended subagent isolation use case if session markers are applied too broadly.

Mitigation: Review the routing change in the target environment and limit the `:subagent:` marker to isolated subagent sessions with distinct `agentDir` values.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/halfmoon82/skills/subagent-isolation-guard)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with configuration rules]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only skill with no executable code or hidden install behavior.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
