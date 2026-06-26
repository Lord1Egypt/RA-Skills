## Description: <br>
This skill helps agents query hourly weather forecasts from the Shuzhi Weather API using HMAC-SHA256 authentication and user-provided API credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alex098929](https://clawhub.ai/user/alex098929) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when they want an agent to answer weather questions for named locations or coordinates. The agent checks local Shuzhi API configuration, runs the weather helper script, and presents forecast results in a readable form. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores Shuzhi API credentials in a local config file. <br>
Mitigation: Restrict the config file to user-only permissions and avoid sharing captured errors or logs. <br>
Risk: Weather requests send the queried coordinates to the Shuzhi Weather API. <br>
Mitigation: Only query locations the user intends to share with that external API. <br>
Risk: The server security review warns that an error path may print the full config if required credential fields are missing. <br>
Mitigation: Fix that error path before adding real credentials, or avoid sharing error output from failed configuration checks. <br>


## Reference(s): <br>
- [Shuzhi Weather API Documentation](references/api_response_format.md) <br>
- [ClawHub skill page](https://clawhub.ai/alex098929/shuzhi-weather) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration guidance] <br>
**Output Format:** [Markdown or plain text, with optional JSON weather data from the helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local Shuzhi app_key and app_secret configuration; weather requests send longitude and latitude to the Shuzhi Weather API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
