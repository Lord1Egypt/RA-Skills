## Description:

Access your Readwise highlights and Reader documents from the command line.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tristanh](https://clawhub.ai/user/tristanh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to operate the Readwise CLI for searching, reading, saving, organizing, exporting, and managing Reader documents and Readwise highlights.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to handle a raw Readwise access token.

Mitigation: Prefer authenticating outside the agent or with a safer secret-entry method, and avoid putting tokens in chat or command history.

Risk: The setup guidance installs an unpinned global npm CLI.

Mitigation: Consider using a pinned or local CLI install before enabling the skill.

Risk: The skill includes account-changing commands for export, bulk edit, move, tag, update, and delete actions.

Mitigation: Confirm destructive or bulk account changes with the user before running them.

Risk: Using the CLI can give broad access to the user's Readwise and Reader account.

Mitigation: Review the skill before installing and use it only when broad account access is acceptable.

## Reference(s):

- [ClawHub Readwise Official skill page](https://clawhub.ai/tristanh/skills/readwise-official)
- [Readwise access token page](https://readwise.io/access_token)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Readwise CLI commands and optional JSON command output when --json is used.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
