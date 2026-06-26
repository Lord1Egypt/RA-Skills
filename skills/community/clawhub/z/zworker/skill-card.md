## Description: <br>
Zworker lets an agent control a local Zworker automation app to list and run tasks, manage schedules, sync user identifiers, and retrieve notifications through a localhost HTTP API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[peterpan0630](https://clawhub.ai/user/peterpan0630) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation operators use this skill to connect an agent to a locally running Zworker app for task execution, schedule control, user information synchronization, and notification forwarding. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can collect and synchronize user identifiers and route notifications. <br>
Mitigation: Restrict user-ID collection to approved OpenClaw sources, require explicit confirmation before synchronization or forwarding, and block notification sending when userid is missing. <br>
Risk: The skill can execute tasks and change schedules through an unauthenticated local API. <br>
Mitigation: Install only when the local Zworker app is trusted, keep the service bound to the local environment, and require explicit confirmation before task execution or schedule changes. <br>


## Reference(s): <br>
- [Zworker HTTP API endpoints](references/api_endpoints.md) <br>
- [ClawHub Zworker skill page](https://clawhub.ai/peterpan0630/zworker) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown or JSON responses with command-line status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include task and schedule lists, success or failure messages, notification payloads, and user synchronization results.] <br>

## Skill Version(s): <br>
1.0.3 (source: release evidence and version.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
