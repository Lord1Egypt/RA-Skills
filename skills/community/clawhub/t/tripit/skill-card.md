## Description:

Create and update TripIt travel plans by generating structured confirmation emails for flights, hotels, activities, car rentals, rail, and cruises.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adamwestland](https://clawhub.ai/user/adamwestland)

### License/Terms of Use:

MIT-0

## Use Case:

Travelers and agents use this skill to turn itinerary details into TripIt-compatible email text and send those details through an available email tool to plans@tripit.com.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated itinerary emails can expose traveler names, confirmation numbers, dates, destinations, and booking details to TripIt.

Mitigation: Review the generated email text with the user before sending and include only itinerary details the user approves.

Risk: A private TripIt iCal feed URL can provide ongoing access to itinerary data if stored or logged.

Mitigation: Do not store the feed URL unless the user explicitly chooses that and secure secret storage, redaction, and deletion controls are available.

Risk: Itinerary details copied from untrusted booking messages may be incorrect or misleading.

Mitigation: Check dates, confirmation numbers, traveler names, and destinations before sending the generated email.

## Reference(s):

- [TripIt Email Template Format Reference](references/template-format.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text TripIt Approved email body generated from JSON input, with an optional subject line.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a separate email-sending capability; validates required fields and warns on non-ISO dates.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
