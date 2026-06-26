## Description: <br>
Queries real-time financial market data for A-shares, Hong Kong shares, U.S. stocks, gold, crude oil, VIX, Treasury yields, foreign exchange, and major indices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaoqiang243](https://clawhub.ai/user/xiaoqiang243) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer market quote questions by calling a Python finance lookup tool and returning concise quote summaries. It is intended for supported market symbols and common Chinese or ticker-based finance queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Finance-related queries are sent to Sina Finance and Yahoo Finance. <br>
Mitigation: Install only where that disclosure is acceptable, and narrow trigger phrases if accidental activation would be a problem. <br>
Risk: The Sina Finance lookup in the artifact uses an HTTP quote endpoint. <br>
Mitigation: Prefer HTTPS for the Sina request if the provider supports it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiaoqiang243/realtime-finance) <br>
- [Sina Finance](https://finance.sina.com.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown] <br>
**Output Format:** [Plain text with Markdown emphasis and finance quote lines] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs current quote summaries, price changes, percentages, highs, lows, and volume when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
