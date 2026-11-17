## Description:

Log Analyzer Dashboard runs a local Streamlit interface for log statistics, duplicate detection, error analysis, and anomaly identification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[godyounger](https://clawhub.ai/user/godyounger)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect local log files, summarize volume and timing patterns, detect duplicate entries, and review error or anomaly signals through a local dashboard.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local dashboard reads files from the log directory selected by the user, which may include sensitive or unrelated logs.

Mitigation: Point the skill only at intended log directories and avoid directories containing secrets or unrelated sensitive files.

Risk: Dependency installation may pull unpinned Streamlit, Pandas, or Plotly versions.

Mitigation: Install in an isolated environment and review or pin dependency versions before deployment.

Risk: Large log sets can take longer to process or increase memory use.

Mitigation: Use the built-in file count limit and narrow file patterns when analyzing large directories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/godyounger/skills/system-log-analyzer)
- [Publisher profile](https://clawhub.ai/user/godyounger)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and a local Streamlit dashboard for interactive analysis.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally against the log directory and file patterns selected by the user.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
