## Description:

Helps travelers search private jet empty legs, compare indicative charter prices, and obtain booking links through SkyAccess.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skyaccess](https://clawhub.ai/user/skyaccess)

### License/Terms of Use:

MIT-0

## Use Case:

Travelers and travel planners use this skill to find available private jet empty legs, check charter price estimates, and follow booking links. Travelers may also ask SkyAccess to contact them about a trip.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Searches and booking-contact requests send trip details to SkyAccess.

Mitigation: Share only trip details needed for the request and avoid unrelated sensitive information in notes.

Risk: Booking-contact requests send a traveler's name and email to SkyAccess.

Mitigation: Use the contact request only when the traveler asks SkyAccess to contact them and provides those details.

Risk: Flight inventory changes and charter estimates are not binding quotes.

Mitigation: Refresh searches before presenting options and have the traveler verify final pricing and availability before booking.

## Reference(s):

- [SkyAccess skill listing](https://clawhub.ai/skyaccess/skills/skyaccess)
- [SkyAccess](https://skyaccess.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with flight listings, indicative price ranges, and booking links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search returns up to five flights; availability and prices may change.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
