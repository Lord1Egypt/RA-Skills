## Description:

途牛全品类旅行查询预订技能，酒店/机票/火车票/景点门票/邮轮/度假17个工具一站式服务，含图片展示和跨品类推荐。暑假跟团自由行，途牛精选线路推荐

This skill is ready for commercial/non-commercial use.

## Publisher:

[travel-skills](https://clawhub.ai/user/travel-skills)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to search hotels, flights, trains, attraction tickets, cruises, and vacation products, then prepare supported bookings after reviewing the returned options. Booking flows require user-provided travel and contact details and should be used only when the user intends to create or change a real order.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Booking and cancellation tools can create or change real travel orders.

Mitigation: Review itinerary, passenger, contact, pricing, and order details with the user before invoking booking or cancellation actions.

Risk: Booking flows may send names, phone numbers, identity-document details, and itinerary data through the configured Tencent Cloud proxy to the travel platform.

Mitigation: Collect personal data only when the user is ready to book, and avoid sending unnecessary identity or contact details during search-only workflows.

Risk: Travel prices, availability, schedules, and cancellation rules can change after search results are returned.

Mitigation: Treat returned options as current offers for review and confirm final terms on the booking or payment step before completion.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/travel-skills/skills/tuniu-travel-assistant)
- [Publisher profile](https://clawhub.ai/user/travel-skills)

## Skill Output:

**Output Type(s):** [text, markdown, configuration]

**Output Format:** [JSON objects containing travel search results, booking responses, and Markdown-formatted summaries with image links when available.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PROXY_TOKEN and a permitted PROXY_URL for proxy-backed travel search and booking calls.]

## Skill Version(s):

2.1.19 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
