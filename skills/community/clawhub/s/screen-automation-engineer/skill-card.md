## Description:

Provides strong screen understanding and control with local screen-vision technology, and creates and maintains automation workflows through natural language.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaozs-com](https://clawhub.ai/user/xiaozs-com)

### License/Terms of Use:

MIT-0

## Use Case:

External users and automation engineers use this skill to interpret screens, complete desktop tasks, and design, validate, and deliver reusable workflows for Windows and macOS.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Python workflow extensions can access files, network, and programs with the current user's permissions.

Mitigation: Install only trusted workflows; do not treat permission declarations or static checks as a system sandbox.

Risk: Managed browser profiles can retain logged-in sessions, and screenshots may expose sensitive screen content to an external provider.

Mitigation: Confirm the provider, screenshot scope, and purpose before external sharing; avoid credentials and unrelated private information.

Risk: Generated workflow steps may be incorrect, and authentication, payment, or other high-risk actions can have serious consequences.

Mitigation: Review generated steps and supervise the first run; pause for the user to complete credentials and high-risk actions, then verify the resulting state.

## Reference(s):

- [Screen Automation](https://www.xiaozs.com/sah/)
- [Workflow code trust boundaries](references/workflow-trust.md)
- [Workflow agent phases](references/workflow-agent-phases.md)
- [Workflow lifecycle](references/workflow-lifecycle.md)
- [Current-task operations](references/current-task.md)
- [User guide](references/user-guide.md)

## Skill Output:

**Output Type(s):** [Guidance, Text, Markdown, Shell commands, Code, Configuration]

**Output Format:** [Conversational guidance and Markdown workflow files, with shell commands and optional Python extensions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include workflow steps, parameters, permissions, validation, and delivery instructions.]

## Skill Version(s):

1.2.6 (source: SKILL.md frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
