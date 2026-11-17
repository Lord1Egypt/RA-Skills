## Description:

Provides the top 3 surf spots in a selected region by gathering public Surfline forecast data and ranking valid spots with a defined wave and wind scoring rubric.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wertopter](https://clawhub.ai/user/wertopter)

### License/Terms of Use:

MIT-0

## Use Case:

Surfers, trip planners, and surf-focused agents use this skill to compare surf spots in a supported region or supplied Surfline spot list and return a concise top-3 recommendation with scoring rationale.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the skill contacts Surfline public services, and custom spot IDs supplied by a user are sent to Surfline.

Mitigation: Tell users when an external Surfline lookup is required and avoid submitting sensitive or nonpublic identifiers as custom spot IDs.

Risk: Results depend on Surfline service availability and returned forecast data for the selected region or spot IDs.

Mitigation: Report fetch failures or exclusions clearly and treat the ranking as forecast-based guidance rather than a guarantee of local surf conditions.

## Reference(s):

- [Surf Forecast Agent on ClawHub](https://clawhub.ai/wertopter/skills/surf-spot-finder)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown ranking with scored recommendations and supporting forecast values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns up to three valid spots, excludes failed or missing forecast data, and names the top recommendation.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
