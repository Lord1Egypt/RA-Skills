## Description: <br>
港股日报分析Agent - 每日发送《港股每日动量报告》到飞书 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wuchhao](https://clawhub.ai/user/wuchhao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to draft weekday Hong Kong equity momentum reports for Feishu, including market stance, a five-stock watchlist, probability estimates, and risk notes. The generated report is informational draft analysis and is not investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated stock picks and win probabilities may be mistaken for investment advice. <br>
Mitigation: Present reports as informational draft analysis, retain the included disclaimer, and require human review before trading decisions. <br>
Risk: The skill can post reports to Feishu and may send content to an unintended destination if configured incorrectly. <br>
Mitigation: Confirm the Feishu destination and weekday schedule before enabling automated posting. <br>
Risk: Optional market-data credentials could expose broader account access if reused. <br>
Mitigation: Use a limited-purpose Finnhub API key and rotate or revoke it if the skill configuration changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wuchhao/stock-daily-report-hk) <br>
- [Sina Finance Hong Kong stocks](https://finance.sina.com.cn/stock/hkstock/) <br>
- [Eastmoney Hong Kong stock list](https://quote.eastmoney.com/center/gridlist.html#hk_stocks) <br>
- [AAStocks](https://www.aastocks.com) <br>
- [Futu](https://www.futunn.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown daily market report with headings, bullets, probabilities, and disclaimer text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can use an optional Finnhub API key for US market reference data and can post the generated report to Feishu.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
