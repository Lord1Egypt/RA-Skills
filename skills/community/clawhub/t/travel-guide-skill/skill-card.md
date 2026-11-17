## Description:

智能旅行攻略生成器。当用户想要制定旅行计划、询问旅游攻略、需要行程安排时使用。根据目的地、日期、人员、预算等信息，通过实时网络查询生成包含机票酒店、游玩计划、交通、美食、天气的完整攻略。所有价格、时间等关键信息必须来自网络查询并标注来源。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wendyhufh](https://clawhub.ai/user/wendyhufh)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to create Chinese-language travel plans from destination, dates, group type, budget, and preferences. It gathers missing trip details, requires live lookup for prices and schedules, and produces itinerary, transportation, lodging, food, weather, and budget guidance with source labels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated prices, schedules, visa notes, and availability may be outdated or unsuitable for booking decisions.

Mitigation: Verify important bookings and policy details directly with official or booking sources before spending money.

Risk: Travel guide outputs may mix estimates with live data if source lookup is incomplete.

Mitigation: Require source and query-time labels for factual travel data, clearly mark estimates, and tell users when live lookup fails.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wendyhufh/skills/travel-guide-skill)
- [Guide template](references/guide-template.md)
- [Budget template](references/budget-template.md)
- [Travel information questions](references/questions.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Configuration]

**Output Format:** [Markdown travel guide with tables, source annotations, warnings, and optional configuration JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language output; live travel data should include source and query-time labels, while estimates should be clearly marked.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter and package.json report 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
