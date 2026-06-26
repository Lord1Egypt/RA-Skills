## Description: <br>
Smart hotel search, supporting filtering by location, date, star rating, and budget. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zxc-Aqr](https://clawhub.ai/user/zxc-Aqr) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and travel-planning agents use this skill to search hotels, compare room prices, retrieve hotel details, and discover available hotel filter tags from structured travel criteria. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Hotel search prompts may contain personal details or payment-related information that should not be sent to the hotel service. <br>
Mitigation: Send only structured hotel search criteria such as location, dates, occupancy, star rating, budget, tags, country, currency, and language; remove names, phone numbers, emails, IDs, payment details, loyalty numbers, and travel document data before tool calls. <br>
Risk: Hotel pricing and availability can vary by country, currency, date, and language settings. <br>
Mitigation: Verify country, currency, dates, and language settings before relying on returned hotel results or prices. <br>


## Reference(s): <br>
- [Star Hotel Search ClawHub Page](https://clawhub.ai/zxc-Aqr/star-hotel) <br>
- [Star Hotel MCP endpoint](https://mcp.aigohotel.com/mcp) <br>
- [Star Hotel API key application](https://mcp.agentichotel.cn/apply) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration, guidance] <br>
**Output Format:** [Markdown or structured JSON from hotel search and detail tools] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Hotel results may include hotel names, locations, amenities, tags, room rates, booking URLs, currency, availability, and cancellation policy details.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
