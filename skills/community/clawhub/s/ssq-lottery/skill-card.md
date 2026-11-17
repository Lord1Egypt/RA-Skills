## Description:

查询最新或指定期双色球开奖结果及中奖号码，优先官方数据源，含中奖规则说明和奖池信息。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenchaoqun](https://clawhub.ai/user/chenchaoqun)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to look up China Welfare Lottery Double Color Ball draw results for the latest or a specified issue, compare numbers, and review prize rules. It is informational only and should not be treated as betting advice or authoritative proof of a prize.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Lottery results may be incomplete, stale, or altered in transit because the skill depends on external websites and some official sources use HTTP.

Mitigation: Treat returned numbers as convenience information and verify important results directly against official China Welfare Lottery channels before acting on them.

Risk: Fallback third-party lottery sources may differ from official data or omit context such as prize pool details.

Mitigation: Prefer official sources when available and clearly label third-party results as reference-only.

Risk: The skill can answer lottery-result questions, which may be misread as gambling advice.

Mitigation: Keep responses limited to factual lookup and rules guidance, and avoid prediction, number selection, or purchasing recommendations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenchaoqun/skills/ssq-lottery)
- [Data source configuration](references/data_sources.md)
- [Double Color Ball rules](references/rules.md)
- [China Welfare Lottery draw announcements](http://kaijiang.zhcw.com/zhcw/html/ssq/list.html)
- [China Welfare Lottery official site](http://www.zhcw.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-style text with lottery draw fields and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include issue number, draw date, red balls, blue ball, prize pool, data source, rule summary, and source verification reminders.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
