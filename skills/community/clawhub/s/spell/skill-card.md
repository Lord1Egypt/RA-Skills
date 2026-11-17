## Description:

Log anything fast and find it later with search and export. Use when running lookups, checking entries, converting formats, generating summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain1](https://clawhub.ai/user/bytesagain1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use Spell as a local command-line activity logger for saving lookup notes, checking recent entries, searching history, and exporting saved entries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Inputs passed to Spell are persisted on disk under ~/.local/share/spell.

Mitigation: Avoid entering secrets or private data, and review or delete local logs before sharing the machine or exports.

Risk: Several utility-sounding commands mostly create log entries rather than performing the named operation.

Mitigation: Treat command output as local note-taking unless the command visibly returns the expected conversion, analysis, report, or export result.

Risk: Routing bugs may make some intended status or export behavior unreachable.

Mitigation: Run spell help and verify the produced files or terminal output before relying on a command in a workflow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bytesagain1/skills/spell)
- [BytesAgain Homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files, Configuration]

**Output Format:** [Terminal text with local log files and JSON, CSV, or plain text exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores entries locally under ~/.local/share/spell.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
