## Description: <br>
QVerisAI searches for and executes dynamic external tools through the QVeris API for weather, search, stocks, finance, economics, geolocation, AIGC, news, social media, health data, and other API-backed workflows using QVERIS_API_KEY. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chris7iu](https://clawhub.ai/user/chris7iu) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to discover external API tools by capability and execute selected tools through QVeris for weather, search, finance, economics, geolocation, AIGC, news, social media, and health-data workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tool searches and execution parameters are sent to QVeris and may involve downstream tool providers. <br>
Mitigation: Use a scoped, revocable QVERIS_API_KEY, monitor usage, and avoid sending secrets, personal data, health details, or account-sensitive finance or social data unless QVeris and downstream policies have been reviewed. <br>
Risk: The skill can execute dynamically discovered external tools, so returned data and tool behavior may vary by provider. <br>
Mitigation: Review selected tools before execution, prefer high-confidence providers, and inspect outputs before relying on them in agent workflows. <br>


## Reference(s): <br>
- [ClawHub QVerisAI release page](https://clawhub.ai/chris7iu/qverisai) <br>
- [QVeris API service](https://qveris.ai) <br>
- [QVeris API endpoint](https://qveris.ai/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and optional JSON tool responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search and execution calls require QVERIS_API_KEY; command output may include formatted summaries or raw JSON when --json is used.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
