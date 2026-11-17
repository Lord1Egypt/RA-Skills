## Description:

Manage TinyTalkingTodos lists and items via the ttt CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joshuacrowley](https://clawhub.ai/user/joshuacrowley)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to manage TinyTalkingTodos lists and todo items from the command line, including authentication, list management, item updates, batch operations, undo, and daemon usage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill operates on a TinyTalkingTodos account and can create, update, batch-edit, and delete synced todo data.

Mitigation: Confirm the target list name or todo ID before mutating commands, use care with delete and force-delete operations, and use undo or history when correcting mistakes.

Risk: The documented global npm install depends on a third-party CLI package.

Mitigation: Review or pin the npm package before global installation and install it only from a trusted package source.

## Reference(s):

- [TinyTalkingTodos homepage](https://tinytalkingtodos.com)
- [ClawHub skill page](https://clawhub.ai/joshuacrowley/skills/ttt)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell command examples and optional JSON CLI output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the ttt CLI binary and an authenticated TinyTalkingTodos account.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
