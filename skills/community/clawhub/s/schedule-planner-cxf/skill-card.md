## Description:

Plan requested travel itineraries, compare flight/train/hotel prices, and generate local itinerary HTML with optional public platform homepage QR codes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cryptocxf](https://clawhub.ai/user/cryptocxf)

### License/Terms of Use:

MIT-0

## Use Case:

Travelers, assistants, and developers use this skill to plan concrete trips, compare Tuniu flight/train/hotel options, and export local itinerary pages without booking or payment handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live travel searches require a Tuniu API key and send travel search details to Tuniu.

Mitigation: Use the skill only when that data transfer is acceptable, keep the API key in the local process environment, and exclude passenger identity, phone numbers, order IDs, and payment links from inputs.

Risk: Generated itinerary files can contain user travel details.

Mitigation: Review generated local files before sharing them and do not upload or publish them without explicit user authorization.

## Reference(s):

- [Input and Output Usage](artifact/references/usage.md)
- [Transport Comparison Reference](artifact/references/transport-comparison.md)
- [City Guides](artifact/references/city-guides.md)
- [ClawHub Skill Page](https://clawhub.ai/cryptocxf/skills/schedule-planner-cxf)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Markdown guidance, JSON inputs, and local HTML itinerary files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated local files may contain travel details; live queries require TUNIU_API_KEY and send necessary search details to Tuniu.]

## Skill Version(s):

1.0.13 (source: SKILL.md metadata, package.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
