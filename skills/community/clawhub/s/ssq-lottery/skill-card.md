## Description: <br>
查询中国福利彩票双色球开奖结果，支持多数据源自动切换并优先使用官方渠道。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenchaoqun](https://clawhub.ai/user/chenchaoqun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to look up the latest or specified China Welfare Lottery Double Color Ball draw results, verify numbers, and review prize rules. It is an information lookup helper and does not provide lottery predictions or buying advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Lottery results can be stale, unavailable, or parsed incorrectly when public websites change structure or block requests. <br>
Mitigation: Verify prize, payout, and ticket decisions on the official China Welfare Lottery site before relying on results. <br>
Risk: Fallback data may come from third-party lottery sites rather than official sources. <br>
Mitigation: Prefer official China Welfare Lottery data and label third-party results as reference-only. <br>
Risk: The skill discusses lottery rules and results, which users may mistake for betting or financial advice. <br>
Mitigation: Keep responses limited to factual lookup and rules guidance, and avoid predictions, number recommendations, or purchase encouragement. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/chenchaoqun/ssq-lottery) <br>
- [双色球数据源配置](references/data_sources.md) <br>
- [双色球游戏规则详解](references/rules.md) <br>
- [中国福彩网](http://www.zhcw.com) <br>
- [中国福彩网开奖公告](http://kaijiang.zhcw.com/zhcw/html/ssq/list.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown text with lottery draw fields, source notes, prize-rule guidance, and optional shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May contact public lottery websites and may fall back from official sources to third-party sources when official pages are unavailable.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
