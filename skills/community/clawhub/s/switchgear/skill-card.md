## Description:

Switchgear specification manager for JSON and CSV switchgear tasks and status checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain3](https://clawhub.ai/user/bytesagain3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and operators use this skill to manage local switchgear specification records through status, add, list, search, remove, export, stats, and config commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The shell script has input-handling flaws that may lead to command execution or corrupted exports.

Mitigation: Review or fix the shell script before deployment, avoid passing untrusted values to config, and require explicit user direction for remove, export, and config actions.

Risk: CSV exports can carry risk when generated from untrusted entries and opened in spreadsheet software.

Mitigation: Avoid opening exported CSV files from untrusted entries in spreadsheet software, or sanitize entries before export.

## Reference(s):

- [Switchgear ClawHub Skill Page](https://clawhub.ai/bytesagain3/skills/switchgear)
- [BytesAgain Homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files]

**Output Format:** [Markdown guidance with inline shell commands; local CLI output may be plain text, JSONL, or CSV.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses SWITCHGEAR_DIR to choose the local data directory; remove, export, and config actions should be explicitly user-directed.]

## Skill Version(s):

1.0.0 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
