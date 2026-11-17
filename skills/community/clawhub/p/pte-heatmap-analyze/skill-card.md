## Description:

Ptengine Heatmap Analyze fetches Ptengine heatmap data through ptengine-cli and produces CRO behavior analysis using a four-stage psychology model.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaichen](https://clawhub.ai/user/zhaichen)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing practitioners, CRO specialists, and site operators use this skill to analyze Ptengine heatmap data for page behavior, conversion barriers, segment comparisons, A/B tests, ad performance, and audience characteristics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install external CLI software before analysis.

Mitigation: Review before installing, approve installation explicitly, and use the local install.sh wrapper.

Risk: One reference recommends a remote installer command that pipes downloaded code directly to a shell.

Mitigation: Use the local install.sh wrapper instead of the pipe-to-shell command.

Risk: Ptengine credentials and analytics queries may expose sensitive site analytics.

Mitigation: Provide credentials only through a secure secret-handling path and expect queries for the URLs and date ranges supplied.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhaichen/skills/pte-heatmap-analyze)
- [ptengine-cli Command Reference](references/ptengine-cli.md)
- [Data Transformation Reference](references/data-transform.md)
- [Page Classification](references/page-classification.md)
- [Block Content Analysis and Stage Classification](references/block-analysis.md)
- [Quality Constraints](references/quality-constraints.md)
- [Single Page Analysis](references/single-page-task.md)
- [Segment Comparison Analysis](references/compare-task.md)
- [A/B Test Analysis](references/ab-test-task.md)
- [Ad Performance Analysis](references/ad-performance.md)
- [Audience Analysis](references/audience-analysis.md)
- [Page Type Interpretation Guide](references/page-types.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Human-readable Markdown reports with shell command snippets and structured analysis sections.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Ptengine CLI data as the authoritative source and supports single-page, segment comparison, A/B test, ad performance, and audience analysis reports.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
