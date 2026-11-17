## Description:

Provides a complete AI agent observability solution with structured logs, metrics, distributed tracing, alert management, and a real-time monitoring dashboard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuyonghao-123](https://clawhub.ai/user/yuyonghao-123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add structured logs, metrics, traces, alerting, and dashboard visibility to AI agent systems. It is suited for monitoring LLM calls, MCP tool activity, A2A messages, latency, errors, and operational health.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The dashboard and logs can expose sensitive operational telemetry, prompts, tool payloads, or agent activity.

Mitigation: Treat logs and dashboard output as sensitive, avoid logging secrets or raw prompts/tool payloads, and add redaction before use with real agent traffic.

Risk: Dashboard endpoints can expose monitoring data if reachable by untrusted users.

Mitigation: Run the dashboard on loopback or behind authentication and network access controls.

Risk: Webhook alerting can send telemetry to external destinations.

Mitigation: Disable webhooks by default or restrict them to trusted HTTPS endpoints.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yuyonghao-123/skills/yuyonghao-observability)
- [SKILL.md](SKILL.md)
- [README.md](README.md)
- [package.json](package.json)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript examples, shell commands, runtime logs, metrics, traces, alerts, dashboard views, and JSON or Prometheus API output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 18 or newer and the Winston dependency declared by the package.]

## Skill Version(s):

0.1.1 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
