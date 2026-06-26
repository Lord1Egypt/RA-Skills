## Description: <br>
QWeather China provides localized China weather service through the QWeather API, including current conditions, forecasts, life indices, air quality, and weather alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[uni-huang](https://clawhub.ai/user/uni-huang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer China-focused weather questions, including current conditions, multi-day forecasts, air quality, life indices, and weather-based guidance such as umbrella or clothing suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill needs a QWeather JWT private key and sends requested or default city information to QWeather. <br>
Mitigation: Use a dedicated QWeather key stored outside shared application keys, restrict the private key file permissions, and only configure default locations that users are comfortable sending to QWeather. <br>
Risk: Some artifact configuration references .openclaw private-key paths instead of the dedicated QWeather key path. <br>
Mitigation: Remove or ignore those entries before use and configure QWEATHER_PRIVATE_KEY_PATH to a dedicated file such as ~/.config/qweather/private.pem. <br>
Risk: Developer-side file rewriting artifacts are included in the release. <br>
Mitigation: Do not run fix_encoding.py as part of normal installation, and review scripts before executing them in a production or shared environment. <br>
Risk: Authentication errors or debug output could expose sensitive context in shared environments. <br>
Mitigation: Avoid sharing raw auth error output or logs, and run the skill with environment-scoped credentials. <br>


## Reference(s): <br>
- [QWeather China on ClawHub](https://clawhub.ai/uni-huang/qweather-china) <br>
- [QWeather Developer Portal](https://dev.qweather.com/) <br>
- [QWeather Documentation](https://dev.qweather.com/docs/) <br>
- [QWeather City Resource](https://dev.qweather.com/docs/resource/city/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text weather responses, with setup guidance and shell commands where needed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires QWeather API credentials, may read a local private key, may cache weather responses locally, and sends requested or default city information to QWeather.] <br>

## Skill Version(s): <br>
1.2.2 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
