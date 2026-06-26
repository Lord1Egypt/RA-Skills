## Description: <br>
Query QWeather city codes and real-time weather with bundled executable scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RichLiao1112](https://clawhub.ai/user/RichLiao1112) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and agents use this skill to resolve city names to QWeather location IDs or adcodes and retrieve current weather with a configured QWeather API host and API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a bundled Python script for QWeather lookups. <br>
Mitigation: Install and run it only after reviewing the bundled script and confirming it fits the target environment. <br>
Risk: Using an untrusted QWeather API host or exposing the API key can leak credentials or query data. <br>
Mitigation: Set QWEATHER_API_HOST only to an official or trusted QWeather endpoint, protect QWEATHER_API_KEY, and avoid sharing the key in logs or transcripts. <br>


## Reference(s): <br>
- [QWeather HTTP API Contract](references/qweather-http-contract.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires QWEATHER_API_HOST and QWEATHER_API_KEY; successful script calls return JSON with success: true.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
