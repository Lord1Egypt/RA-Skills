## Description: <br>
Manage tasks, projects, and notes in tududi (self-hosted task manager). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chrisvel](https://clawhub.ai/user/chrisvel) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and personal productivity users use this skill to let an agent manage tududi tasks, projects, inbox items, and tags through the configured tududi API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends requests to a user-configured tududi server using an API token. <br>
Mitigation: Confirm the configured TUDUDI_URL is trusted and use the least-privilege API token available. <br>
Risk: Delete operations can remove task or inbox items by UID. <br>
Mitigation: Ask the agent to list or fetch the item first and repeat the exact UID before proceeding. <br>


## Reference(s): <br>
- [ClawHub tududi skill page](https://clawhub.ai/chrisvel/tududi) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown with curl examples and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a configured tududi server URL and API token; destructive operations should be confirmed against the exact UID before execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
