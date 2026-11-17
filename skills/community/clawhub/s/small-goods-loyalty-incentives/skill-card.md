## Description:

Designs and refines customer loyalty programs and incentive systems for DTC and independent stores selling small, high-frequency products.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rijoyai](https://clawhub.ai/user/rijoyai)

### License/Terms of Use:

MIT-0

## Use Case:

External DTC and independent-store teams use this skill to design points, tiers, rewards, referral, win-back, and lifecycle incentives for small, high-frequency products. It helps agents produce structured program designs, incentive calendars, margin guardrails, and measurable validation plans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Loyalty, email, SMS, birthday, referral, and win-back campaigns can require consent, unsubscribe, privacy, and regional compliance checks.

Mitigation: Treat skill output as planning guidance and review every campaign against the store's consent, unsubscribe, privacy, and legal requirements before launch.

Risk: Helper scripts that accept an output path can overwrite the selected file.

Mitigation: Run helper scripts in a working copy or write to a new output path, then review the generated markdown before replacing operational files.

## Reference(s):

- [Small Goods Loyalty Incentives on ClawHub](https://clawhub.ai/rijoyai/skills/small-goods-loyalty-incentives)
- [Loyalty Framework](references/loyalty_framework.md)
- [Incentive Playbook](references/incentive_playbook.md)
- [Loyalty and Incentive Metrics](references/metrics.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with tables, JSON configuration examples, Python helper scripts, and shell command snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Helper scripts can generate markdown reports or incentive calendars when run with an output path.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
