## Description: <br>
Provides a complete AI agent observability solution with structured logs, metrics, distributed tracing, alert management, and a real-time monitoring dashboard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuyonghao-123](https://clawhub.ai/user/yuyonghao-123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add observability to AI agents, including structured logging, metrics, tracing, alerting, and a local monitoring dashboard for LLM, MCP, and A2A activity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local dashboard exposes telemetry APIs and recent logs without built-in authentication. <br>
Mitigation: Bind it to localhost or place it behind access control before using it with sensitive agent telemetry. <br>
Risk: Logs and trace metadata can persist prompts, tokens, payload details, or other sensitive operational data. <br>
Mitigation: Disable file or debug logging when handling secrets, and avoid sending prompts, tokens, or raw payloads into trace metadata. <br>
Risk: Webhook alerting can send observability data to external endpoints. <br>
Mitigation: Configure webhook notifications only for trusted destinations and review the alert payloads before enabling them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yuyonghao-123/yuyonghao-observability) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JavaScript and shell command examples; runtime telemetry is emitted as logs, metrics, traces, dashboard views, and JSON or Prometheus API responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The dashboard defaults to a local HTTP service and log files unless configured otherwise.] <br>

## Skill Version(s): <br>
0.1.1 (source: release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
