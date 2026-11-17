## Description:

Guides an agent through a Bazi and Tianxing Mipai fortune-reading workflow, then presents probability-based observations and suggestions in a structured report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[136449689yu-prog](https://clawhub.ai/user/136449689yu-prog)

### License/Terms of Use:

MIT-0

## Use Case:

People seeking a traditional Bazi and Tianxing Mipai reading provide birth date, time, sex, birthplace, and a consultation topic to receive a structured, probability-based interpretation. The reading is folklore and should not replace professional advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs changes to source notes and engine rules, which could alter readings.

Mitigation: Keep the knowledge base read-only during use and review proposed note or engine edits separately.

Risk: The setup depends on PyYAML and external vault and presentation files that are not bundled, despite the offline-use claim.

Mitigation: If offline operation matters, provision PyYAML from an approved offline source and review external files before use.

Risk: Birth details and generated reports can contain sensitive personal information.

Mitigation: Choose a consultation topic intentionally and protect saved birth details and reports.

Risk: Fortune readings are folklore and may be mistaken for reliable professional guidance.

Mitigation: Treat readings as folklore, not medical, legal, or financial advice.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/136449689yu-prog/skills/tianxing-mipai-jilaoshi)
- [Publisher profile](https://clawhub.ai/user/136449689yu-prog)

## Skill Output:

**Output Type(s):** [Text, Markdown, HTML, Guidance]

**Output Format:** [Single-file offline HTML by default; Markdown when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Structured, probability-based observations and suggestions; report content is intended for local use.]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
