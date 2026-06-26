## Description: <br>
Three-factor stock analysis combining DCF valuation, Livermore trend trading rules, and VIX market sentiment to generate high-confidence buy signals for US equities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lyflyd](https://clawhub.ai/user/lyflyd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and analysts use this skill to screen US equities with a three-factor framework and generate informational buy, hold, confidence, target, stop-loss, and position-sizing outputs for further review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated buy signals, targets, stop losses, and portfolio percentages could be mistaken for financial advice. <br>
Mitigation: Treat outputs as informational screening results and require independent review or licensed financial advice before acting. <br>
Risk: An FMP API key can be exposed if placed in shared files or logs. <br>
Mitigation: Provide the key through a private environment variable or local-only configuration and avoid committing or sharing secrets. <br>
Risk: Market-data-dependent analysis can be affected by stale, missing, or incorrect source data. <br>
Mitigation: Confirm data freshness and cross-check important signals before using the report in an investment workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lyflyd/us-stock-analyzer) <br>
- [Publisher profile](https://clawhub.ai/user/lyflyd) <br>
- [Project homepage from ClawHub metadata](https://github.com/yourusername/us-stock-analyzer) <br>
- [Three-Factor Analysis Methodology](references/methodology.md) <br>
- [Financial Modeling Prep API](https://financialmodelingprep.com/api/v3) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with optional Python objects and chart files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Analysis can include composite scores, factor scores, buy or hold signals, target prices, stop-loss levels, position sizing guidance, and visual outputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
