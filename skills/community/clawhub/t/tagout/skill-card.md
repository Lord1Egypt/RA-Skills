## Description:

Tagout is a local command-line skill for recording, checking, searching, and exporting tagout-related status entries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain1](https://clawhub.ai/user/bytesagain1)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to maintain a local tagout activity log, inspect current status, search or list entries, and export records as JSON or CSV. Its records should be treated as local notes, not authoritative safety compliance evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe shell handling can allow command execution through the config command.

Mitigation: Review before installing, avoid untrusted config keys or values, and fix the config command before using the skill outside a low-risk local environment.

Risk: JSON and CSV serialization are weak for safety-related records.

Mitigation: Do not treat stored or exported data as reliable safety compliance evidence unless serialization and record validation are made safe.

Risk: Destructive and export operations may be unclear for users handling safety-related logs.

Mitigation: Require clear confirmation and review generated exports before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bytesagain1/skills/tagout)
- [BytesAgain homepage](https://bytesagain.com)
- [Publisher profile](https://clawhub.ai/user/bytesagain1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The backing script can create local JSONL data and JSON or CSV exports.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
