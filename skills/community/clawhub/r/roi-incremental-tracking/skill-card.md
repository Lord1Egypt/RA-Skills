## Description:

Track your AI agent's ROI incrementally - log time saved and direct cash as deliveries happen, then close the cycle monthly with an HTML dashboard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thiagocaltoe](https://clawhub.ai/user/thiagocaltoe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and teams use this skill to track incremental value from agent-assisted work. It guides first-run ROI setup, ongoing ledger entries, monthly closeout, and dashboard reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ROI data may include business-sensitive costs, hourly rates, cash amounts, evidence links, and notes.

Mitigation: Treat <workspace>/reports/roi/ as business-sensitive and review ledger entries before sharing reports.

Risk: Dashboard generation may fail because the referenced dashboard script is missing from this artifact.

Mitigation: Confirm render_roi_report.py is present before running monthly closeout or provide the script separately.

## Reference(s):

- [Source repository](https://github.com/ThiagoCAltoe/roi-incremental-tracking)
- [ClawHub skill page](https://clawhub.ai/thiagocaltoe/skills/roi-incremental-tracking)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON and CSV schemas, shell commands, and generated workspace files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes ROI configuration, ledger, summary, dashboard script, and static dashboard files under <workspace>/reports/roi/.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
