## Description:

Monitors Damai event ticket availability and sold-out status, then alerts on restocks, returned tickets, sellouts, and session or price-tier changes through terminal logs, webhooks, or Windows desktop notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[widoxm](https://clawhub.ai/user/widoxm)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure and run a read-only Node.js monitor for Damai event ticket status changes. It is suited for ticket-availability alerts and debugging raw availability responses, not for purchasing tickets or bypassing platform controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional Damai cookie is a login-session secret if configured.

Mitigation: Store config.json privately, avoid sharing logs or configuration that contain cookies, and rotate the browser session if the cookie is exposed.

Risk: Webhook notifications send alert titles and messages to configured third-party endpoints.

Mitigation: Enable only trusted webhook providers and review notification contents before connecting production endpoints.

Risk: Aggressive polling can trigger platform rate limits, anti-abuse controls, or account risk.

Mitigation: Use the documented 30-60 second polling interval guidance, increase the interval after failures, and run only read-only monitoring.

## Reference(s):

- [ClawHub ticket-monitor Skill Page](https://clawhub.ai/widoxm/skills/ticket-monitor)
- [ClawHub Publisher Profile: widoxm](https://clawhub.ai/user/widoxm)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration JSON, terminal status text, log entries, webhook payloads, and optional JSON snapshots.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces monitoring guidance and runtime outputs; notification delivery depends on user-provided configuration and external provider availability.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
