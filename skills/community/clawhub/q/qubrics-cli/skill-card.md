## Description:

Use the Qubrics CLI for durable agent inbox registration, owner invites, profiles, and terminal-driven Management, Mailbox, and Sending workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roshanjonah](https://clawhub.ai/user/roshanjonah)

### License/Terms of Use:

MIT-0

## Use Case:

Developers building agents use this skill to register Qubrics inboxes, manage profiles and credentials, and carry out mailbox, sending, and account management tasks from the terminal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review had incomplete coverage because several local path-like references could not be resolved, and its overall confidence is medium.

Mitigation: Review those referenced files and the CLI package source before installation.

Risk: Commands can access account data or make mailbox and sending changes using local credentials.

Mitigation: Keep credentials in a secret store, clear inherited credentials before setup, verify the selected account identity before reads or mutations, and confirm destructive actions explicitly.

## Reference(s):

- [Qubrics OAuth for REST APIs](https://qubrics.com/docs/developer-tools/oauth)
- [Qubrics project homepage (listed in skill metadata)](https://github.com/qubrics/skills)
- [ClawHub skill page](https://clawhub.ai/roshanjonah/skills/qubrics-cli)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON examples]

**Output Format:** [Markdown instructions with shell examples and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes credential, account identity, and command-surface guidance.]

## Skill Version(s):

2.0.4 (source: artifact frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
