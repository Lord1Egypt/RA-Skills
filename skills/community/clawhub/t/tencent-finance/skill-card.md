## Description: <br>
腾讯财经实时行情接口，查询A股、港股、美股、期货、外汇、ETF的实时行情数据。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ezio-xiang](https://clawhub.ai/user/ezio-xiang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to look up Tencent Finance market symbols and retrieve real-time quote fields for equities, indexes, commodities, foreign exchange, and ETFs. It supports interactive quote checks and simple automated quote snapshots. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requested symbols and request metadata are sent to Tencent's public quote endpoint. <br>
Mitigation: Do not include secrets, private portfolio notes, or other sensitive context in query codes. <br>
Risk: High-frequency polling may trigger endpoint throttling or IP blocking. <br>
Mitigation: Use rate limiting and keep requests at least 100 ms apart as documented by the artifact. <br>
Risk: Market quote data can be incomplete, delayed, or unsuitable for investment decisions. <br>
Mitigation: Treat returned data as informational and verify it with authoritative market data before acting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ezio-xiang/tencent-finance) <br>
- [Tencent Finance quote endpoint](https://qt.gtimg.cn/q=) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with Python examples and plain-text quote output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs market quote fields for requested symbols; returned data should be treated as informational.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
