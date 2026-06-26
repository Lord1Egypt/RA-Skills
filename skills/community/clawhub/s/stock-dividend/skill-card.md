## Description: <br>
Analyze dividend metrics for stocks via AIsa API. Provides yield, payout ratio, growth CAGR, safety score (0-100), income rating, and Dividend Aristocrat/King status. Use when the user asks about dividends, income investing, or dividend safety. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bibaofeng](https://clawhub.ai/user/bibaofeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to request dividend-focused analysis for one or more stock tickers, including yield, payout, growth, safety score, income rating, and dividend aristocrat or king status. The output is informational and should not be treated as investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an AIsa API key and sends requested ticker symbols and prompts to AIsa or a configured custom AISA_BASE_URL. <br>
Mitigation: Use the skill only with an approved AIsa endpoint and provide credentials only in environments where sending those requests is acceptable. <br>
Risk: Dividend analysis may be incorrect, incomplete, stale, or unsuitable for a user's financial situation. <br>
Mitigation: Treat outputs as informational analysis, verify material data independently, and avoid using the result as investment advice. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bibaofeng/stock-dividend) <br>
- [Publisher profile](https://clawhub.ai/user/bibaofeng) <br>
- [AIsa homepage](https://aisa.one) <br>
- [AIsa API endpoint](https://api.aisa.one/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, guidance] <br>
**Output Format:** [Markdown report by default, or structured JSON when invoked with --output json] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ticker symbols as input and sends requests to the configured AIsa API endpoint.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
