## Description: <br>
Quantitative trading data analysis skill for real-time A-share, US stock, Hong Kong stock, and precious-metals quotes, multi-factor scoring, market anomalies, northbound flows, and intraday capital-flow analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[onlyloveher](https://clawhub.ai/user/onlyloveher) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and market analysts use this skill to fetch current market data and generate structured stock, commodity, anomaly, and capital-flow analysis. Its outputs are analysis aids only and should not be treated as investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound requests to public finance and news providers. <br>
Mitigation: Run it in an environment where those network calls are expected, and review provider access before deployment. <br>
Risk: The skill may write local cache databases. <br>
Mitigation: Configure cache locations deliberately and monitor stored market data according to local data-handling policies. <br>
Risk: Scores and buy/sell labels can be mistaken for investment advice. <br>
Mitigation: Present results as analytical signals only and require human review before financial decisions. <br>
Risk: Python dependencies are not fully pinned to exact versions. <br>
Mitigation: Pin or review dependency versions before installing in a managed or production environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/onlyloveher/trading-quant-zhouli) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON-producing CLI examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses market/news data providers and may write local cache databases.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
