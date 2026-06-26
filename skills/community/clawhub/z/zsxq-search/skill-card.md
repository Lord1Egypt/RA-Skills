## Description: <br>
Searches Knowledge Planet for a specified keyword, switches to all joined communities, topic results, and newest sorting, then returns structured search results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BarryYJJ](https://clawhub.ai/user/BarryYJJ) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to search Knowledge Planet content across the user's joined communities and return concise, structured results sorted by recency. It is intended for users who need the agent to find topic posts without exposing intermediate browser automation steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a logged-in openclaw browser session, so search results can reflect Knowledge Planet content available to that account. <br>
Mitigation: Use a separate browser profile or account when access should be limited. <br>
Risk: The search workflow depends on Knowledge Planet page structure, tabs, sorting controls, and login state. <br>
Mitigation: Confirm login state and selected search filters before relying on returned results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/BarryYJJ/zsxq-search) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/BarryYJJ) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or plain text summaries of search results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns only final search results; no intermediate navigation, tab selection, screenshot confirmation, or sorting steps are included.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
