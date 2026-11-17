## Description:

Provides an end-to-end business strategy analysis workflow for market sizing, competitor analysis, SWOT+, Porter Five Forces, and business model canvas work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vincentlau2046-sudo](https://clawhub.ai/user/vincentlau2046-sudo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to collect market evidence and produce structured business strategy reports with quantitative frameworks, industry templates, citations, and visual outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Business topics, search queries, and context may be sent to Tavily or other external sources.

Mitigation: Use non-confidential topics unless approved, strip sensitive context before searching, and rely on approved data sources.

Risk: User-provided topic text can influence output paths or shell snippets.

Mitigation: Use a sanitized slug for output paths and review generated shell commands before execution.

Risk: Generated reports and API key material may be stored locally.

Mitigation: Keep API keys in a secret manager or owner-only environment file and verify permissions on generated reports.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vincentlau2046-sudo/skills/technical-business-strategy-analysis)
- [Business Model Canvas framework](references/frameworks/business-model-canvas.md)
- [Competitor Matrix framework](references/frameworks/competitor-matrix.md)
- [Porter Five Forces framework](references/frameworks/porter-five-forces.md)
- [SWOT+ framework](references/frameworks/swot-plus.md)
- [TAM/SAM/SOM framework](references/frameworks/tam-sam-som.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, HTML presentations, CSV/JSON data files, and inline shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local report, data, source, and presentation files for each strategy analysis topic.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json; artifact README lists v1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
