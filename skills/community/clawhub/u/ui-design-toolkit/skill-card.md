## Description:

This skill helps agents design clear, consistent, and visually polished user interfaces with guidance for design systems, components, responsive layouts, and accessibility.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and product teams use this skill to ask an agent for UI design guidance, design-token systems, component patterns, responsive layouts, and accessibility-aware HTML or CSS examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad read, write, and command-execution authority that is not clearly scoped to UI work.

Mitigation: Review the skill before installing it, and allow it only in projects where reading and writing UI files and running explicit build or test commands is acceptable.

Risk: Broad tool access could expose unrelated private files or secrets if the agent is given excessive workspace or credential access.

Mitigation: Avoid providing broad API keys or access to unrelated private files when using this skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/ui-design-toolkit)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with optional code blocks and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include UI design checklists, design-token snippets, HTML/CSS examples, troubleshooting steps, and command suggestions.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
