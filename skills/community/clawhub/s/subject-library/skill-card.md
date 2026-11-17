## Description:

Use when a user asks about China A-share market themes, subject analysis, stock-theme relationships, theme heat rankings, or investment insight based on iTougu Theme Library data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qingyixiaoyao](https://clawhub.ai/user/qingyixiaoyao)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to browse China A-share market themes, inspect single-theme details, compare themes, look up stock-theme relationships, and generate structured market-theme analysis reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may suggest installing additional tooling or packages.

Mitigation: Review installation instructions before running them and prefer pinned ClawHub and Python package versions.

Risk: Market quotes may come from public unauthenticated endpoints, including an HTTP Tencent quote endpoint.

Mitigation: Treat quote data as unverified, cross-check important values against trusted sources, and preserve source attribution in outputs.

Risk: Generated market analysis may be mistaken for investment advice.

Mitigation: Keep informational-purpose disclaimers, label AI predictions clearly, and avoid explicit buy or sell recommendations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qingyixiaoyao/skills/subject-library)
- [iTougu Theme Library API](https://group-api.itougu.com)
- [Theme list endpoint](https://group-api.itougu.com/teach-hotspot/subject/fullList)
- [Theme detail endpoint](https://group-api.itougu.com/teach-hotspot/subject/subjectDetail4Free)
- [East Money quote API](https://push2.eastmoney.com/api/qt/ulist.np/get)
- [AKShare](https://github.com/akfamily/akshare)
- [API reference](artifact/api-reference.md)
- [Analysis templates](artifact/analysis-templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Structured Markdown reports with tables, source attribution, code snippets, and risk disclaimers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should identify data sources, avoid unsupported market claims, and state when data is insufficient.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
