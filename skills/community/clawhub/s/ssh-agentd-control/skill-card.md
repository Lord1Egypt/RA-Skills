## Description:

Manages and uses a local ssh-agentd setup through systemd service controls, local API calls, and connectivity checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[offlinecat-dev](https://clawhub.ai/user/offlinecat-dev)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to administer a local ssh-agentd service, check systemd state, call health/session/metrics endpoints, and run configured remote commands through the service API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can enable, restart, stop, and inspect a privileged systemd service.

Mitigation: Require explicit user approval before running service-control commands and verify the service status, health endpoint, and session state after configuration changes.

Risk: The skill includes examples for invoking remote commands through the ssh-agentd /run API.

Mitigation: Confirm the target host, command, timeout, and authorization token before invoking mutating or remote-execution API calls.

Risk: Exposing the API beyond localhost or mishandling SSH_AGENTD_TOKEN could allow unauthorized control.

Mitigation: Keep the API bound to localhost unless intentionally changed, protect SSH_AGENTD_TOKEN, and do not store real tokens, passwords, or hosts.yaml in the skill repository.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/offlinecat-dev/skills/ssh-agentd-control)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code]

**Output Format:** [Markdown with inline bash commands and a shell helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses localhost API calls by default and accepts SSH_AGENTD_URL and SSH_AGENTD_TOKEN environment variables.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
