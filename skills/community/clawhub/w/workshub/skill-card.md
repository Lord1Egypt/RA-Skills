## Description: <br>
WorksHub is an MCP skill that lets an agent use the WorksHub platform to browse workers, post bounty tasks, communicate with workers, and manage task workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nylk](https://clawhub.ai/user/nylk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can connect an agent to WorksHub to search for human workers, create and manage bounty tasks, and exchange task-related messages through a configured WorksHub account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a WorksHub account to create paid tasks, accept workers, cancel tasks, and send messages. <br>
Mitigation: Require manual approval before posting bounties, accepting applicants, canceling tasks, sending messages, or sharing sensitive task details. <br>
Risk: The WORKSHUB_API_KEY and optional WORKSHUB_API_URL environment variables control account access and endpoint selection. <br>
Mitigation: Use a dedicated revocable API key, protect it as a secret, and keep WORKSHUB_API_URL unset unless the endpoint is fully trusted. <br>


## Reference(s): <br>
- [ClawHub WorksHub skill page](https://clawhub.ai/nylk/workshub) <br>
- [WorksHub MCP endpoint](https://www.workshub.ai/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Text] <br>
**Output Format:** [JSON responses and command-line status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and a WorksHub API key for authenticated tools; WORKSHUB_API_URL can override the default endpoint.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
