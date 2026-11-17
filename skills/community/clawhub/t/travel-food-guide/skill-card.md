## Description:

帮旅行者找景点周边餐厅、当地必吃特色、生成多日餐饮计划，旅途中不踩雷、不错过当地特色。暑期旅行美食探店，各地特色小吃推荐

This skill is ready for commercial/non-commercial use.

## Publisher:

[travel-skills](https://clawhub.ai/user/travel-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Travelers and travel-planning agents use this skill to find restaurants near destinations, surface local specialty foods, and draft multi-day dining plans based on location, budget, preferences, and itinerary context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Travel locations, dining preferences, and restaurant search terms are sent to the skill proxy and downstream map POI service.

Mitigation: Install only when that data flow is acceptable and avoid entering sensitive personal details that are not needed for restaurant search or meal planning.

Risk: The skill uses a proxy token for access to the restaurant search service.

Mitigation: Scope the proxy token specifically to this service and do not reuse it for unrelated accounts or infrastructure.

Risk: Restaurant details and availability may be incomplete or stale because the skill provides POI information and does not support booking, queue status, delivery lookup, or live review verification.

Mitigation: Treat recommendations as planning guidance and verify critical restaurant details directly before travel or purchase decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/travel-skills/skills/travel-food-guide)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON, guidance]

**Output Format:** [Natural-language guidance derived from JSON tool results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include restaurant names, addresses, distances, ratings when available, average cost estimates, local specialty lists, food streets, and day-by-day meal plans.]

## Skill Version(s):

1.0.19 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
