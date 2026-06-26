## Description: <br>
Zadig provides an agent-facing API client for managing Zadig DevOps platform projects, workflows, environments, services, builds, tests, releases, clusters, users, permissions, and logs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lilianzhu](https://clawhub.ai/user/lilianzhu) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and DevOps engineers use this skill to connect an agent to a Zadig instance, inspect CI/CD resources, trigger or approve workflows, manage environments and services, and retrieve platform status or logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a powerful Zadig API token that can affect projects, workflows, deployments, clusters, users, roles, and approvals. <br>
Mitigation: Use a dedicated least-privilege Zadig token, keep it out of version control, and require explicit confirmation before deletes, deployments, approvals, cluster changes, or user and permission changes. <br>
Risk: The service-log helper uses shell execution and may expose the API token while retrieving logs. <br>
Mitigation: Avoid the synchronous service-log helper until it is rewritten without shell execution and without exposing the token. <br>
Risk: The server security verdict is suspicious because the skill combines broad Zadig API access with an unsafe shell command path. <br>
Mitigation: Install only when the publisher is trusted, configure HTTPS-only Zadig endpoints, review requested operations before execution, and scan the skill before deployment. <br>


## Reference(s): <br>
- [Zadig official documentation](https://docs.koderover.com) <br>
- [ClawHub skill page](https://clawhub.ai/lilianzhu/zadig) <br>
- [Publisher profile](https://clawhub.ai/user/lilianzhu) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Text, Shell commands, Guidance] <br>
**Output Format:** [JavaScript API responses, JSON objects, text logs, and Markdown guidance with inline code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ZADIG_API_URL and ZADIG_API_KEY environment variables; optional defaults include ZADIG_DEFAULT_PROJECT and ZADIG_DEFAULT_ENV.] <br>

## Skill Version(s): <br>
4.0.2 (source: server release metadata; artifact package.json and README list 4.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
