## Description:

Record, search, and display quotes and sayings for local command-line workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to operate a local quote-oriented CLI for recording entries, searching logs, checking status, and exporting saved data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented quote features and the command behavior do not fully align.

Mitigation: Validate the actual CLI behavior in a test environment before relying on it for quote analysis, attribution checks, conversion, or generated picks.

Risk: User input is stored persistently in local plaintext logs.

Mitigation: Avoid entering secrets, credentials, private notes, or sensitive business text; restrict file permissions on the storage directory and delete old logs when they are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ckchzh/skills/quote)
- [Publisher profile](https://clawhub.ai/user/ckchzh)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and plain text CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled CLI writes local log and export files under the user's home directory.]

## Skill Version(s):

2.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
