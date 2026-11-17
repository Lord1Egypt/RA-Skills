## Description:

SASAC Performance Analyst helps agents benchmark enterprise financial performance against SASAC 2025 standard values, diagnose profitability, operations, risk, and growth dimensions, and generate improvement recommendations and reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yjkj999999](https://clawhub.ai/user/yjkj999999)

### License/Terms of Use:

MIT

## Use Case:

Finance, strategy, and enterprise performance teams use this skill to compare company metrics with SASAC 2025 benchmarks, identify performance gaps, and draft management recommendations. Agents can also produce local charts, text summaries, and HTML reports from supplied financial inputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner reports unsupported authority claims and cautions against relying on the skill for financial decisions without review.

Mitigation: Review publisher identity and source claims, compare material benchmark outputs with official publications, and treat recommendations as analytical support rather than final financial advice.

Risk: The scanner notes sensitive financial report handling with weak safeguards.

Mitigation: Use only financial data the user is authorized to process, prefer redacted or aggregate inputs, and avoid storing confidential report outputs in shared paths.

Risk: Generated HTML reports may contain untrusted user-supplied text before the escaping issue is fixed.

Mitigation: Choose explicit local output paths and avoid opening or sharing generated HTML reports that include untrusted inputs until the report escaping issue is remediated.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yjkj999999/skills/sasac-performance-analyst)
- [ClawDIS Homepage](https://github.com/yjkj999999/sasac-performance-analyst#readme)
- [README](artifact/README.md)
- [Skill Definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown or plain text analysis with optional generated local chart and report files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local HTML, text, or image report artifacts when the user requests report generation.]

## Skill Version(s):

2.0.0 (source: SKILL.md frontmatter, package.json, and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
