## Description:

Check weather forecasts and best travel seasons for any destination \u2014 temperature ranges, rainy seasons, typhoon risks, and what to wear; it also supports flight booking, hotel reservation, train tickets, attraction tickets, itinerary planning, visa info, travel insurance, car rental, and related travel tasks powered by Fliggy (Alibaba Group).

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-focused agents use this skill to answer destination weather, seasonal timing, and related travel-planning questions by querying the flyai CLI and formatting results with booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires installing and executing a third-party travel CLI globally.

Mitigation: Use a version-pinned, locally sandboxed setup and require explicit approval before installation or execution.

Risk: The skill forces commercial booking links and branding into weather and travel answers.

Mitigation: Review outputs for commercial influence and disclose flyai booking links and branding to users before relying on recommendations.

## Reference(s):

- [Travel Weather ClawHub Skill Page](https://clawhub.ai/dingtom336-gif/skills/travel-weather)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and booking links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses are required by the source skill to be conclusion-first, based on flyai CLI output, and include flyai booking links and branding when results are shown.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
