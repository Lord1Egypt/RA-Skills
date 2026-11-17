## Description:

Trade Tracker helps an agent analyze local trading CSV files for profit and loss, attribution by stock or period, trading costs, holding periods, strategy tags, comparisons, and ASCII profit distribution charts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cqdev-ai](https://clawhub.ai/user/cqdev-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to review trade records from CSV files, attribute P&L across stocks and time periods, and generate cost, holding-period, strategy, comparison, chart, or JSON reports for post-trade review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local trade CSV files that may contain sensitive financial history.

Mitigation: Use it only on trusted local files and handle generated reports as sensitive financial data.

Risk: The --output option can overwrite files at paths the user can write to.

Mitigation: Choose output paths deliberately and avoid pointing --output at existing important files.

Risk: Reports from untrusted CSV content may be misleading or unsafe to display in a terminal until output sanitization is added.

Mitigation: Prefer trusted CSV sources and review terminal output before relying on the analysis.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Files, Guidance]

**Output Format:** [Terminal text tables and ASCII charts, with optional JSON stdout or JSON file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally on user-provided CSV files; JSON output is written to the path supplied with --output.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
