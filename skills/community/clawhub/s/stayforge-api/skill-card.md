## Description: <br>
Hotel booking and accommodation search using StayForge API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Jbennett111](https://clawhub.ai/user/Jbennett111) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and travel-support agents use this skill to search hotels, compare accommodation options, and manage StayForge bookings through API calls. It supports leisure travel, business travel, group bookings, price alerts, booking status checks, modifications, and cancellations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send travel and guest details to the StayForge API. <br>
Mitigation: Share personal details only after user approval and use a per-user API key stored in an approved secret store. <br>
Risk: The skill can create, modify, or cancel real hotel reservations. <br>
Mitigation: Confirm hotel, room, dates, total price, cancellation terms, guest contact details, and the requested booking action before calling booking or cancellation endpoints. <br>
Risk: Hotel availability, pricing, and cancellation policies may change before booking. <br>
Mitigation: Check current availability and present final price and cancellation terms immediately before completing a reservation. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/Jbennett111/stayforge-api) <br>
- [StayForge API key endpoint](https://stayforge.vosscg.com/v1/keys) <br>
- [StayForge hotel search endpoint](https://stayforge.vosscg.com/v1/hotels/search) <br>
- [StayForge advanced hotel search endpoint](https://stayforge.vosscg.com/v1/hotels/search/advanced) <br>
- [StayForge booking creation endpoint](https://stayforge.vosscg.com/v1/bookings/create) <br>
- [VCG forges plans](https://vosscg.com/forges) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses per-user StayForge API keys and may handle travel, guest, pricing, booking, modification, and cancellation details.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
