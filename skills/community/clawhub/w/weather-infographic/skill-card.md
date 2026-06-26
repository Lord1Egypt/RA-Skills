## Description: <br>
Generate a TV-style weather infographic with a location-specific seasonal background. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[silverkiwi](https://clawhub.ai/user/silverkiwi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to create a local TV-style weather image for a specified address and coordinates, combining live forecast data with a generated seasonal background. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Gemini image generation can consume API quota or billable usage. <br>
Mitigation: Use a Gemini API key with appropriate quotas or billing limits and monitor usage for generated images. <br>
Risk: Addresses and coordinates are sent to Open-Meteo and included in prompts sent to Google Gemini. <br>
Mitigation: Enter only locations that are acceptable to share with those external services. <br>
Risk: Generated weather graphics may misrender or stylize forecast details. <br>
Mitigation: Compare important values against the source forecast before publishing or relying on the image. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/silverkiwi/weather-infographic) <br>
- [Open-Meteo Forecast API](https://api.open-meteo.com/v1/forecast) <br>


## Skill Output: <br>
**Output Type(s):** [files, shell commands, guidance] <br>
**Output Format:** [PNG image file with terminal status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires address, latitude, longitude, output path, GEMINI_API_KEY, and network access to Open-Meteo and Google Gemini.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
