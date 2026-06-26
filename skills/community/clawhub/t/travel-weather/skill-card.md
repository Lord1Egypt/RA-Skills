## Description: <br>
Check weather forecasts and best travel seasons for any destination, including temperature ranges, rainy seasons, typhoon risks, clothing guidance, and related travel booking support powered by Fliggy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-focused agents use this skill to answer destination weather and best-season questions by running the flyai CLI and formatting provider-backed results with booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may install and run an unpinned global npm CLI for broad travel and weather requests. <br>
Mitigation: Install and verify @fly-ai/flyai-cli in a controlled environment before use; do not allow automatic global installation in restricted production agents. <br>
Risk: Weather and travel answers depend on provider-backed CLI output rather than neutral or independently verified weather data. <br>
Mitigation: Treat results as provider-backed travel guidance and cross-check high-impact travel decisions with authoritative weather or travel sources. <br>


## Reference(s): <br>
- [Travel Weather on ClawHub](https://clawhub.ai/dingtom336-gif/travel-weather) <br>
- [Publisher profile: dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with comparison tables, booking links, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should be based on flyai CLI results, include a conclusion first, avoid raw JSON, and preserve the user's language.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
