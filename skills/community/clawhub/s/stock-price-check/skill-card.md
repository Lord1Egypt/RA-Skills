## Description:

Query current A/HK/US-share stock prices using natural language stock names.

This skill is ready for commercial/non-commercial use.

## Publisher:

[silverfoxchina-gif](https://clawhub.ai/user/silverfoxchina-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to look up A-share, Hong Kong, and U.S. stock quote data from natural language stock names or stock codes. It is intended for informational quote lookup, not financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The entered stock name or code is sent to public finance lookup services.

Mitigation: Use the skill only for intended public quote lookups and avoid submitting private or sensitive identifiers.

Risk: Returned quote data can be incomplete, delayed, or unsuitable for investment decisions.

Mitigation: Treat results as informational market data and verify against authoritative sources before making financial decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/silverfoxchina-gif/skills/stock-price-check)
- [Sina Finance](https://finance.sina.com.cn)
- [Eastmoney suggest API](https://searchapi.eastmoney.com/api/suggest/get?input={stock_name}&type=14&count=5)
- [Sina Finance quote endpoint](https://hq.sinajs.cn/list={sina_code})

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Chinese-formatted plain text stock quote fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires outbound HTTP access to public finance services; no credentials detected.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
