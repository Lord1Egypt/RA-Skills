## Description: <br>
Manage Vikunja Kanban boards via API to read, create, move, and complete tasks across predefined buckets with integrated cron sync. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shad0wca7](https://clawhub.ai/user/shad0wca7) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and agent workflows use this skill to inspect and update a Vikunja Kanban board. It supports reading board status, creating tasks, moving tasks between predefined buckets, and completing tasks for heartbeat and email triage workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated API calls are documented by security evidence as insecure and the scripts use TLS verification bypass flags. <br>
Mitigation: Configure a proper CA or remove TLS verification bypass before use, and install only for trusted Vikunja endpoints. <br>
Risk: The documented PostgreSQL permission workaround can bypass normal application permission handling. <br>
Mitigation: Avoid the direct SQL workaround except under a controlled break-glass process; prefer supported Vikunja API and administrative permission flows. <br>
Risk: Long-lived Vikunja API tokens can increase exposure if copied into shared environments or logs. <br>
Mitigation: Use a least-privilege token, keep it in the runtime secret store, rotate it regularly, and avoid committing token values with the skill. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/shad0wca7/vikunja-kanban) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown status summaries and shell command invocations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a trusted Vikunja endpoint, a Vikunja API token, and predefined project, view, and bucket IDs.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
