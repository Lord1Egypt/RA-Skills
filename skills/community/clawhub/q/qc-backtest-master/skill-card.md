## Description:

Automates QuantConnect backtest submission, compilation, monitoring with optional early-stop, and result download from local strategy files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tltby12341](https://clawhub.ai/user/tltby12341)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and quantitative researchers use this skill to run QuantConnect backtests from local strategy files, monitor progress, stop runs that breach drawdown thresholds, and retrieve JSON/CSV results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill has QuantConnect project mutation authority and uploads local strategy content to a cloud project.

Mitigation: Run it only against the intended QuantConnect project, review the strategy file before submission, and confirm QC_PROJECT_ID before execution.

Risk: Auxiliary .json, .txt, and .csv files in the strategy directory may be uploaded along with the main file.

Mitigation: Place strategy files in a clean directory and remove unrelated data files before running the submission or full workflow.

Risk: Credentials may be read from environment variables, a parent .env file, or ~/.lean/credentials.

Mitigation: Set QC_USER_ID, QC_API_TOKEN, and QC_PROJECT_ID explicitly for the intended account and check for fallback credential files before use.

Risk: Early-stop behavior can permanently delete a backtest when the drawdown threshold is exceeded.

Mitigation: Use conservative thresholds, omit --max-dd when result retention matters, and treat deleted early-stop runs as unrecoverable.

## Reference(s):

- [QuantConnect REST API v2](https://www.quantconnect.com/api/v2)
- [ClawHub skill page](https://clawhub.ai/tltby12341/skills/qc-backtest-master)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands; generated artifacts may include JSON result files and CSV order files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires QC_USER_ID, QC_API_TOKEN, QC_PROJECT_ID, python3, and requests; may mutate QuantConnect project files and delete early-stopped backtests.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
