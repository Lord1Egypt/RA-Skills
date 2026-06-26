## Description: <br>
Controls a local zworker AI automation app over HTTP to list and run tasks, manage schedules, sync OpenClaw user routing information, and fetch notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[peterpan0630](https://clawhub.ai/user/peterpan0630) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and automation operators use this skill to control a locally running zworker instance, including task execution, schedule control, notification retrieval, and user routing synchronization. It is intended for environments where the local zworker app and its automations are trusted. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can route notification content to channels and users. <br>
Mitigation: Prefer explicit channel and userid routing, and avoid notification fallback behavior in shared or multi-user channels. <br>
Risk: The skill can run tasks and enable schedules in the local zworker app. <br>
Mitigation: Install only when the local zworker app is trusted, and periodically review enabled schedules and task behavior. <br>
Risk: The skill depends on a local unauthenticated HTTP service. <br>
Mitigation: Use it only in a trusted local environment and confirm the service listening on localhost:18803 is the intended zworker app. <br>


## Reference(s): <br>
- [Zworker HTTP API endpoints](references/api_endpoints.md) <br>
- [ClawHub skill page](https://clawhub.ai/peterpan0630/zworkeragentskillopenclaw) <br>
- [Publisher profile](https://clawhub.ai/user/peterpan0630) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or JSON-backed command output from local zworker HTTP operations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a trusted local zworker service listening on localhost:18803.] <br>

## Skill Version(s): <br>
1.0.2 (source: release evidence and version.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
