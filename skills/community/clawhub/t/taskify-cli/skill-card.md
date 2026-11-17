## Description:

Manage tasks, boards, and calendar events via the Taskify CLI (`taskify` command).

This skill is ready for commercial/non-commercial use.

## Publisher:

[ink-north](https://clawhub.ai/user/ink-north)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and agents use this skill to manage Taskify tasks, boards, assignments, deadlines, imports, exports, and AI-assisted triage through the `taskify` CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on the third-party `taskify-nostr` npm package and source repository.

Mitigation: Verify the npm package and source repository before installation, and prefer a user-local install when possible.

Risk: Some board operations can delete or clear task data.

Mitigation: Confirm the target board and recovery expectations before running destructive cleanup, column deletion, or task deletion commands.

Risk: `taskify agent` commands can forward task text to a configured AI backend.

Mitigation: Use agent commands only with trusted or self-hosted AI backends, especially for boards containing sensitive data.

## Reference(s):

- [Taskify CLI Full Command Reference](references/commands.md)
- [Taskify Boards and Columns Reference](references/boards.md)
- [taskify-nostr npm package](https://www.npmjs.com/package/taskify-nostr)
- [Taskify release source repository](https://github.com/Solife-me/Taskify_Release)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline shell commands and JSON parsing examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may recommend `--json` for machine-readable Taskify CLI output.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
