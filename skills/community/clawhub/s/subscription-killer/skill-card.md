## Description:

Analyse a bank transactions CSV to detect recurring subscriptions, score cancellation priority, and surface actionable savings recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexwong27](https://clawhub.ai/user/alexwong27)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to analyze local bank transaction CSV exports, identify recurring subscriptions, and prioritize cancellation or downgrade opportunities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bank transaction CSVs contain sensitive financial data.

Mitigation: Run the skill locally and share only the resulting recommendations that are necessary for the task.

Risk: Cancellation recommendations may be wrong when CSV exports use unusual refund, credit, or debit sign conventions.

Mitigation: Review detected subscriptions, amounts, and cancellation targets before acting on the report.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alexwong27/skills/subscription-killer)
- [Publisher profile](https://clawhub.ai/user/alexwong27)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Terminal text report with cancellation guidance; the script also documents a JSON output mode for downstream agent use.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Currency display can be configured with SUBSCRIPTION_KILLER_CURRENCY or the --currency argument; minimum confidence can be adjusted with --min-confidence.]

## Skill Version(s):

1.3.0 (source: server release metadata; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
