## Description:

Hotel booking and accommodation search using StayForge API for hotel search, availability checks, reservations, booking management, travel accommodation, lodging discovery, and hotel comparison.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jbennett111](https://clawhub.ai/user/jbennett111)

### License/Terms of Use:


## Use Case:

External users and travel-focused agents use this skill to search StayForge hotel inventory, compare accommodation options, create API keys, and manage bookings. It supports vacation planning, business travel, group quotes, last-minute lodging, and price alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create, cancel, or modify reservations and may affect costs, refunds, or cancellation terms.

Mitigation: Require the agent to show the exact booking, cancellation, or modification details and obtain explicit user approval before taking action.

Risk: The skill may transmit personal or payment-related travel data to the StayForge API.

Mitigation: Require the agent to disclose what data will be sent and avoid sending sensitive details until the user confirms.

Risk: The security verdict is suspicious because mandatory confirmation safeguards are not built into the skill text.

Mitigation: Deploy with an approval policy for booking, cancellation, modification, API-key signup, and price-alert workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jbennett111/skills/stayforge-api)
- [Publisher profile](https://clawhub.ai/user/jbennett111)
- [StayForge API key endpoint](https://stayforge.vosscg.com/v1/keys)
- [StayForge hotel search endpoint](https://stayforge.vosscg.com/v1/hotels/search)
- [StayForge booking creation endpoint](https://stayforge.vosscg.com/v1/bookings/create)
- [VCG Forge plans](https://vosscg.com/forges)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API calls, Configuration]

**Output Format:** [Markdown with curl examples, JSON examples, and step-by-step guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses user-provided email, API keys, travel dates, destination details, guest information, and booking identifiers when interacting with the StayForge API.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
