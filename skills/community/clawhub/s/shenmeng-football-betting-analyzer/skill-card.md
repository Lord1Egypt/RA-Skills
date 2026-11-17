## Description:

足彩分析助手 - 提供足球比赛数据分析、赔率分析、投注建议。支持基本面分析（球队战绩、伤停、对战历史）、赔率面分析（亚盘、欧赔、凯利指数）、投注策略建议。当用户需要分析足球比赛、获取投注建议、查询球队数据时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[shenmeng](https://clawhub.ai/user/shenmeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to request Chinese-language football match analysis, odds interpretation, bankroll-oriented stake sizing, and betting-value summaries. It is intended as decision-support output only and should be reviewed against local laws, current data quality, and the user's risk tolerance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary flags high-impact billing code with a hardcoded payment API key and weak user-control boundaries.

Mitigation: Install only after publisher review, billing-key rotation or removal, and confirmation that any per-call charge is explicit and authorized for the current user.

Risk: The security guidance states that the skill can send a user ID to an external billing service and charge a SkillPay account.

Mitigation: Run in an environment where SkillPay user identifiers and network access are intentionally configured, and disclose the 0.01 USDT per-call billing model before use.

Risk: The security guidance notes Chinese-only betting-related output and local file-write helper risk.

Mitigation: Use the skill only where betting-analysis output is lawful and appropriate, and review generated files or filesystem permissions before allowing persistent writes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shenmeng/skills/shenmeng-football-betting-analyzer)
- [Publisher profile](https://clawhub.ai/user/shenmeng)
- [API-Football](https://www.api-football.com/)
- [API-Football API endpoint](https://v3.football.api-sports.io)
- [Football-Data.org API](https://api.football-data.org/v4)
- [SkillPay billing provider](https://skillpay.me)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Chinese-language text or Markdown reports, with optional JSON files and Python or shell snippets for setup and execution.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May make external football-data and billing service requests when configured; some helper functions can write analysis JSON under the artifact outputs directory.]

## Skill Version(s):

1.3.1 (source: server release metadata; artifact metadata reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
