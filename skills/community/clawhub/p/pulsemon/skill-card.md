## Description:

Monitor cron jobs and background tasks with PulseMon. Check monitor status, create/update/delete monitors, view incidents, and manage alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ramongalego](https://clawhub.ai/user/ramongalego)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to manage PulseMon monitors for cron jobs and background tasks, inspect incidents and pings, and send job status updates through an OpenClaw agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can delete, pause, resume, create, and update PulseMon monitors.

Mitigation: Confirm destructive delete requests and review monitor changes before execution.

Risk: Ping body text is sent to PulseMon and can appear in alerts.

Mitigation: Do not include secrets, credentials, or sensitive personal data in ping body text.

Risk: Authenticated monitor management requires a PulseMon API key.

Mitigation: Install only when the agent should manage PulseMon monitors, and provide PULSEMON_API_KEY through the environment.

## Reference(s):

- [PulseMon](https://pulsemon.dev)
- [PulseMon API settings](https://pulsemon.dev/dashboard/settings)
- [PulseMon API base URL](https://pulsemon.dev/api/v1)
- [PulseMon ping endpoint](https://pulsemon.dev/api/ping/{slug})
- [ClawHub PulseMon skill page](https://clawhub.ai/ramongalego/skills/pulsemon)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Configuration]

**Output Format:** [Markdown responses with JSON API request and response details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PULSEMON_API_KEY for authenticated monitor management; ping endpoints can be sent without an API key.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
