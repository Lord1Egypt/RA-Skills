## Description:

Runs project-defined custom subagents through headless Claude Code so each can use the model specified in its agent file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ysskrishna](https://clawhub.ai/user/ysskrishna)

### License/Terms of Use:

MIT

## Use Case:

Developers using Cursor can run project-defined custom subagents through Claude Code when Cursor would otherwise use the parent model, so each agent can run with the model specified in its agent file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Project content read by a cloud-backed Claude Code subagent may be sent to Anthropic.

Mitigation: Review data-handling requirements before invoking the skill on project content, and use it only when the applicable Anthropic processing is approved.

Risk: The skill runs custom subagents using the Claude model specified in each agent file, which may not be the model or account the user intended to use.

Mitigation: Inspect the relevant agent files and confirm the selected models and account are appropriate before running the subagents.

## Reference(s):

- [Model mapping guidance](references/model-mapping.md)
- [Worked example](references/example.md)
- [Claude Code setup guide](https://code.claude.com/docs/en/setup)
- [Permissions guide](https://github.com/ysskrishna/claude-code-subagents-for-cursor/blob/main/docs/guides/permissions.md)
- [ClawHub release](https://clawhub.ai/ysskrishna/skills/use-claude-code-subagents)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instructions for selecting and running project-defined custom subagents; no generated files are specified.]

## Skill Version(s):

1.3.4 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
