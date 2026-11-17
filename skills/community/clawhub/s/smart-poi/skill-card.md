## Description:

6项工具覆盖景点、酒店、交通、美食、火车票、机票，含图片和预订链接，途牛+高德数据直连，零配置即装即用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[travel-skills](https://clawhub.ai/user/travel-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Travel users and agents use this skill to search domestic China attractions, nearby hotels and restaurants, local transport options, and train or flight options while planning an itinerary.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Travel searches, locations, origin and destination details, and travel dates are sent through cloud proxy services to travel and map providers.

Mitigation: Use the skill only for travel planning data that users are comfortable sharing with those external services, and avoid entering sensitive personal details.

Risk: Recommendation, price, ticket, route, rating, and availability results can be incomplete or stale because they depend on live third-party provider data.

Mitigation: Confirm prices, availability, routes, and booking terms on the linked provider page before making travel decisions or purchases.

Risk: The skill provides booking links but does not complete purchases or reservations itself.

Mitigation: Treat booking links as handoff points and review all order details on the destination platform before checkout.

Risk: The skill is documented as covering domestic China attractions, with possible gaps in smaller-city transport and restaurant data.

Mitigation: Use another map or travel source for unsupported destinations, overseas points of interest, or city coverage that appears incomplete.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/travel-skills/skills/smart-poi)
- [ClawHub Publisher Profile](https://clawhub.ai/user/travel-skills)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown text with travel search results, images, prices, route summaries, and booking links when available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are returned from external travel and map providers through cloud proxy services; prices, availability, travel time, ratings, and coverage may change.]

## Skill Version(s):

2.0.9 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
