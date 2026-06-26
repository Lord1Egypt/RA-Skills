## Description: <br>
TencentCloud Websocket Checker helps diagnose WebSocket connection latency by measuring DNS lookup, TCP handshake, TLS handshake, and WebSocket Upgrade timing for ws and wss endpoints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jizhouli](https://clawhub.ai/user/jizhouli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use this skill to test WebSocket endpoint connection setup time, compare ws and wss behavior, generate CSV or JSON timing reports, and troubleshoot slow DNS, TCP, TLS, or WebSocket Upgrade stages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dependency installation may use privileged setup steps. <br>
Mitigation: Review installation scripts before running them with sudo and prefer trusted OS package-manager commands for required tools. <br>
Risk: WebSocket timing checks generate network probes against target endpoints. <br>
Mitigation: Run checks only against endpoints you control or are authorized to test. <br>
Risk: Cron examples can create persistent monitoring jobs. <br>
Mitigation: Track and remove scheduled checks when diagnostics are complete. <br>


## Reference(s): <br>
- [Examples Reference](artifact/references/examples.md) <br>
- [Troubleshooting Reference](artifact/references/troubleshooting.md) <br>
- [Usage Examples](artifact/docs/EXAMPLES.md) <br>
- [Troubleshooting Guide](artifact/docs/TROUBLESHOOTING.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/jizhouli/tencentcloud-websocket-checker) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and optional CSV or JSON reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports can include multi-round timing summaries, bottleneck analysis, performance ratings, and ASCII timing diagrams.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
