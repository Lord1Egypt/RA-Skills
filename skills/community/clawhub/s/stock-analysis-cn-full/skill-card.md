## Description: <br>
A Chinese-language agent skill for A-share, Hong Kong stock, US stock, and ETF analysis that gathers market data, checks sources, scores signals, and returns trading-oriented analysis with source labels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lin838465-ux](https://clawhub.ai/user/lin838465-ux) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to request Chinese-language stock or ETF analysis by ticker or name, including basic information, technical indicators, fund-flow signals, news checks, scoring, and operation suggestions. It is intended for informational analysis and not personalized financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stock symbols, company names, and related queries may be sent to external market-data or search providers. <br>
Mitigation: Use the skill only when that disclosure is acceptable, and do not include confidential holdings, account data, or unrelated private information in prompts or the local knowledge folder. <br>
Risk: The skill can produce trading-oriented buy, sell, hold, stop-loss, or take-profit guidance that may be incorrect or unsuitable for an individual user. <br>
Mitigation: Treat outputs as informational analysis, verify cited market data independently, and do not rely on the skill as personalized financial advice. <br>
Risk: The skill reads from ~/Desktop/股票知识库/ and may use TUSHARE_TOKEN for Tushare data access. <br>
Mitigation: Keep the local knowledge folder free of secrets or unrelated private material, and set TUSHARE_TOKEN only when Tushare access is intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lin838465-ux/stock-analysis-cn-full) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown-style Chinese-language analysis with data-check sections, source citations, conclusion boxes, and optional Python snippets for data retrieval.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include buy, sell, hold, stop-loss, and take-profit guidance; the artifact requires unavailable or unverified data to be labeled as incomplete.] <br>

## Skill Version(s): <br>
4.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
