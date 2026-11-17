## Description:

智能旅行攻略生成器。输入目的地城市后，自动搜索小红书、微博、B站、抖音等平台的热门景点推荐，生成带推荐指数排序的景点列表，细化游乐项目并按优先级排序（排除人多/踩坑项目），最终结合网络图片自动生成精美PPT攻略。用于：旅行规划、景点调研、出行攻略制作、行程优化。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yongji921](https://clawhub.ai/user/yongji921)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to plan trips by collecting destination signals from public travel and social platforms, ranking attractions, identifying avoid-list items, and preparing travel-guide presentation content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Destination searches may be sent to public travel or social platforms.

Mitigation: Avoid entering sensitive personal itinerary details and review platform terms before using external searches.

Risk: Travel recommendations and avoid-list notes can reflect stale, promotional, or incomplete public content.

Mitigation: Verify hours, prices, accessibility, safety conditions, and recent reviews before relying on the plan.

Risk: The bundled scripts are scaffolding or JSON generators rather than a complete automated PPT system.

Mitigation: Treat generated presentation content as a draft and review it before sharing or booking travel.

## Reference(s):

- [Travel Planner Case release page](https://clawhub.ai/yongji921/skills/travel-planner-case)
- [推荐指数评分标准](references/scoring-criteria.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance and JSON/PPT data structures produced by helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce a local presentation data file path, itinerary highlights, attraction rankings, and avoid-list reminders.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
