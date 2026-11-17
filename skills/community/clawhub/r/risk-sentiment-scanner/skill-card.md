## Description:

Scans public news, announcements, and regulatory information for listed companies and produces structured credit-risk sentiment reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yukirang](https://clawhub.ai/user/yukirang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and business users can use this skill to batch review enterprises for public sentiment and credit-risk signals, then receive company-level ratings, summaries, and recommended review cadence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner can generate low-risk company reports when no source evidence is collected.

Mitigation: Require evidence collection to fail closed, include source URLs and timestamps, and block risk ratings when no sources are found.

Risk: Credit, procurement, investment, or business workflows could over-rely on generated risk scores.

Mitigation: Require human review and professional financial due diligence before using reports for material decisions.

Risk: Reports may be saved or exported outside the chat workflow.

Mitigation: Require explicit approval before saving reports, exporting to Feishu, or enabling scheduled monitoring.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yukirang/skills/risk-sentiment-scanner)
- [ClawHub publisher profile](https://clawhub.ai/user/yukirang)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown, Guidance]

**Output Format:** [Structured JSON report with optional Markdown report output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes company-level risk ratings, risk scores, trend labels, positive and negative factors, red flags, recommended actions, review frequency, source URLs when collected, and high-risk alerts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
