## Description:

Stock Deep Report generates printable single-page HTML stock analysis reports for A-share, Hong Kong, and U.S. stocks across fundamentals, news, capital flows, technical indicators, valuation, peer comparison, and ownership structure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[songxf1024](https://clawhub.ai/user/songxf1024)

### License/Terms of Use:

MIT-0

## Use Case:

External users and market analysts use this skill to collect public market and news data for a named stock or ticker and generate a visual deep-dive HTML report for review, printing, or sharing. The report may include investment-oriented analysis and should be reviewed before use as financial guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML reports may include untrusted market or news text, which the security evidence identifies as a browser-script injection risk if fields are not escaped.

Mitigation: Review generated reports before opening or sharing them, avoid placing private notes in report data, and confirm externally sourced fields are escaped by the renderer.

Risk: The security verdict is suspicious despite no evidence of theft, backdoors, or destructive behavior.

Mitigation: Review the skill before installing or deploying it and limit use to the declared workspace file access and allowlisted public data sources.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/songxf1024/skills/stock-deep-report)
- [Publisher Profile](https://clawhub.ai/user/songxf1024)
- [Stock Data JSON Template](artifact/references/json_template.md)
- [HTML Report Renderer](artifact/references/build.py)
- [Eastmoney Quote Page Template](https://quote.eastmoney.com/{market}{code}.html)
- [Eastmoney F10 Data Page Template](https://emweb.securities.eastmoney.com/pc_hsf10/pages/index.html?type=web&code={market}{code})

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, HTML files]

**Output Format:** [Structured JSON input and a printable single-page HTML report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes stock_data.json and a stock deep-analysis HTML report in the current workspace.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
