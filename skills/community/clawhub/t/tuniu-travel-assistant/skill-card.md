## Description: <br>
Tuniu Travel Assistant helps agents search and book hotels, flights, trains, scenic tickets, cruises, and vacation products through a configured travel proxy, with Markdown-formatted results and related-service recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[travel-skills](https://clawhub.ai/user/travel-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-assistant agents use this skill to look up travel options and optionally create or cancel bookings for hotels, flights, trains, scenic tickets, cruises, and vacation products. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Booking and cancellation tools can submit or cancel travel orders with traveler contact and identity details. <br>
Mitigation: Require the agent to show a final booking or cancellation summary and get explicit user confirmation before invoking create_order, save_order, book, or cancel_order tools. <br>
Risk: The skill requires a proxy token and forwards travel query or order data to the configured travel proxy and travel platform. <br>
Mitigation: Install only with a trusted PROXY_URL and PROXY_TOKEN, and disclose that traveler details are forwarded to the travel platform when the user chooses to book. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/travel-skills/skills/tuniu-travel-assistant) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON] <br>
**Output Format:** [JSON objects with optional Markdown-formatted travel results and error messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results may include realtime prices, availability, images, and related-service recommendations; booking and cancellation tools return proxy/platform responses.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
