## Description:

Use when the user wants a claim-safe growth report from validated current evidence, with TrustGrowth score/history when connected and source-specific reporting otherwise.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trustgrowth](https://clawhub.ai/user/trustgrowth)

### License/Terms of Use:

MIT-0

## Use Case:

External-facing growth and SEO teams use this skill to produce claim-safe growth reports from validated current evidence. It reports TrustGrowth score and history when connected, or source-specific measurements from validated imports and connectors otherwise.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to run an unbundled local validator from a discovered skills root before using evidence.

Mitigation: Verify the validator path and trust the installed Groundcrew doctor script before relying on conclusions; avoid passing sensitive evidence records to unknown local scripts.

Risk: Configured connectors and paid API batches can expose credentials, private site data, or costs if used without review.

Mitigation: Use only already configured read-only connectors or explicitly approved paid API batches, and never print API keys.

## Reference(s):

- [Connectors and categories](references/connectors.md)
- [Reporting contract](references/reporting.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report with measurements, changes, actions, evidence, and limitations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses validated current evidence; missing values remain missing.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
