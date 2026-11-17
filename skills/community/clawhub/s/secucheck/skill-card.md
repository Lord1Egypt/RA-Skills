## Description:

Secucheck audits OpenClaw configurations, permissions, runtime exposure, sessions, skills, cron jobs, agents, channels, and network posture with localized reports and a dashboard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jooneyp](https://clawhub.ai/user/jooneyp)

### License/Terms of Use:

MIT

## Use Case:

Developers, operators, and OpenClaw administrators use this skill to review an OpenClaw deployment's security posture, identify configuration and runtime risks, and receive prioritized remediation guidance. It supports routine reviews after skill installation, agent changes, cron changes, or a requested full audit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dashboard serving can expose the OpenClaw workspace over the local network and leave a background web server running.

Mitigation: Avoid dashboard mode on shared, office, VPN, or untrusted networks unless it binds to localhost, serves only the report file, and stops automatically.

Risk: Declared gateway and cron capabilities increase the permission surface when they are not needed for normal audit output.

Mitigation: Remove unused gateway and cron capabilities before release, or document why each capability is required.

Risk: Public-IP checks can contact external services during runtime audits.

Mitigation: Make public-IP checks opt-in and explain the external request before running them.

Risk: Dashboard report data may be rendered into HTML.

Mitigation: HTML-escape report data before inserting it into dashboard templates.

## Reference(s):

- [Secucheck ClawHub Listing](https://clawhub.ai/jooneyp/skills/secucheck)
- [Secucheck README](artifact/README.md)
- [Runtime Security Checks](artifact/checks/runtime.md)
- [Network Security Checks](artifact/checks/network.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report with JSON audit data and optional HTML dashboard]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Localized to the user's language; dashboard mode writes an HTML report and can start a background HTTP server.]

## Skill Version(s):

2.8.0 (source: server release evidence and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
