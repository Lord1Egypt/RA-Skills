## Description:

Create VS Code Copilot custom Agent (.agent.md) files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to create VS Code Copilot custom agent files, define specialized agent roles, configure tool permissions, and document handoff workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated agent files may grant broader tool access, handoff behavior, user-level availability, or hook commands than intended.

Mitigation: Review generated agent files before use, especially tools, agents, handoffs.send, user-level install paths, and hooks command entries; prefer the minimum permissions needed for the agent's role.

## Reference(s):

- [VS Code Custom Agent Complete Format Reference](references/agent-format.md)
- [ClawHub skill page](https://clawhub.ai/openlark/skills/vscode-agent-creator)
- [OpenLark publisher profile](https://clawhub.ai/user/openlark)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with YAML frontmatter examples and agent file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent authoring guidance and example .agent.md content; users should review generated tools, handoffs, and hooks before use.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
