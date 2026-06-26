## Description: <br>
Professional US stock analysis with financial data, news, social sentiment, and multi-model AI. Comprehensive reports at $0.02-0.10 per analysis. Use when: the user needs market data, stock analysis, watchlists, or portfolio workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aisadocs](https://clawhub.ai/user/aisadocs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and analysts use this skill to run US equity research workflows for stock analysis, watchlists, portfolio monitoring, earnings reviews, competitor comparison, and screening. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends stock symbols, portfolio or watchlist context, research queries, fetched source content, and LLM prompts to AIsa. <br>
Mitigation: Use the skill only with data you are comfortable sharing with AIsa, avoid unnecessary sensitive portfolio details, and review organization data-sharing requirements before use. <br>
Risk: The skill requires an AIsa API key and uses paid API calls. <br>
Mitigation: Use a scoped or test AIsa key where possible, store it in the environment, and monitor credit usage during analysis workflows. <br>
Risk: Generated reports are written to disk and include raw collected data. <br>
Mitigation: Choose output paths deliberately, protect generated report files, and remove or redact raw data before sharing. <br>
Risk: Stock-analysis output may be incomplete, stale, or unsuitable as personalized investment advice. <br>
Mitigation: Treat reports as informational research, verify material claims against primary sources, and consult qualified financial professionals before making investment decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aisadocs/us-stock-analyst) <br>
- [AIsa API Reference](https://aisa.mintlify.app/api-reference/introduction) <br>
- [AIsa complete docs](https://aisa.mintlify.app/llms.txt) <br>
- [AIsa website](https://aisa.one) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [Human-readable terminal report and JSON analysis report written to disk] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include investment summary, key metrics, sentiment, valuation, data sources, raw collected data, and an informational-only disclaimer.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
