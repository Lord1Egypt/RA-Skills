## Description: <br>
Variance Analyst helps finance analysts, controllers, and CFOs collect budget-versus-actual data, rank material variances, identify root causes, and produce management-ready variance analysis reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[archlab-space](https://clawhub.ai/user/archlab-space) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Finance analysts, controllers, and CFOs use this skill for month-end or quarter-end management reporting, board or CFO presentation preparation, and rapid budget-versus-actual, forecast, or prior-year variance explanations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Confidential financial data may be included in the user's variance inputs. <br>
Mitigation: Use the skill only in sessions where that financial data is appropriate to share, and avoid external searches or tool calls with confidential inputs. <br>
Risk: Variance explanations can be misleading if root causes are guessed or source numbers are inconsistent. <br>
Mitigation: Require period, audience, variance basis, and financial data before analysis; flag arithmetic discrepancies and unknown drivers for investigation instead of inventing causes. <br>
Risk: Default currency or materiality settings may not match the reporting context. <br>
Mitigation: Specify currency and materiality thresholds when USD or the default $10K or 5% threshold is not suitable. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/archlab-space/variance-analyst) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown variance analysis report with an executive summary, variance summary table, variance narratives, recommendations table, and notes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided reporting period, audience, variance basis, and financial line-item data; defaults to USD and a $10K or 5% materiality threshold unless specified.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence and changelog, released 2026-05-28) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
