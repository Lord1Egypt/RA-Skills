## Description:

Access global ocean tides model. Functions include tide height at a given date/time/location, tide extrema, and grid weather data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hamandmore](https://clawhub.ai/user/hamandmore)

### License/Terms of Use:


## Use Case:

External developers and agents use this skill to call the hamandmore.net JSON-RPC API for tide heights, tide extrema, and grid weather variables by location and time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries may send coordinates, times, requested weather variables, and optional hamandmore.net API tokens to the disclosed service endpoint.

Mitigation: Use service-specific tokens only, avoid reusing unrelated secrets, and send only coordinates and time ranges appropriate for the intended request.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hamandmore/skills/tides)
- [Disclosed JSON-RPC API endpoint](https://hamandmore.net/api/harmonics/mcp)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration]

**Output Format:** [Markdown with JSON and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The API returns JSON-RPC responses with stringified JSON text and preferred structured JSON content.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
