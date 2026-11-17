## Description:

McKinsey-style business research and analysis skill. This skill should be used when the user needs consulting-grade insights, quantitative data modeling, competitor deep-dive analysis, user persona research, industry trend reports, or structured business problem-solving. Triggers on requests like analyze this market, compare competitors, build a user persona, estimate market size, write a research report, do a SWOT analysis, or any business research task requiring structured frameworks and data-driven conclusions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nannl22](https://clawhub.ai/user/nannl22)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers use this skill to structure business research, competitor analysis, user research, market sizing, quantitative modeling, and executive-ready recommendations. It helps agents turn broad business questions into sourced findings, analysis frameworks, charts, reports, and prioritized action plans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Business analyses may include confidential company data, proprietary exports, or sensitive market research.

Mitigation: Redact sensitive inputs, use approved data handling processes, and avoid sharing confidential data with unapproved external services.

Risk: The skill can rely on outside data services and web searches for enterprise, market, and app data.

Mitigation: Use only approved connectors and sources, record source dates, and verify important data points with independent sources before relying on recommendations.

Risk: Generated reports may include unpinned web chart libraries.

Mitigation: Prefer pinned or local visualization libraries when reports contain sensitive data or need reproducible rendering.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nannl22/skills/research-analysis)
- [Analysis frameworks](references/analysis-frameworks.md)
- [Competitor analysis](references/competitor-analysis.md)
- [Data modeling](references/data-modeling.md)
- [Tool usage](references/tool-usage.md)
- [User research](references/user-research.md)
- [VChart CDN](https://unpkg.com/@visactor/vchart/build/index.min.js)
- [VTable CDN](https://unpkg.com/@visactor/vtable/build/index.min.js)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, structured tables, cited analysis, standalone HTML chart code, and concise implementation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include external data source citations, confidence labels, timelines, and prioritized recommendation tables.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
