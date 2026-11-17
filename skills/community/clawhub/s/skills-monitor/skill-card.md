## Description:

Monitors, evaluates, benchmarks, recommends, and reports on AI Skills through a seven-factor scoring engine, cross-model baseline data, dashboards, and diagnostics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jaredwei01](https://clawhub.ai/user/jaredwei01)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to monitor installed AI Skills, run seven-factor evaluations and model benchmarks, compare or recommend skills, and generate operational reports for dashboards or push notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Insecure public-server defaults can expose dashboards, reports, or agent credentials.

Mitigation: Require authentication on overview and dashboard routes, disable debug mode, set a random secret, and bind locally or place the service behind HTTPS.

Risk: Weak agent registration or token handling can allow existing tokens to be overwritten or reused without sufficient authorization.

Mitigation: Require authenticated ownership for registration and key-update flows, then rotate or revoke affected tokens before deployment.

Risk: Telemetry, report uploads, and push notifications can disclose operational data or send it to an under-disclosed webhook destination.

Mitigation: Make realtime telemetry opt-in with consent checks, remove or replace the hardcoded WeCom webhook, and require HTTPS for remote uploads.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jaredwei01/skills/skills-monitor)
- [Artifact skill documentation](artifact/SKILL.md)
- [Deployment guide](artifact/deploy/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance]

**Output Format:** [CLI and agent responses as JSON-like text, Markdown diagnostic reports, and dashboard/server configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local monitoring data, benchmark cache data, report files, dashboard or server processes, and optional remote uploads.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata also contains 0.7.0 and setup.py contains 0.6.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
