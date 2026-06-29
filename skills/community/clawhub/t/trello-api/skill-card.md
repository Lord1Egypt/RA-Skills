## Description: <br>
Trello API integration with managed OAuth for managing boards, lists, cards, checklists, labels, and members through Maton. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent read and update Trello project-management data through a Maton-managed OAuth connection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The connected Trello OAuth account can be used to read and modify boards, lists, cards, labels, and checklists. <br>
Mitigation: Install only if the user trusts Maton to broker Trello OAuth access, and confirm the target resource and intended effect before any create, update, archive, or delete action. <br>
Risk: When multiple Trello connections exist, a request may affect the wrong connected account if the connection is not specified. <br>
Mitigation: Specify the intended Maton connection ID for Trello requests whenever more than one connection is available. <br>


## Reference(s): <br>
- [ClawHub Trello Skill](https://clawhub.ai/byungkyu/skills/trello-api) <br>
- [Trello API Overview](https://developer.atlassian.com/cloud/trello/rest/api-group-actions/) <br>
- [Trello Boards API](https://developer.atlassian.com/cloud/trello/rest/api-group-boards/) <br>
- [Trello Cards API](https://developer.atlassian.com/cloud/trello/rest/api-group-cards/) <br>
- [Maton CLI Manual](https://cli.maton.ai/manual) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell, Python, JavaScript, JSON, and HTTP API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and an active Trello OAuth connection.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
