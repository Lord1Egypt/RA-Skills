## Description: <br>
Booking.com国际酒店预订助手，支持全球酒店搜索、房型查询、价格对比、预订管理。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryan-zry](https://clawhub.ai/user/ryan-zry) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel planners use this skill to search international hotels, compare room options and prices, and manage Booking.com-style reservations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Hotel availability, pricing, room, review, and reservation details may be misleading because the security evidence reports hardcoded travel data rather than live Booking.com API results. <br>
Mitigation: Review before installing and rely on it for real travel only after it calls live Booking.com APIs and clearly labels any demo data. <br>
Risk: Booking or cancellation actions can affect travel plans if treated as confirmed without safeguards. <br>
Mitigation: Require explicit user confirmation and verified live reservation details before creating or canceling bookings. <br>


## Reference(s): <br>
- [ClawHub release: trip-booking-hub](https://clawhub.ai/ryan-zry/trip-booking-hub) <br>
- [Booking.com Distribution API](https://distribution-xml.booking.com/json/bookings.getHotels) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, API calls, guidance] <br>
**Output Format:** [JSON function-call responses and Markdown-style hotel tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3; real booking use requires valid Booking.com API access and live data handling.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
