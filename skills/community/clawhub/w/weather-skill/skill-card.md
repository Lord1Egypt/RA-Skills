## Description: <br>
Returns current weather details for a requested city using wttr.in, with SkillPay billing configured at 0.001 USDT per call. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[loverun321](https://clawhub.ai/user/loverun321) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to look up current city-level weather conditions and receive structured weather data after the configured per-call payment flow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill publishes and uses a SkillPay API key in the artifact files. <br>
Mitigation: Review carefully before installing; the publisher should remove the exposed key from the artifact and rotate it before broader use. <br>
Risk: The skill charges 0.001 USDT per successful call through SkillPay. <br>
Mitigation: Only install or invoke the skill where paid per-call execution is acceptable to the user or operator. <br>


## Reference(s): <br>
- [Weather Skill on ClawHub](https://clawhub.ai/loverun321/weather-skill) <br>
- [wttr.in weather service](https://wttr.in) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, API calls, Weather data] <br>
**Output Format:** [JSON object containing city, temperature, condition, humidity, wind, visibility, UV index, and payment status fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return payment-required or input-error objects instead of weather data when billing fails or no city is provided.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
