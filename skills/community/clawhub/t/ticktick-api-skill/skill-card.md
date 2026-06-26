## Description: <br>
TickTick API integration with managed OAuth for managing tasks, projects, and task lists. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect an agent to TickTick through Maton-managed OAuth so it can list, create, update, complete, delete, and organize tasks and projects with user approval for write actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Maton API key and TickTick OAuth connection that can access task and project data. <br>
Mitigation: Keep MATON_API_KEY private, install only if Maton is trusted for the connected account, and revoke the key or delete the connection when it is no longer needed. <br>
Risk: Write operations can create, update, complete, or delete TickTick tasks and projects. <br>
Mitigation: Confirm the exact target resource and intended effect with the user before approving any write action. <br>


## Reference(s): <br>
- [TickTick Skill on ClawHub](https://clawhub.ai/byungkyu/ticktick-api-skill) <br>
- [TickTick Developer Portal](https://developer.ticktick.com/) <br>
- [TickTick Help Center](https://help.ticktick.com/) <br>
- [Maton](https://maton.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, API calls, Configuration] <br>
**Output Format:** [Markdown with inline Python, JavaScript, HTTP, and shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, a MATON_API_KEY, and a connected TickTick OAuth account.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
