## Description:

Rectifier presents as a rectifier circuit design calculator and provides commands for local record status, add, list, search, remove, export, statistics, and configuration workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain3](https://clawhub.ai/user/bytesagain3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers can use this skill to run the bundled CLI for simple local record management tasks described by the artifact, including status checks, adding entries, listing, searching, removal, export, statistics, and configuration. Because the security evidence reports a mismatch with the advertised calculator purpose, users should not rely on it for rectifier circuit design calculations without independent validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is described as a rectifier circuit design calculator, while authoritative security evidence says it stores, deletes, searches, configures, and exports local records.

Mitigation: Treat the skill as a local record manager unless its calculator behavior is separately verified; do not rely on it for electrical design decisions.

Risk: The remove, config, and export commands can change local records, preferences, or generated files.

Mitigation: Review proposed commands before execution, run in a controlled workspace, and back up any records before removal or configuration changes.

Risk: Entries may be exported to CSV, which can be unsafe to open in spreadsheet software when values come from untrusted input.

Mitigation: Sanitize exported values or inspect CSV output in a viewer that does not evaluate formulas.

Risk: Local records may contain sensitive information if users add secrets or private data.

Mitigation: Do not store secrets in entries, and set RECTIFIER_DIR to a scoped non-sensitive directory for testing or review.

## Reference(s):

- [ClawHub Rectifier skill page](https://clawhub.ai/bytesagain3/skills/rectifier)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands; command output is plain text, with JSONL or CSV files when export is used.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses RECTIFIER_DIR when set, otherwise writes local records under ~/.rectifier; export writes rectifier-export.json or rectifier-export.csv in the current working directory.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
