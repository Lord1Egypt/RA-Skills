## Description:

Terminal Dashboard is a local terminal logging utility for recording data-operation notes, searching recent activity, and exporting locally stored logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain3](https://clawhub.ai/user/bytesagain3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data practitioners can use this skill to guide local command-line journaling of data pipeline, analysis, validation, and export activity. It is best treated as a local logging utility whose entries are stored persistently on disk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports that the release metadata advertises shell-command execution, YAML configuration, visualization, and alerting, while the artifact behaves as a local terminal logging utility.

Mitigation: Review the installed artifact before use and treat it as a local logging and journaling tool unless separate trusted evidence supports the advertised capabilities.

Risk: User-entered operational text is stored persistently in local log files and exports under ~/.local/share/terminal-dashboard.

Mitigation: Do not enter secrets, tokens, credentials, private SQL, PII, or sensitive business data unless local persistence in that directory is acceptable.

## Reference(s):

- [Terminal Dashboard ClawHub Skill Page](https://clawhub.ai/bytesagain3/skills/terminal-dashboard)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and local file output descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe locally persisted logs and exports under ~/.local/share/terminal-dashboard.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
