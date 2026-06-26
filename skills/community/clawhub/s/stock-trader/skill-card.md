## Description: <br>
A股股票交易助手支持 A 股实时股价查询、批量查询、财经新闻、潜力股分析、行业资金流向、龙头股分析、消息面情感分析和激进型模拟交易。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Sunxianzheng](https://clawhub.ai/user/Sunxianzheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query A-share market data, review market and news signals, simulate aggressive trading scenarios, and draft buy/sell strategy guidance. Outputs are informational and should not be treated as investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The alert feature can create recurring QQ bot alerts to a fixed recipient. <br>
Mitigation: Verify and change the recipient before use, confirm the recurring OpenClaw cron job is intended, and know how to remove it. <br>
Risk: Trading analysis and simulated performance may be misleading or stale, especially when live sources are unavailable or mock or fallback data is used. <br>
Mitigation: Treat outputs as informational, verify market data independently, and do not use the skill as the sole basis for investment decisions. <br>


## Reference(s): <br>
- [技术指标参考](references/indicators.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/Sunxianzheng/stock-trader) <br>
- [Sina Finance Stock News](https://finance.sina.com.cn/stock/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance, Configuration] <br>
**Output Format:** [Markdown-style guidance with terminal command examples and plain-text script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update a local JSON simulated trading record and may create a recurring OpenClaw alert when set_alert.py is used.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
