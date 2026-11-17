## Description:

Interact with Codeberg using the `x cb` CLI to manage repositories, issues, pull requests, organizations, teams, and users.

This skill is ready for commercial/non-commercial use.

## Publisher:

[curry798](https://clawhub.ai/user/curry798)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to have an agent propose `x cb` commands for Codeberg repository, issue, pull request, organization, team, and user workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A broad Codeberg token could allow unintended repository, issue, pull request, collaborator, or team changes.

Mitigation: Use a least-privilege Codeberg token and avoid exposing it in prompts or logs.

Risk: State-changing `x cb` commands could create or modify Codeberg resources.

Mitigation: Review and confirm commands before running actions that create repositories, issues, pull requests, collaborators, or teams.

## Reference(s):

- [Codeberg application tokens](https://codeberg.org/user/settings/applications)
- [ClawHub skill page](https://clawhub.ai/curry798/skills/x-cb)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may create or change Codeberg resources and should be reviewed before execution.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
