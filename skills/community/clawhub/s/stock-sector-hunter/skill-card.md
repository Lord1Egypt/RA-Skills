## Description:

Stock Sector Hunter helps an agent search for active A-share sectors and leading stocks in the Shanghai and Shenzhen markets, with optional filtering by stock-code prefix or sector keyword.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wenhulove333](https://clawhub.ai/user/wenhulove333)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent for current Chinese A-share sector momentum summaries, leading-stock lists, and simple moving-average screens. Outputs are for informational screening only and should not be treated as investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The authoritative security scan marks the release suspicious because the package ships mismatched financial-analysis scripts and unsafe command, file, and network patterns.

Mitigation: Review the shipped scripts before installation, confirm that each script is expected for the release, and run the skill only in an environment where shell, file, and network access are constrained.

Risk: The sector-search behavior is not clearly separated from extra moving-average screeners.

Mitigation: Document every shipped script and remove or isolate scripts that are not needed for the sector-hunter workflow before routine use.

Risk: The security guidance calls out shell=True, fixed /tmp output, and unauthenticated HTTP market-data sources.

Mitigation: Replace shell execution with argument-list subprocess calls, avoid fixed temporary output paths, and use authenticated HTTPS market-data sources where possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wenhulove333/skills/stock-sector-hunter)
- [Eastmoney stock kline endpoint used by shipped script](http://push2his.eastmoney.com/api/qt/stock/kline/get)
- [Eastmoney stock list endpoint used by shipped script](http://push2.eastmoney.com/api/qt/clist/get)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown-style Chinese text with grouped sector and stock lists, plus optional command output from Python scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May depend on live web search, WEB_SEARCH_API_KEY configuration, and external market-data availability.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
