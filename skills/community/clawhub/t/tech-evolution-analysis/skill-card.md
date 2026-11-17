## Description:

A seven-step technology evolution analysis workflow that uses TRIZ evolution paths, SVOP functional abstraction, and PatSnap patent/paper retrieval to analyze product evolution directions, whitespace, cross-domain analogies, 3/5/10-year predictions, gray-rhino signals, and black-swan signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and product strategy teams use this skill to decompose a target product, retrieve patent and paper evidence through PatSnap, map findings to TRIZ routes, and produce technology-evolution forecasts and report artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML reports can turn untrusted case data into executable browser content.

Mitigation: Use the skill in a controlled workspace and sanitize untrusted product names, web snippets, patent text, and third-party JSON before opening generated HTML.

Risk: The workflow may process external patent, paper, web, and account-scoped PatSnap data.

Mitigation: Confirm PatSnap MCP/account access and web-research scope are acceptable before running the analysis, and review outputs before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanzhian-patsnap/skills/tech-evolution-analysis)
- [PatSnap Open Platform](https://open.zhihuiya.com/)
- [Step 1-2 Components and SVOP](references/step1-2-components-svop.md)
- [Step 3 Four-Track Search](references/step3-double-track-search.md)
- [Step 4 Multi-Dimensional Scoring](references/step4-multi-dim-scoring.md)
- [Step 5 TRIZ Labeling](references/step5-triz-labeling.md)
- [Step 6 Evolution Tree](references/step6-evolution-tree.md)
- [Step 7 Prediction Report](references/step7-prediction-report.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON, HTML reports, Guidance]

**Output Format:** [Markdown guidance with structured JSON artifacts, shell commands, and generated HTML reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PatSnap MCP/account access for live patent and paper retrieval; without that configuration it provides the analysis framework only.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
