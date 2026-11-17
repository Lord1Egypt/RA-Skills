## Description:

Use this skill when a finance analyst, controller, or CFO needs to produce a budget-vs-actual variance analysis report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[archlab-space](https://clawhub.ai/user/archlab-space)

### License/Terms of Use:

MIT-0

## Use Case:

Finance analysts, controllers, CFOs, and management-reporting teams use this skill to turn actuals-vs-budget, forecast, or prior-year financial data into a management-ready variance analysis report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may provide sensitive financial data during variance analysis.

Mitigation: Share only the financial detail needed for the report and avoid unnecessary confidential information in the agent session.

Risk: A variance narrative may become misleading if the cause is unknown or unsupported.

Mitigation: Use the skill's requirement to flag unknown drivers for investigation instead of inventing root causes.

Risk: Incorrect figures or favorable/unfavorable labels could affect management decisions.

Mitigation: Review the normalized table, arithmetic flags, F/U labels, and final narrative for consistency before using the report.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report with tables and narrative sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes an executive summary, variance summary table, per-line variance narratives, recommendations table, and notes.]

## Skill Version(s):

0.1.2 (source: server release metadata and changelog, released 2026-05-28)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
