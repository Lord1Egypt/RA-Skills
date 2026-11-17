## Description:

Dispatches one-shot workers through other vendors’ CLIs using the user’s existing logins for second opinions, cross-model reviews, or task-specific responses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[escoffier-labs](https://clawhub.ai/user/escoffier-labs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use the skill to request a one-shot answer or work product from another model provider through a CLI they already use. It supports cross-model reviews, second opinions, and provider-specific tasks without an orchestration framework.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Disabling named editing tools does not restrict shell commands, so an agent may still modify files.

Mitigation: Use enforced read-only execution for questions and isolated, disposable workspaces for edits.

Risk: Dispatching tasks sends their content and project information to another model provider.

Mitigation: Share only task content and project information authorized for that selected provider.

## Reference(s):

- [Stagiaire on ClawHub](https://clawhub.ai/escoffier-labs/skills/skillet-stagiaire)
- [Brigade](https://github.com/escoffier-labs/brigade)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration instructions]

**Output Format:** [Worker responses as text, with Markdown guidance and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One worker response per dispatch; exact task and CLI parameters vary by provider.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
