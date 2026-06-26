## Description: <br>
Analyze bank transactions, categorize spending, track monthly budgets, detect overspending and anomalies, and output an interactive HTML report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andreolf](https://clawhub.ai/user/andreolf) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to analyze local bank or card transaction exports, categorize spending, monitor monthly budgets, and generate private reports with overspending and anomaly alerts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Transaction history, budgets, merchant overrides, and generated reports are saved locally under ~/.watch_my_money/. <br>
Mitigation: Install and use only on systems where local storage of personal financial data is acceptable; protect or delete the state and report files when they are no longer needed. <br>
Risk: Generated reports load Google Fonts even though the skill claims local-only operation and no network calls. <br>
Mitigation: Use offline or system fonts, or block external requests, before processing sensitive financial data in strict local-only environments. <br>
Risk: The report privacy toggle blurs visible amounts and merchants but should not be treated as redaction for sharing. <br>
Mitigation: Do not share generated reports as anonymized artifacts unless sensitive values have been removed from the underlying report content. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/andreolf/watch-my-money) <br>
- [Budget Templates](references/budget-templates.md) <br>
- [Common Merchant Mappings](references/common-merchants.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, plus generated local HTML reports, JSON exports, and console summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists local state and monthly report files under ~/.watch_my_money/.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
