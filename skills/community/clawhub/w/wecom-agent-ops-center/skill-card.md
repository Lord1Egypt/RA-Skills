## Description: <br>
企微 AI Agent 可观测性工具 — 心跳监控、进程守护、敏感信息扫描、网络白名单，2 分钟接入 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mikeliang2000](https://clawhub.ai/user/mikeliang2000) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operations teams, and WorkBuddy/OpenClaw users use this skill to monitor AI agent health, forward WeCom messages, receive alerts, scan for sensitive data, and enforce network controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: WeCom bot credentials, local agent inventory, task or audit logs, and process-control capabilities may be exposed to this skill. <br>
Mitigation: Install only in environments where those permissions are acceptable, use least-privilege credentials, and review retained audit or task data before production use. <br>
Risk: Message, admin, HTTP, and P2P endpoints may be reachable without sufficient authentication. <br>
Mitigation: Bind services to localhost or trusted networks and add authentication to HTTP, P2P, and admin endpoints before production deployment. <br>
Risk: External conversion or pairing flows can send operational data outside the local environment. <br>
Mitigation: Verify whether cloud conversion can be disabled for the intended deployment and document any external data flow that remains enabled. <br>
Risk: Deployment and repair scripts can change service paths, permissions, or server configuration. <br>
Mitigation: Review scripts and target paths before running them, especially on shared or production hosts. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/mikeliang2000/wecom-agent-ops-center) <br>
- [Publisher homepage](https://hermesai.ltd) <br>
- [README](artifact/README.md) <br>
- [Architecture notes](artifact/ARCHITECTURE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, YAML configuration, and operational status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WeCom bot credentials and local agent endpoint configuration; may use external conversion and pairing services when enabled.] <br>

## Skill Version(s): <br>
2.4.1 (source: server release metadata; artifact frontmatter and package.json show 2.4.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
