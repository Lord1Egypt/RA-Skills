## Description:

多币种记录旅行消费、汇率自动换算、分类统计与预算管理，旅行花钱心里有数。

This skill is ready for commercial/non-commercial use.

## Publisher:

[travel-skills](https://clawhub.ai/user/travel-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Travelers and agents use this skill to record trip expenses in multiple currencies, summarize spending by category, date, or currency, and check spending against trip budgets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores trip expense data in local JSON files.

Mitigation: Use it only where local-file storage is acceptable and avoid entering sensitive financial details beyond what is needed for trip tracking.

Risk: Exchange rates are fixed reference values, not live market rates.

Mitigation: Treat converted totals as planning estimates and verify exchange rates before making financial decisions.

Risk: The short description mentions AA splitting, but the security guidance says shared splitting should not be expected.

Mitigation: Use the skill for single-trip expense tracking and budget checks, not as a shared settlement system.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/travel-skills/skills/travel-expense-tracker)
- [ClawHub publisher profile](https://clawhub.ai/user/travel-skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Natural-language responses based on JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local JSON files for expense data and fixed reference exchange rates.]

## Skill Version(s):

1.0.19 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
