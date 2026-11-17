## Description:

Temporary email helper backed by Vortex for creating disposable addresses, polling for messages, fetching inbox contents, and clearing mailboxes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[techwithanirudh](https://clawhub.ai/user/techwithanirudh)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to create disposable email addresses, poll or fetch temporary inbox messages, and clear temporary mailboxes during signup or testing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Temporary inbox contents are handled by an external mailbox service and may not be appropriate for sensitive or regulated information.

Mitigation: Use disposable addresses only for low-sensitivity signup or testing workflows, and avoid account recovery, secrets, private personal mail, or regulated data.

Risk: The clear command deletes all messages for the selected temporary mailbox.

Mitigation: Confirm the mailbox address before clearing it and fetch any needed messages before deletion.

Risk: Python dependencies are specified with broad version ranges.

Mitigation: Run the skill in an isolated virtual environment or use pinned dependencies in controlled deployments.

## Reference(s):

- [Vortex temporary email service](https://vortex.skyfall.dev)
- [Vortex API endpoint](https://vtx-api.skyfall.dev)
- [ClawHub skill page](https://clawhub.ai/techwithanirudh/skills/temp-mail)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Plain text commands and CLI output, including email address strings and JSON mailbox responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Mailbox polling is timeout-based; clearing a mailbox is destructive for that address.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
