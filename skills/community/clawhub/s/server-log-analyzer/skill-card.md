## Description:

Analyzes server log files to detect problems, extract performance metrics, and provide troubleshooting insights.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chengaojian](https://clawhub.ai/user/chengaojian)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect structured server logs, identify errors and Python exceptions, summarize performance metrics, and produce troubleshooting guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads user-provided log files, which may contain sensitive operational or personal data.

Mitigation: Review log contents before analysis and avoid processing highly sensitive logs unless local handling is acceptable.

Risk: Very large logs may require noticeable local processing time or memory.

Mitigation: Use appropriately scoped log excerpts or review resource usage before running analysis on large files.

## Reference(s):

- [Server Log Analysis Reference](references/log_reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, guidance]

**Output Format:** [Markdown troubleshooting summaries and optional JSON analysis output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can summarize log statistics, exceptions, performance metrics, detected issues, and module frequency from user-provided log files.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
