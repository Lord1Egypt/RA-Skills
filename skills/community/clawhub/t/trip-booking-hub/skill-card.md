## Description:

行程预订中心 helps agents search international hotels, compare room options and prices, and manage Booking.com-style reservations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryan-zry](https://clawhub.ai/user/ryan-zry)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-support agents use this skill to search overseas hotels, compare rooms and prices, and handle reservation-related requests in multiple languages and currencies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The current artifact can present mock hotel availability, prices, reviews, and cancellation terms as live Booking.com results.

Mitigation: Use it only after connecting a verified Booking.com partner API and clearly labeling any fixture or test data as non-authoritative.

Risk: Reservation-management prompts may imply that real bookings can be created, queried, or cancelled.

Mitigation: Require explicit confirmation that booking actions are backed by verified live API calls before treating any reservation response as actionable.

## Reference(s):

- [Booking.com distribution API endpoint](https://distribution-xml.booking.com/json/bookings.getHotels)
- [ClawHub skill page](https://clawhub.ai/ryan-zry/skills/trip-booking-hub)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown tables and JSON-like function responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Hotel, room, review, and reservation-oriented responses may include prices, cancellation terms, currencies, and booking identifiers.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
