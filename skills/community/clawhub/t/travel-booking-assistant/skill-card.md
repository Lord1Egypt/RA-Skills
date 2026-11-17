## Description:

A Booking.com hotel assistant for international hotel search, room availability checks, price comparison, and reservation-management workflows using Booking.com partner APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryan-zry](https://clawhub.ai/user/ryan-zry)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-support agents use this skill to search international hotels, compare room details and prices, and manage Booking.com reservation workflows. Developers can use the included Python API wrapper and OpenAI function-call adapter as integration scaffolding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hotel availability, prices, cancellation terms, and reviews may be fixed sample data rather than live Booking.com results.

Mitigation: Require tested live API calls and clearly label or block sample data before using the skill for traveler-facing decisions.

Risk: Reservation creation, lookup, or cancellation may be advertised before the booking workflow is fully implemented.

Mitigation: Do not create, change, or cancel reservations unless a live partner API confirms the action and the confirmation is shown to the user.

Risk: Currency and cancellation information can create user harm if stale or transformed incorrectly.

Mitigation: Display prices, currencies, taxes, fees, and cancellation terms exactly as returned by the API, with timestamped exchange-rate context when conversion is shown.

## Reference(s):

- [Booking.com Distribution API endpoint](https://distribution-xml.booking.com/json/bookings.getHotels)
- [Booking.com Distribution API base URL](https://distribution-xml.booking.com/json)
- [ClawHub skill page](https://clawhub.ai/ryan-zry/skills/travel-booking-assistant)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance, JSON function-call schemas, and Python integration code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and Booking.com API credentials before live use.]

## Skill Version(s):

1.0.0 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
