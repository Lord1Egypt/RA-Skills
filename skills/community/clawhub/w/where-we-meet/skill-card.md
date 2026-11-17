## Description:

Where We Meet helps an agent recommend up to five meetup locations for a group based on each person's starting point, city, travel mode, and food or entertainment preferences.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gggggyyyyy000](https://clawhub.ai/user/gggggyyyyy000)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill through an agent to choose fair meetup, dining, or activity locations for people starting from different places. The skill prepares the request for the bundled location planner and returns the generated venue comparison without rewriting it.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send sensitive location data, such as home or work addresses, to Amap.

Mitigation: Use approximate landmarks when possible and proceed only when users are comfortable sharing the provided locations with Amap.

Risk: The release evidence reports that the local script implementation is not packaged with the skill artifact.

Mitigation: Verify that scripts/where-we-meet.js is supplied from a trusted source before running the skill.

## Reference(s):

- [Server-resolved GitHub source](https://github.com/GggggYyyyy000/where-we-meet)
- [ClawHub skill page](https://clawhub.ai/gggggyyyyy000/skills/where-we-meet)
- [Publisher profile](https://clawhub.ai/user/gggggyyyyy000)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Final response text, optional MEDIA line for a QR code PNG, mobile map schema URL, and PC HTML comparison file path]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default output includes five candidate locations, travel-time comparisons, representative venues, nearby similar venue counts, and map access details when available.]

## Skill Version(s):

0.1.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
