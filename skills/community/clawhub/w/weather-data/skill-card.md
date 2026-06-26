## Description: <br>
Provides weather forecast data from NOAA. Free tier returns 3-day forecast, premium tier returns 7-day with hourly data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[letorresmeza](https://clawhub.ai/user/letorresmeza) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users can use this skill to request NOAA-based weather forecasts by latitude and longitude through documented local forecast endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requests target a localhost weather service, so an unintended local service could receive forecast requests or payment headers. <br>
Mitigation: Confirm that localhost:5000 is the intended weather service before sending requests. <br>
Risk: The premium endpoint requires an x402 payment header for a stated 0.05 USDC charge. <br>
Mitigation: Send a payment header only after confirming the charge and deciding to use the premium forecast endpoint. <br>


## Reference(s): <br>
- [ClawHub Weather Data API release page](https://clawhub.ai/letorresmeza/weather-data) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with curl command examples and endpoint guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Forecast requests accept latitude and longitude parameters; premium forecast requests require an x402 payment header.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
