## Description:

Track revenue across multiple Stripe accounts with automated daily reports, goal tracking, and anomaly alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[son-of-poseidon](https://clawhub.ai/user/son-of-poseidon)

### License/Terms of Use:

MIT-0

## Use Case:

External business operators and developers use this skill to pull Stripe revenue, refund, subscription, MRR, ARR, goal, and anomaly summaries across multiple accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads a Stripe secret key and uses it to retrieve financial and subscription data.

Mitigation: Use a restricted read-only Stripe key when possible and store the key with tight local file permissions.

Risk: Automated or broad invocation can expose sensitive revenue data during ordinary revenue discussions.

Mitigation: Narrow the skill trigger conditions and review automated nightly runs before sharing or storing their output.

Risk: Running the skill on shared or heavily monitored machines can leak credentials or revenue details.

Mitigation: Run it only in trusted environments with appropriate access controls and local monitoring expectations.

## Reference(s):

- [Configuration template](references/config-template.json)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON, Markdown reports, brief text summaries, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include financial totals, refund rates, transaction counts, growth comparisons, MRR, ARR, goal progress, and anomaly flags.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
