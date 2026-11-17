## Description:

世界杯比赛赛前情报搜集。用户说「A队 vs B队 第X轮」，自动收集 12 维数据（球队背景、赔率、场地、伤病、首发、裁判等），生成一份带来源链接的完整情报报告。不生成卡片。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaojay](https://clawhub.ai/user/xiaojay)

### License/Terms of Use:

MIT-0

## Use Case:

External users ask for a World Cup match such as "A team vs B team, round X" and receive a structured pre-match scouting report. The skill gathers public football background, standings, venue, weather, form, injuries, news, head-to-head history, odds, referee details, predicted lineups, tactical analysis, and a prediction with source links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The report may include public football information that changes quickly, including weather, injuries, lineups, news, odds, and match markets.

Mitigation: Use current sources, include source links, timestamp odds, and treat predictions as provisional until official data is available.

Risk: Betting and odds coverage may be inappropriate for some users or contexts.

Mitigation: Ask for a narrower report or explicitly request no betting or odds coverage when invoking the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiaojay/skills/worldcup-scouting)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis, Guidance]

**Output Format:** [Markdown report in the conversation with tables, source links, timestamps, and disclaimers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Does not create documents, cards, or images.]

## Skill Version(s):

1.2.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
