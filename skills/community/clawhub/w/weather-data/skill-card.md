## Description:

Provides weather forecast data from NOAA. Free tier returns 3-day forecast, premium tier returns 7-day with hourly data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[letorresmeza](https://clawhub.ai/user/letorresmeza)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to retrieve NOAA-based weather forecast guidance for a latitude and longitude, including a free 3-day forecast and a paid premium 7-day hourly forecast.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Premium forecast requests are documented as costing 0.05 USDC.

Mitigation: Only provide an X-Payment header when the user intends to use the paid premium forecast endpoint.

Risk: The artifact documents local weather-service endpoints but does not provide or run the service.

Mitigation: Confirm that the local service is trusted and available before issuing requests.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline curl commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include free and paid endpoint guidance; premium access is documented as costing 0.05 USDC.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
