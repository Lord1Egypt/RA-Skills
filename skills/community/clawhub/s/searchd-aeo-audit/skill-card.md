## Description:

Measure how often a company is named in answer-engine research, which competitors appear instead, and which sites shape the answers. Use when a user provides a company domain and asks about AEO, GEO, AI visibility, answer-engine exposure, competitor mentions, cited sources, or an HTML visibility report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[searchd](https://clawhub.ai/user/searchd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, marketers, and growth teams use this skill to run an evidence-first answer-engine visibility audit for a company domain. It helps them create neutral buyer questions, measure named-rate exposure, record competitor mentions and cited sources, and render a self-contained HTML report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports include SearchD attribution and may include a disclosed SearchD service recommendation.

Mitigation: Install only if SearchD-branded reports are acceptable; for neutral or client-facing work, avoid `--agency-cta` unless explicitly wanted and review generated reports before sharing.

Risk: Answer-engine visibility measurements can be mistaken for consumer-app impressions, traffic, market share, or guaranteed responses from specific AI products.

Mitigation: Keep the measurement boundary in the report, disclose the actual agent and search method used, and treat one run per question as directional discovery unless repeated with a fixed panel.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/searchd/skills/searchd-aeo-audit)
- [SearchD homepage](https://searchd.ai/)
- [Audit data contract](references/data-contract.md)
- [Searchd AEO audit methodology](references/methodology.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with JSON audit records, shell commands, and a self-contained HTML report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3.10 or newer for deterministic report rendering; generated reports preserve measured questions, run-level evidence, URLs, and embedded audit JSON.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
