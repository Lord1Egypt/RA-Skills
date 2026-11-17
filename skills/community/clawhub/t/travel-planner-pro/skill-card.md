## Description:

提供深度个性化、全链条的智能旅游规划服务，涵盖行程设计、交通优化、餐饮住宿推荐、省钱小招、避坑指南、安全保障和购物体验。

This skill is ready for commercial/non-commercial use.

## Publisher:

[e2e5g](https://clawhub.ai/user/e2e5g)

### License/Terms of Use:

MIT-0

## Use Case:

Travelers and travel-planning assistants use this skill to create personalized itineraries, route plans, budgets, safety notes, accessibility guidance, and local recommendations. It is especially oriented toward Chinese-language trip planning that can adapt to current destination conditions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Travel plans can become inaccurate when weather, transport, attraction policies, prices, or safety conditions change.

Mitigation: Check current destination information before planning and update recommendations when conditions change.

Risk: Travel planning can involve sensitive personal details such as budget, itinerary dates, accessibility needs, family composition, and dietary restrictions.

Mitigation: Ask only for details needed to plan the trip and avoid sharing unnecessary personal information.

Risk: The skill may use an external image-generation service for itinerary cards.

Mitigation: Skip external image generation or use the user's preferred service when external visual generation is not appropriate.

## Reference(s):

- [Itinerary template](references/itinerary-template.md)
- [ClawHub skill page](https://clawhub.ai/e2e5g/skills/travel-planner-pro)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Image prompts]

**Output Format:** [Markdown travel plans with structured lists and optional hand-drawn infographic prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single responses are intended to stay under 2000 Chinese characters unless more detail is needed.]

## Skill Version(s):

1.0.0 (source: release evidence and _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
