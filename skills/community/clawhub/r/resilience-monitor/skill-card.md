## Description:

Monitors OpenClaw API and agent-session errors, model health, retry strategies, reporting, dashboard state, and recovery queues through natural-language commands backed by the required Resilience plugin.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leijack-lo](https://clawhub.ai/user/leijack-lo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect OpenClaw LLM API reliability, tune retry behavior, open the monitoring dashboard, and review session or tool recovery status through Chinese natural-language commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release requires installing unaudited external plugin code with OpenClaw unsafe-install protection bypassed.

Mitigation: Install only after reviewing or pinning the plugin release and only when the publisher is trusted.

Risk: The dashboard has unsafe HTML rendering that could expose or alter monitoring data.

Mitigation: Keep the dashboard bound to loopback and avoid exposing it beyond the local machine until the rendering issue is fixed.

Risk: Conversation access is needed for full session recovery behavior.

Mitigation: Enable conversation access only when session recovery is required and review the privacy impact for the workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leijack-lo/skills/resilience-monitor)
- [Publisher profile](https://clawhub.ai/user/leijack-lo)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and natural-language guidance with inline JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on the required external Resilience plugin tools and local dashboard service.]

## Skill Version(s):

0.5.1 (source: server release metadata and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
