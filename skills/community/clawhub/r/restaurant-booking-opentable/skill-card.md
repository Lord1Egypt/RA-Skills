## Description:

Books restaurant reservations on OpenTable through a browser session, including hidden time-slot controls and terms checkboxes when needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eeshita-pande](https://clawhub.ai/user/eeshita-pande)

### License/Terms of Use:

MIT-0

## Use Case:

External users and assistants use this skill to reserve OpenTable restaurant tables in an authenticated browser session, selecting the restaurant, date, time, party size, seating option, and completing the booking when prerequisites are met.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent can act in an authenticated OpenTable session with a saved payment method.

Mitigation: Require the agent to show the restaurant, date, time, party size, booking type, fees or cancellation terms, and consent text before submitting a reservation.

Risk: The booking flow may expose payment or personal form details that are not needed for the final answer.

Mitigation: Do not collect or report full card details or broad form values; report only necessary booking confirmation details and, at most, the card last four digits if shown.

Risk: The skill may choose consequential alternatives such as a nearest available time slot or booking type.

Mitigation: Ask the user before accepting materially different times, non-standard booking types, fees, cancellation terms, or other commitments.

Risk: JavaScript fallbacks interact with page elements that may be hidden from the accessibility snapshot.

Mitigation: Re-snapshot after each action and verify the visible booking state before proceeding to confirmation.

## Reference(s):

- [Browser Booking JS Snippet Reference](artifact/browser-snippets.md)
- [ClawHub skill page](https://clawhub.ai/eeshita-pande/skills/restaurant-booking-opentable)

## Skill Output:

**Output Type(s):** [guidance, code, text]

**Output Format:** [Markdown guidance with browser tool steps and JavaScript snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an enabled headed browser session, an authenticated OpenTable account, and a saved payment card; final responses should summarize confirmation details without exposing full card data.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
