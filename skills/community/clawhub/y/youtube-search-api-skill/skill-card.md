## Description: <br>
This skill helps agents search YouTube through BrowserAct and return structured result data for videos, Shorts, channels, and playlists. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ccmagia2-gif](https://clawhub.ai/user/ccmagia2-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and market analysts use this skill to collect structured YouTube search results for topic discovery, competitor scanning, trend monitoring, channel research, tutorial aggregation, and creator outreach. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: YouTube search queries are sent to BrowserAct and may reveal sensitive research topics. <br>
Mitigation: Review queries before execution and avoid submitting confidential or regulated terms unless BrowserAct is approved for that use. <br>
Risk: The skill requires a BrowserAct API key. <br>
Mitigation: Provide BROWSERACT_API_KEY through an environment variable or secrets manager and avoid pasting secrets into chat. <br>
Risk: The workflow depends on BrowserAct service availability and authorization. <br>
Mitigation: If authorization fails, stop and refresh the API key; retry non-authorization failures at most once as described by the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ccmagia2-gif/youtube-search-api-skill) <br>
- [BrowserAct Console integrations](https://www.browseract.com/reception/integrations) <br>
- [BrowserAct workflow API endpoint](https://api.browseract.com/v2/workflow) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal status logs followed by structured YouTube search result text or JSON from the BrowserAct workflow response.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python and BROWSERACT_API_KEY. The script accepts search keywords, result type, and result limit, then polls BrowserAct until completion.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
