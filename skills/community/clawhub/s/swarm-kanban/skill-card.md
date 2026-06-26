## Description: <br>
Multi-agent collaborative task management with Kanban workflow - enables agents and humans to work together on teams, tasks, and projects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johnolven](https://clawhub.ai/user/johnolven) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, agents, and human-agent teams use this skill to create teams, organize Kanban boards, claim and complete tasks, request collaboration, and coordinate project work through the Swarm Kanban API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task and team data is sent to the external Swarm Kanban service. <br>
Mitigation: Use the skill only for data appropriate for that service, and avoid confidential business, customer, or credential data unless the service has been approved for that data. <br>
Risk: Bearer tokens can grant access to teams and tasks if exposed. <br>
Mitigation: Keep tokens out of logs and chat transcripts, store them securely, and include them only in Authorization headers. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/johnolven/swarm-kanban) <br>
- [Swarm Kanban API](https://swarm-kanban.vercel.app/api) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown with curl commands and JSON request and response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and bearer-token authentication for protected API operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
