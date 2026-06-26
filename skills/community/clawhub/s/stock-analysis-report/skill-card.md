## Description: <br>
Provides multi-dimensional A-share stock and market analysis covering fundamentals, valuation, capital flow, technical indicators, chip distribution, news, scoring, and action-oriented recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[derrors](https://clawhub.ai/user/derrors) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to generate structured A-share individual stock analyses or daily market reviews from stock codes and configured market, news, and LLM providers. The output supports research workflows but should be reviewed as informational analysis, not investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stock queries, retrieved news content, and analysis prompts may be sent to the configured LLM and enabled search or market data providers. <br>
Mitigation: Use dedicated API keys, avoid confidential research terms, and configure only providers approved for the intended workflow. <br>
Risk: Market data, news, and model-generated recommendations may be incomplete, stale, or misleading for trading decisions. <br>
Mitigation: Treat outputs as reference analysis only, review the report before acting, and verify important findings against trusted financial sources. <br>
Risk: The skill depends on external Python packages and live provider APIs. <br>
Mitigation: Use a locked dependency environment for production and monitor provider availability, rate limits, and API-key handling. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/derrors/stock-analysis-report) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/derrors) <br>
- [Miaoxiang financial data API key page](https://dl.dfcfs.com/m/itc4) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, guidance] <br>
**Output Format:** [Structured JSON analysis and optional Markdown reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save reports to a caller-selected directory when save=true; includes risk alerts and a disclaimer that results are for reference only and are not investment advice.] <br>

## Skill Version(s): <br>
1.0.9 (source: frontmatter, manifest, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
