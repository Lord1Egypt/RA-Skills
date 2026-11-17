## Description:

Analyze bank transactions, categorize spending, track monthly budgets, detect overspending and anomalies. Outputs interactive HTML report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andreolf](https://clawhub.ai/user/andreolf)

### License/Terms of Use:


## Use Case:

External users use this skill to analyze local bank or card transaction exports, categorize spending, compare budgets, detect overspending, and generate monthly financial reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles private financial data and saves local reports that may contain transaction details.

Mitigation: Review report storage, sharing practices, and access controls before use; keep generated files local unless intentionally shared.

Risk: The generated HTML report can contact Google Fonts despite the local-only privacy claim.

Mitigation: Remove external font imports or review network behavior before opening reports with sensitive transaction data.

Risk: The HTML template does not define safe escaping for merchant or transaction text.

Mitigation: Use trusted transaction input or add HTML escaping and a restrictive content security policy before generating reports from untrusted data.

## Reference(s):

- [Watch My Money ClawHub Skill Page](https://clawhub.ai/andreolf/skills/watch-my-money)
- [Budget Templates](references/budget-templates.md)
- [Common Merchant Mappings](references/common-merchants.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and generated local HTML, JSON, and console summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local financial reports and saved state under ~/.watch_my_money/.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
