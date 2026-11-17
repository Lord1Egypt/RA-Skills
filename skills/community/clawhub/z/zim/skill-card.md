## Description:

Agent travel middleware for searching flights, hotels, and car rentals, assembling policy-aware itineraries, managing traveler preferences, and preparing payment-ready booking workflows via Stripe Checkout.

This skill is ready for commercial/non-commercial use.

## Publisher:

[robinmtzieme-commits](https://clawhub.ai/user/robinmtzieme-commits)

### License/Terms of Use:

MIT-0

## Use Case:

External users, travel operations teams, and developers use Zim to turn travel requests into policy-aware flight, hotel, car, and itinerary options with approval and payment-ready workflow support. The current package prepares booking paths and payment sessions, but supplier-side reservation execution remains manual or placeholder-only unless a real executor is added.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Deployable API modes can expose or change sensitive travel and payment data when secrets, authentication, or webhook verification are missing or weak.

Mitigation: Use controlled development deployments until authentication and webhook verification are fixed or tightly configured, and protect or minimize stored passport, contact, payment, booking, and conversation data.

Risk: Public affiliate markers and API tokens can be confused or exposed in generated links.

Mitigation: Separate public affiliate markers from API tokens and rotate any Travelpayouts token already emitted in generated links.

Risk: OpenRouter and Twilio integrations can introduce third-party data processing for travel conversations.

Mitigation: Document those data flows before production use and avoid sending unnecessary sensitive traveler data.

## Reference(s):

- [Zim API Integration Guide](references/api-guide.md)
- [Zim Agent-to-Agent Booking Model](references/agent-to-agent-booking.md)
- [Travelpayouts Support Documentation](https://support.travelpayouts.com/hc/en-us/categories/200358578)
- [ClawHub Skill Page](https://clawhub.ai/robinmtzieme-commits/skills/zim)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include affiliate deeplinks, payment session status, approval state, and booking-ready itinerary summaries.]

## Skill Version(s):

3.0.2 (source: ClawHub release metadata, released 2026-04-20; artifact pyproject.toml version is 0.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
