## Description: <br>
Weather and forecasts with no API key: one wttr.in fetch by default, with Open-Meteo fallback if wttr.in fails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maximedogawa](https://clawhub.ai/user/maximedogawa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer current weather and forecast questions for named places in concise, plain language. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Place names requested by the user are sent to wttr.in and may be sent to Open-Meteo if fallback is needed. <br>
Mitigation: Install only when sending requested locations to those public weather services is acceptable for the intended use. <br>


## Reference(s): <br>
- [Weather 2.0 on ClawHub](https://clawhub.ai/maximedogawa/weather-2-0) <br>
- [wttr.in help](https://wttr.in/:help) <br>
- [Open-Meteo weather codes](https://open-meteo.com/en/docs#api_form) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Concise natural-language weather summaries with optional inline curl commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and sends requested place names to public weather services.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
