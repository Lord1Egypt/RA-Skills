## Description: <br>
Xiangshan Douyin helps agents search Douyin users and videos and retrieve user profiles, video details, comments, and playback statistics through the XSData API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jesuslove](https://clawhub.ai/user/jesuslove) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query Douyin account, video, comment, and engagement data from user-provided links, IDs, or search terms. It guides the agent to select the relevant XSData endpoint, supply the required API key, parse the response, and present the requested fields clearly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user-provided Douyin links, IDs, search terms, and an XSData API key to api.xsdata.top. <br>
Mitigation: Use the skill only if the XSData service is trusted, store XS_API_KEY in an environment variable when possible, and avoid pasting secrets into chat. <br>
Risk: API calls may consume paid XSData credits. <br>
Mitigation: Confirm the intended query before calling an endpoint and remind users when an operation may spend credits. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jesuslove/xiangshan-douyin) <br>
- [XSData API base URL](https://api.xsdata.top) <br>
- [Search Douyin users](reference/search-user.md) <br>
- [Search Douyin videos](reference/search-video.md) <br>
- [Fetch Douyin user data](reference/user-data.md) <br>
- [Fetch Douyin user video list](reference/user-video-list.md) <br>
- [Fetch Douyin video comments](reference/video-comment.md) <br>
- [Fetch Douyin video details](reference/video-detail.md) <br>
- [Fetch Douyin video statistics](reference/video-statistics.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown summaries with optional curl commands and parsed API response fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include paginated result summaries, tables of selected Douyin fields, and reminders that API calls consume XSData credits.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
