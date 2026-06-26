## Description: <br>
Plan TfL journeys from start/end/time, resolve locations (prefer postcodes), and warn about disruptions; suggest alternatives when disrupted. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diegopetrucci](https://clawhub.ai/user/diegopetrucci) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to plan London public transport journeys through TfL, resolve ambiguous locations, check current line disruptions, and present route alternatives when disruption affects the top option. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Journey origins, destinations, requested travel times, and optional TfL API credentials are sent to TfL when the helper is used. <br>
Mitigation: Use the skill only when sharing those journey details with TfL is acceptable, and provide TFL_APP_ID or TFL_APP_KEY only in an environment where those credentials are approved for TfL API requests. <br>
Risk: Disruption statuses reflect current TfL conditions and may change before a future journey begins. <br>
Mitigation: For journeys later today or on another date, present disruption information as current status and advise the user to recheck closer to travel time. <br>


## Reference(s): <br>
- [TfL API documentation](https://tfl.gov.uk/info-for/open-data-users/api-documentation) <br>
- [Skill page](https://clawhub.ai/diegopetrucci/transport-for-london-journey-disruption) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and route summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include TfL journey options, line disruption warnings, disambiguation choices, and current-status caveats for future travel.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
