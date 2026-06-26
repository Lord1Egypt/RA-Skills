## Description: <br>
Trello API integration with managed OAuth for managing boards, lists, cards, members, labels, and related project-management resources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agent users use this skill to read and manage Trello project data through Maton-managed OAuth. It supports common board, list, card, checklist, label, member, connection, and search workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: MATON_API_KEY is a sensitive credential used to access managed Trello connections. <br>
Mitigation: Store MATON_API_KEY in a secret manager or protected environment variable, avoid logging it, and rotate it if exposed. <br>
Risk: Create, update, archive, and delete operations can modify Trello project data. <br>
Mitigation: Confirm the target board, list, card, checklist, label, or member and the intended effect with the user before running write operations. <br>
Risk: Multiple Trello connections may route requests to the wrong account or workspace. <br>
Mitigation: Specify the intended Maton connection when more than one Trello connection exists and verify the active account before making changes. <br>


## Reference(s): <br>
- [ClawHub Trello Skill Page](https://clawhub.ai/byungkyu/trello-api) <br>
- [Trello REST API Overview](https://developer.atlassian.com/cloud/trello/rest/api-group-actions/) <br>
- [Trello Boards API](https://developer.atlassian.com/cloud/trello/rest/api-group-boards/) <br>
- [Trello Cards API](https://developer.atlassian.com/cloud/trello/rest/api-group-cards/) <br>
- [Maton CLI Manual](https://cli.maton.ai/manual) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, HTTP paths, and code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and a valid Trello OAuth connection through Maton.] <br>

## Skill Version(s): <br>
1.0.5 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
