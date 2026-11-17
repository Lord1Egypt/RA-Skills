## Description:

Generates a Chinese weekly report from this week's Git commit history, grouping entries by functional module in numbered-list format.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anneheartrecord](https://clawhub.ai/user/anneheartrecord)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to collect weekly Git logs across one or more configured repositories and turn them into a concise Chinese status report organized by functional module.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The configuration file is executed as shell code, which can create local command-execution risk if config.conf is untrusted or maliciously modified.

Mitigation: Review and control config.conf before running the script, and do not use configuration files from untrusted sources.

Risk: Commit messages or file names from shared repositories may affect the generated report text.

Mitigation: Review the generated weekly report before sharing it, and treat repository text as untrusted input.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anneheartrecord/skills/weekly-report-generator-by-git)
- [Publisher profile](https://clawhub.ai/user/anneheartrecord)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-compatible numbered Chinese list with optional nested bullets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The report is derived from local Git history for the configured repositories and author.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
