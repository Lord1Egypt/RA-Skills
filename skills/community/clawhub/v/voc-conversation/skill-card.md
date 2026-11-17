## Description:

Analyzes batches of Chinese customer-service conversation exports to produce a VOC insight report with topic distribution, sentiment, frequent issues, redacted customer quotes, churn-risk signals, and prioritized improvement recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zenobiazizi](https://clawhub.ai/user/zenobiazizi)

### License/Terms of Use:

MIT-0

## Use Case:

Operations, product, and customer-service teams use this skill to turn authorized Chinese support conversation exports into a single decision-oriented VOC snapshot. It helps identify what customers ask about, where negative sentiment concentrates, which issues recur most often, and which improvements should be prioritized.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Customer conversation exports may contain personal, order, address, or account data.

Mitigation: Use only conversation data the user is authorized to analyze, keep processing local where possible, and review report quotes for complete redaction before sharing.

Risk: The VOC report is a single-batch snapshot and may not represent broader customer behavior.

Mitigation: Treat findings as decision support, validate important decisions with additional data, and disclose sampling or excluded-file counts in the report.

Risk: The skill is designed for Chinese customer-service conversations, so non-Chinese datasets may produce weaker classifications.

Mitigation: Warn users when the dataset is primarily non-Chinese and ask whether to continue or adjust the analysis approach.

Risk: The release includes visible customization and paid-service contact language.

Mitigation: Review public-facing output for acceptable marketplace language before distribution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zenobiazizi/skills/voc-conversation)
- [Default topic taxonomy](references/topics-default.md)
- [Sample VOC report](examples/sample-report.md)

## Skill Output:

**Output Type(s):** [markdown, analysis, guidance]

**Output Format:** [Markdown report, with optional Excel report when the runtime supports file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes aggregated metrics, redacted representative quotes, risk signals, prioritized recommendations, and a note that conclusions are based on a single batch of conversations.]

## Skill Version(s):

1.0.0 (source: server release metadata and README version section)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
