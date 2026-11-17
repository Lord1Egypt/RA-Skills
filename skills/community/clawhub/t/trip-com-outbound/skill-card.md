## Description:

出境游一站式助手，支持搜索全球酒店、查询国际机票、购买境外景点门票。数据来自Trip.com（携程国际版），预订链接自动携带联盟推广。面向中国出境游用户。

This skill is ready for commercial/non-commercial use.

## Publisher:

[travel-skills](https://clawhub.ai/user/travel-skills)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-planning agents use this skill to search outbound hotels, international flights, and overseas attraction tickets for Chinese-language trip planning. Results include prices, ratings or schedule details, and Trip.com booking links when returned by the upstream service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User travel searches, dates, budgets, and destination details are sent to the publisher's external proxy service.

Mitigation: Install only when this data sharing is acceptable, avoid sending sensitive personal details, and prefer deployments that use documented endpoints and user-supplied secrets.

Risk: Remote results and booking links are displayed without validation.

Mitigation: Treat returned text and links as untrusted, verify prices and booking details directly on Trip.com before purchase, and review destination-specific travel information separately.

Risk: The artifact contains a fixed proxy endpoint and embedded token.

Mitigation: Rotate credentials before deployment and configure secrets outside the skill artifact where possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/travel-skills/skills/trip-com-outbound)
- [Publisher profile](https://clawhub.ai/user/travel-skills)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with command examples and returned travel-search text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include prices, ratings, flight times, attraction details, and Trip.com booking links returned by the remote service.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
