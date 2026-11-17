## Description:

Real-time token consumption monitoring dashboard for OpenClaw agents that tracks per-agent token usage, model cost breakdowns, cache hit rates, cron job status, and 30-day historical trends with prompts redacted by default.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kasparchen](https://clawhub.ai/user/kasparchen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators running OpenClaw agents use this skill to monitor token spend, model cost drivers, cache efficiency, prompt-cost outliers, and cron job health from a local dashboard.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive agent activity can be exposed through the local dashboard, especially if localhost services are proxied or bound beyond loopback.

Mitigation: Keep the service bound to 127.0.0.1, do not set BIND_HOST to a non-loopback address without authentication, and review deployment on shared machines.

Risk: Prompt excerpts may be visible when prompt display is explicitly enabled.

Mitigation: Keep showPrompts disabled unless debugging on a trusted single-user machine; treat session data as sensitive.

Risk: Custom themes and session or cron data can introduce unsafe browser rendering paths.

Mitigation: Use trusted themes, review custom theme HTML before enabling it, and avoid loading untrusted session or cron data into the dashboard.

Risk: Unverified installation sources can change the code that reads local agent data.

Mitigation: Prefer pinned or verified ClawHub installation sources and review the release before installing on shared or sensitive systems.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/kasparchen/skills/token-burn-monitor)
- [OpenClaw](https://openclaw.ai)
- [API Reference](API.md)
- [README](README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance]

**Output Format:** [Markdown setup guidance, shell commands, JSON configuration examples, JSON API responses, and a local HTML dashboard.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs as a zero-dependency Node.js localhost service on port 3847 by default; prompt excerpts remain redacted unless showPrompts is explicitly enabled.]

## Skill Version(s):

5.3.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
