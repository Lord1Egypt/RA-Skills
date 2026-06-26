## Description: <br>
Get AI-powered marine weather forecasts for any location worldwide. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sealegs-ai-coder](https://clawhub.ai/user/sealegs-ai-coder) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, agents, and boating-focused users use this skill to request SeaLegs SpotCast marine forecasts, poll forecast status, retrieve AI weather analysis, and present boating condition guidance for specified coordinates and vessels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Forecast requests send locations, dates, vessel details, and optional metadata to SeaLegs using the configured API key. <br>
Mitigation: Only send information the user is comfortable sharing, and avoid secrets or sensitive personal data in metadata or webhook payloads. <br>
Risk: Creating or refreshing forecasts consumes SeaLegs credits. <br>
Mitigation: Ask for user confirmation before creating or refreshing forecasts. <br>
Risk: GO, CAUTION, and NO-GO labels can be incomplete or unsuitable as the sole basis for boating decisions. <br>
Mitigation: Present the labels as forecast guidance and advise users to verify conditions and apply local boating judgment before departure. <br>


## Reference(s): <br>
- [SeaLegs Developer Portal](https://developer.sealegs.ai) <br>
- [ClawHub skill page](https://clawhub.ai/sealegs-ai-coder/sealegs-marine-forecast) <br>
- [Publisher profile](https://clawhub.ai/user/sealegs-ai-coder) <br>
- [SpotCast API endpoint](https://api.sealegs.ai/v3/spotcast) <br>
- [spotcast-workflow.md](artifact/spotcast-workflow.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JSON examples, bash curl commands, and Python workflow code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SEALEGS_API_KEY and curl for documented command examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
