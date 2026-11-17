## Description:

Book professional interpreters in the Netherlands, Belgium, Germany, Luxembourg, and France for phone, video, or on-site assignments through the Tolk2Go public API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tolk2go](https://clawhub.ai/user/tolk2go)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to search interpreter availability, review pricing, create booking requests, poll interpreter responses, and confirm interpreters through Tolk2Go.

### Deployment Geography for Use:

Netherlands, Belgium, Germany, Luxembourg, and France

## Known Risks and Mitigations:

Risk: Booking, registration, or login can send email, password, appointment details, address data, and medical or legal context to Tolk2Go.

Mitigation: Confirm user intent before sending personal or sensitive details, and keep free-text context limited to what is needed for the booking.

Risk: On-site bookings require precise location details.

Mitigation: Ask the user to confirm the address and coordinates before creating an on-site booking.

Risk: Bearer tokens expire after five minutes.

Mitigation: Re-authenticate when a booking request receives an authorization failure instead of reusing an expired token.

## Reference(s):

- [Tolk2Go OpenAPI Specification](https://api.tolk2go.com/api/v1/spec)
- [Tolk2Go Website](https://www.tolk2go.com)
- [ClawHub Skill Page](https://clawhub.ai/tolk2go/skills/tolk2go)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Shell commands, Configuration]

**Output Format:** [Markdown with API request examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes booking-flow sequencing, UTC time handling, authentication notes, pricing presentation guidance, and endpoint-specific requirements.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
