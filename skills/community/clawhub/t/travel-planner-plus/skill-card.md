## Description:

Generates personalized travel itineraries with attraction, hotel, dining, and route planning, then produces a Word travel guide for delivery to the user.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ggyybb](https://clawhub.ai/user/ggyybb)

### License/Terms of Use:

MIT-0

## Use Case:

Travelers and travel-planning agents use this skill to turn trip requirements such as destination, duration, traveler type, and preferences into a structured itinerary. It supports attraction, hotel, dining, and transportation planning and can generate a Word document for delivery to the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trip locations and route details may be sent to Baidu Maps.

Mitigation: Use the skill only when the user is comfortable sharing itinerary locations and route details with Baidu Maps.

Risk: Generated travel files may be sent through Feishu.

Mitigation: Confirm that the generated document does not contain sensitive personal details before sending it through Feishu.

Risk: API keys can be exposed if the skill searches broad memory files or logs key prefixes.

Mitigation: Provide a scoped Baidu Maps key through a dedicated secret mechanism and avoid searching general memory files for credentials.

## Reference(s):

- [Output Template](references/output-template.md)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with Python-generated DOCX travel guide files and inline shell/API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires trip details and a scoped Baidu Maps API key; may send generated Word files through Feishu.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
