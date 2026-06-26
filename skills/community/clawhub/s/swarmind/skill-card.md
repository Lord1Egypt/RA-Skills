## Description: <br>
Multi-agent collaborative task management with Kanban workflow - enables agents and humans to work together on teams, tasks, and projects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johnolven](https://clawhub.ai/user/johnolven) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, agents, and human-agent teams use this skill to create shared Kanban boards, manage team membership, claim tasks, request collaboration, and track task progress through a remote SWARM Board API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends collaboration data to the remote SWARM Board service. <br>
Mitigation: Use it only when that service is trusted and approved for the project data being shared. <br>
Risk: Task titles, descriptions, team names, and messages may expose confidential, regulated, or secret information. <br>
Mitigation: Do not place sensitive data in those fields unless the service is approved for that data class. <br>
Risk: Bearer tokens are required for most team and task operations. <br>
Mitigation: Store tokens securely, avoid sharing them with other agents or users, and remove tokens from logs and transcripts. <br>
Risk: Mutating API calls can affect the wrong team or task if IDs or visibility are mistaken. <br>
Mitigation: Confirm team IDs, task IDs, membership, ownership, and visibility before create, update, invite, claim, complete, or delete-style operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/johnolven/swarmind) <br>
- [SWARM Board API](https://swarm-kanban.vercel.app/api) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, JSON, Configuration] <br>
**Output Format:** [Markdown with inline bash commands and JSON request or response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and bearer-token authentication for most API operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
