## Description: <br>
Queries the weather forecast for a specified city and returns weather conditions and temperature range in Chinese. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuancaihua](https://clawhub.ai/user/yuancaihua) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents can use this skill to answer simple weather questions by extracting a city and date, querying a weather provider, and returning a concise formatted forecast. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Weather queries are sent to a third-party weather service. <br>
Mitigation: Inform users what provider receives requests and what location/date data is shared. <br>
Risk: An embedded weather API key is exposed in the artifact. <br>
Mitigation: Remove and rotate the key, then load credentials from a secure configuration path. <br>
Risk: Weather API failures or slow responses may affect agent reliability. <br>
Mitigation: Add request timeouts, input handling, and clear fallback behavior for provider errors. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yuancaihua/weather-query-ych) <br>


## Skill Output: <br>
**Output Type(s):** [text] <br>
**Output Format:** [Plain text weather response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns city, date, weather status, and temperature range; error responses ask for a valid city or report temporary weather-service unavailability.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
