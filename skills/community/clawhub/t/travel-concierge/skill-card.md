## Description:

Find contact details for accommodation listings (Airbnb, Booking.com, VRBO, Expedia).

This skill is ready for commercial/non-commercial use.

## Publisher:

[arein](https://clawhub.ai/user/arein)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to run the travel-concierge CLI for user-provided accommodation listing URLs and present a contact dossier for direct booking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to run an unbundled travel-concierge executable.

Mitigation: Install and run the executable only from a known, trusted source, and review it before agent use.

Risk: The skill extracts contact details from accommodation listing pages, and some platforms restrict scraping.

Mitigation: Use it only with user-provided listing URLs and confirm that use complies with the relevant platform terms and local rules.

Risk: Broad triggers may cause the skill to run for contact-finding requests outside the intended accommodation-listing use case.

Mitigation: Narrow triggers or add review steps so the agent only invokes the CLI for supported accommodation platforms.

Risk: Optional API key configuration is mentioned, but storage and handling expectations are not documented in the artifact.

Mitigation: Clarify API key storage, access controls, and rotation before configuring enhanced result sources.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or text dossier with optional JSON from the CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include property information, contact methods, sources, and confidence levels.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
