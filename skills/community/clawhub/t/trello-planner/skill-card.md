## Description: <br>
Read-only Trello planner using the official Trello Boards API to inspect boards, cards, members, overdue work, and planning signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tomas-mikula](https://clawhub.ai/user/tomas-mikula) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, project managers, and delivery teams use this skill to review Trello board status, identify overdue cards, and generate planning guidance from read-only Trello API data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Trello token may grant broad read access to boards visible to the authenticated account. <br>
Mitigation: Use a revocable read-only token, scope the connected Trello account carefully, and pass an explicit board_id when possible. <br>
Risk: The skill documentation overstates some analysis features relative to the observed read-only helper behavior. <br>
Mitigation: Treat generated planner insights as review aids and verify prioritization or capacity decisions against Trello before acting. <br>
Risk: Credential exposure would allow unauthorized reads from Trello boards visible to the token. <br>
Mitigation: Keep TRELLO_API_KEY and TRELLO_TOKEN in runtime credential storage, avoid logging them, and rotate the token if exposure is suspected. <br>


## Reference(s): <br>
- [Trello Planner on ClawHub](https://clawhub.ai/tomas-mikula/trello-planner) <br>
- [Atlassian Trello Boards API](https://developer.atlassian.com/cloud/trello/rest/api-group-boards/) <br>
- [Atlassian Trello Actions API](https://developer.atlassian.com/cloud/trello/rest/api-group-actions/) <br>
- [Trello API Key](https://trello.com/app-key) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [Structured JSON status with board metrics, overdue counts, planner insights, and health score] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TRELLO_API_KEY and TRELLO_TOKEN with read access; accepts an optional board_id when provided by the agent runtime.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
