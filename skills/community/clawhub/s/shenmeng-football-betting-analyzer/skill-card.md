## Description: <br>
足彩分析助手 - 提供足球比赛数据分析、赔率分析、投注建议。支持基本面分析（球队战绩、伤停、对战历史）、赔率面分析（亚盘、欧赔、凯利指数）、投注策略建议。当用户需要分析足球比赛、获取投注建议、查询球队数据时使用。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shenmeng](https://clawhub.ai/user/shenmeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to analyze football match fundamentals, odds, historical form, and staking considerations before comparing possible betting outcomes. The skill produces decision-support analysis and risk notes, not guaranteed predictions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes SkillPay billing behavior that can send a SkillPay user ID to skillpay.me and attempt a 0.01 USDT charge. <br>
Mitigation: Install only when paid SkillPay billing is expected, verify the publisher and billing service, and review the payment helper before use. <br>
Risk: Football betting analysis can influence wagering decisions and may be subject to local legal restrictions. <br>
Mitigation: Treat the output as data analysis rather than financial or betting advice, apply independent judgment, and follow applicable local laws. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shenmeng/shenmeng-football-betting-analyzer) <br>
- [Publisher profile](https://clawhub.ai/user/shenmeng) <br>
- [API-Football](https://www.api-football.com/) <br>
- [API-Football endpoint](https://v3.football.api-sports.io) <br>
- [Football-Data.org API](https://api.football-data.org/v4) <br>
- [SkillPay billing provider](https://skillpay.me) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with Python examples, shell commands, configuration notes, and betting-analysis guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require FOOTBALL_API_KEY for live football data and SKILLPAY_USER_ID for paid SkillPay billing.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
