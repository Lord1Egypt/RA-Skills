## Description:

System Data Intelligence helps agents work with office and text files, run multi-level data analysis, and produce visual reports across Windows, macOS, and Linux.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaojie911272507](https://clawhub.ai/user/zhaojie911272507)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users can use this skill to guide agents through reading Excel, WPS, Word, text, Markdown, RTZ, CSV, and JSON files, then analyze the data and create reports or dashboards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to apply broad routing rules for file operations, data analysis, and visualization.

Mitigation: Review the skill before installing it, and do not paste AGENTS.md into a system prompt unless that broad routing behavior is intended.

Risk: Desktop automation and document parsing can act on local files and application state.

Mitigation: Use the skill only with files and folders the user explicitly chooses, avoid untrusted macro-enabled Office or WPS documents, and prefer offline parsers for unknown files.

Risk: Generated reports and logs may include original data or sensitive derived information.

Mitigation: Inspect generated output directories and logs before sharing, retaining, or publishing them.

## Reference(s):

- [Windows API Reference](references/windows-api.md)
- [macOS API Reference](references/macos-api.md)
- [Linux API Reference](references/linux-api.md)
- [File Formats Reference](references/file-formats.md)
- [Visualization Patterns Reference](references/viz-patterns.md)
- [Universal Agent Instructions](AGENTS.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with Python and shell code blocks; generated artifacts may include HTML, PNG, JSON, CSV, and logs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may contain source data or sensitive derived information and should be reviewed before sharing.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
