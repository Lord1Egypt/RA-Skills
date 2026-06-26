## Description: <br>
Weather information lookup tool covering Chinese cities and counties for current weather and forecast requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tencentnewsteam](https://clawhub.ai/user/tencentnewsteam) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer current-weather and forecast questions for Chinese city, district, and county locations through Tencent weather data. It helps choose the appropriate CLI weather command, request missing location details when needed, and format returned weather fields for the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and runs a persistent external Tencent News CLI from Tencent-hosted installer scripts. <br>
Mitigation: Install only when the publisher and installer are trusted, and prefer downloading and verifying installer scripts before execution. <br>
Risk: The skill may use or change a locally stored Tencent News API key. <br>
Mitigation: Let users provide and manage the API key explicitly, avoid exposing the key in responses, and clear it only when the user asks. <br>
Risk: The installed CLI has broader persistent capabilities than weather lookup alone. <br>
Mitigation: Route weather work through the bundled state and run scripts, review the CLI state before use, and stop on CLI failures instead of falling back to another data source. <br>


## Reference(s): <br>
- [tencent-weather ClawHub listing](https://clawhub.ai/tencentnewsteam/tencent-weather) <br>
- [tencent-news-cli manual installation guide](references/installation-guide.md) <br>
- [tencent-news-cli manual update guide](references/update-guide.md) <br>
- [tencent-news-cli API Key configuration guide](references/env-setup-guide.md) <br>
- [Tencent News API Key page](https://news.qq.com/exchange?scene=appkey) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown or readable text, with shell commands for setup and CLI execution when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Weather answers preserve Tencent weather as the source and omit fields not returned by the CLI.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
