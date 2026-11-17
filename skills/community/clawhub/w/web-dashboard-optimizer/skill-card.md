## Description:

Create smooth, stable web monitoring dashboards with smart refresh, scroll position retention, modal interaction, auto-restart, and responsive design.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zqh07-bit](https://clawhub.ai/user/zqh07-bit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use this skill to build task-monitoring, data-visualization, real-time status, system monitoring, and admin dashboards with stable refresh behavior and improved modal interactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The sample server can expose monitoring data, especially if bound beyond localhost or used with permissive CORS.

Mitigation: Bind the server to 127.0.0.1 unless intentionally exposing it, remove wildcard CORS, and add authentication before using real monitoring data.

Risk: Dashboard examples use dynamic HTML insertion for rendered data and modal content.

Mitigation: Avoid innerHTML for untrusted content; use safe DOM APIs, textContent, or a reviewed sanitizer.

Risk: The helper scripts keep a local service running and document a kill -9 port command.

Mitigation: Use a private runtime directory and verify the exact target process before stopping any process.

## Reference(s):

- [Web Dashboard Optimizer on ClawHub](https://clawhub.ai/zqh07-bit/skills/web-dashboard-optimizer)
- [Publisher profile: zqh07-bit](https://clawhub.ai/user/zqh07-bit)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with HTML, CSS, JavaScript, Node.js, and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces dashboard templates, server examples, restart scripts, customization guidance, and troubleshooting steps.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
