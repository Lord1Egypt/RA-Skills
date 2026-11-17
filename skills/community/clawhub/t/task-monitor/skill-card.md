## Description:

Real-time web dashboard for OpenClaw sessions and background tasks. Mobile-responsive with auto-refresh.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jorgermp](https://clawhub.ai/user/jorgermp)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to monitor OpenClaw sessions, Discord activity, sub-agents, and cron jobs from a local web dashboard or JSON status endpoint.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The dashboard can expose OpenClaw activity metadata and prompt-derived task descriptions over an unauthenticated LAN web server.

Mitigation: Bind the server to localhost, add authentication or firewall restrictions, and avoid using the LAN URL on shared or untrusted networks.

Risk: Transcript-derived task descriptions may reveal sensitive user prompts or operational context.

Mitigation: Disable transcript-derived descriptions or review/redact displayed task descriptions before exposing the dashboard.

## Reference(s):

- [Task Monitor on ClawHub](https://clawhub.ai/jorgermp/skills/task-monitor)
- [Publisher profile](https://clawhub.ai/user/jorgermp)
- [OpenClaw Documentation](https://openclaw.org/docs)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, plus JSON from the status API and generated dashboard files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Starts an Express web dashboard on port 3030, polls every 60 seconds, caches session data for 30 seconds, and can generate DASHBOARD.md.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
