## Description:

Plan TfL journeys from start/end/time, resolve locations (prefer postcodes), and warn about disruptions; suggest alternatives when disrupted.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diegopetrucci](https://clawhub.ai/user/diegopetrucci)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to plan TfL journeys from an origin, destination, and time, then check current line disruptions and suggest alternatives when routes are affected.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Route origins, destinations, dates, and times are sent to TfL's public API.

Mitigation: Use the skill only when sharing that travel data with TfL is acceptable.

Risk: Optional TFL_APP_ID and TFL_APP_KEY credentials may be exposed to the helper script environment.

Mitigation: Provide TfL credentials only in environments where API access is intended and credentials are appropriately scoped.

Risk: Disruption statuses reflect current conditions and may change before future travel.

Mitigation: For future journeys, re-check disruption status near the intended travel time.

## Reference(s):

- [Transport for London API documentation](https://tfl.gov.uk/info-for/open-data-users/api-documentation)
- [Transport for London API](https://api.tfl.gov.uk)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance and plain-text route summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include live route durations, leg summaries, disruption warnings, disambiguation options, and alternative routes.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
