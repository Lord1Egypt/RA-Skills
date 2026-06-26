## Description: <br>
This skill helps users extract structured video list data and comment data from YouTube using the BrowserAct API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ccmagia2-gif](https://clawhub.ai/user/ccmagia2-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and research teams use this skill to collect YouTube video metadata and public comment data for audience insight, market research, topic tracking, and sentiment analysis workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends YouTube search and comment-collection requests to BrowserAct using a BrowserAct API key. <br>
Mitigation: Install only when BrowserAct use is intended, provide BROWSERACT_API_KEY through an environment variable or secret manager, and expect BrowserAct quota and network usage when the skill runs. <br>
Risk: Search terms and collected public comment data may be sent to or processed by BrowserAct and may be subject to platform terms. <br>
Mitigation: Avoid sensitive search terms, review BrowserAct and YouTube terms before use, and handle collected public data according to the user's policy requirements. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ccmagia2-gif/youtube-comments-api-skill) <br>
- [BrowserAct integrations console](https://www.browseract.com/reception/integrations) <br>
- [BrowserAct workflow API endpoint](https://api.browseract.com/v2/workflow) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal logs followed by structured YouTube video and comment data returned by the BrowserAct workflow] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python and BROWSERACT_API_KEY; accepts keywords, per-video comment limit, and comment scroll count.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
