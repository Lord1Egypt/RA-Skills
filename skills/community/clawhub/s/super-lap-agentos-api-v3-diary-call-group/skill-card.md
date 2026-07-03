## Description: <br>
Guides agents in using agentOS API V3 Diary Call Group endpoints for diary search, appointment scheduling, updates, cancellation, feedback, branch lookup, allocations, and recurring appointment workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[molexazwo](https://clawhub.ai/user/molexazwo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to help an agent choose agentOS diary endpoints, authenticate with an API key, and prepare diary management requests for scheduling, branch, allocation, feedback, and recurring appointment tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide requests that create, update, delete, or cancel live diary appointments. <br>
Mitigation: Use a least-privilege API key, verify tenant, branch, and appointment identifiers, and require explicit approval before write operations. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/molexazwo/skills/super-lap-agentos-api-v3-diary-call-group) <br>
- [LAP](https://lap.sh) <br>
- [agentOS API Base URL](https://live-api.letmc.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with endpoint tables, setup steps, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AGENTOS_API_V3_DIARY_CALL_GROUP_API_KEY for live API use; write operations should require explicit approval.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
