## Description: <br>
Queries stock prices, quote details, and major market indexes for A-shares, Hong Kong stocks, and US stocks, with support for batch lookups of up to 20 symbols. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tjefferson](https://clawhub.ai/user/tjefferson) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to retrieve current or delayed stock quote data for supported China A-share, Hong Kong, and US securities. It is intended for quick price checks, market index lookups, and small batch comparisons in conversational workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requested ticker symbols are sent to Tencent Finance. <br>
Mitigation: Use only in environments where outbound access to qt.gtimg.cn is approved, and avoid queries that reveal sensitive watchlists or unreleased trading context. <br>
Risk: Hong Kong and US quotes from the free public interface may be delayed by about 15 minutes. <br>
Mitigation: Treat results as informational quote checks and use licensed real-time market data channels when real-time Level-1 data is required. <br>
Risk: The public quote endpoint can fail, rate limit, or return unavailable data. <br>
Mitigation: Surface script errors to the user, retry later for transient failures, and avoid depending on the skill for time-critical trading decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/tjefferson/stock-price-query) <br>
- [Tencent Finance API Reference](artifact/references/api-docs.md) <br>
- [Tencent Finance Quote Endpoint](https://qt.gtimg.cn/q={symbol}) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [JSON from the query script, typically summarized by the agent as concise Markdown or text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports single-symbol and comma-separated batch queries; batch mode is limited to 20 stock symbols.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
