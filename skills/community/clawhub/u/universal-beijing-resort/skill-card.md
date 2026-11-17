## Description:

北京环球影城一站式游园助手，7项工具覆盖实时排队查询、智能推荐下一步、路线规划、演出时间、营业时间、餐厅推荐、门票价格，零配置即装即用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[travel-skills](https://clawhub.ai/user/travel-skills)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and trip planners use this skill to plan a Beijing Universal Resort visit, including ride wait checks, next-step recommendations, show times, daily routing, dining suggestions, operating hours, and ticket-price guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live wait-time and schedule lookups contact themeparks.wiki, which may receive normal request metadata such as IP address and User-Agent.

Mitigation: Inform installers and users about the external data request and avoid including sensitive personal information in queries.

Risk: Ticket prices and some recommendations are local preset guidance and may be outdated or incomplete for purchase or travel decisions.

Mitigation: Verify pricing, availability, and travel-critical details with official Beijing Universal Resort channels before buying tickets or finalizing plans.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/travel-skills/skills/universal-beijing-resort)
- [ThemeParks.wiki live park data endpoint](https://api.themeparks.wiki/v1/entity/68e1d8f0-ed42-4351-af25-160421e37ce0/live)
- [ThemeParks.wiki park schedule endpoint](https://api.themeparks.wiki/v1/entity/68e1d8f0-ed42-4351-af25-160421e37ce0/schedule)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Plain text with Markdown-style lists in Chinese]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May combine live themeparks.wiki wait-time and schedule data with local preset trip-planning, dining, route, and ticket guidance.]

## Skill Version(s):

1.1.19 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
