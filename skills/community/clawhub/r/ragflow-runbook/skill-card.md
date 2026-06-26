## Description: <br>
End-to-end runbook for deploying, operating, troubleshooting, and monitoring RAGFlow (runtime ops only). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[YitingOU](https://clawhub.ai/user/YitingOU) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operations engineers use this skill to deploy, operate, monitor, and troubleshoot RAGFlow runtime environments. It focuses on Docker-based bring-up, health checks, API readiness checks, smoke tests, backup and restore guidance, and optional alerting workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Docker deployment helpers and upstream downloads can change host services or introduce unreviewed runtime files. <br>
Mitigation: Review upstream Docker files before starting containers, pin a trusted RAGFlow version for production, and use the explicit opt-in controls for downloads and container start. <br>
Risk: API keys, database passwords, or operational details can be exposed through chat, committed files, crontabs, or alert messages. <br>
Mitigation: Keep secrets in environment variables or a secret manager, avoid pasting or committing credentials, and keep alert details free of secrets. <br>
Risk: Scheduled checks and optional Telegram alerts can create recurring external notifications. <br>
Mitigation: Enable cron, launchd, and OpenClaw alerting deliberately, and route alerts only to approved destinations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/YitingOU/ragflow-runbook) <br>
- [RAGFlow documentation](https://ragflow.io/docs/) <br>
- [RAGFlow upstream repository](https://github.com/infiniflow/ragflow) <br>
- [RAGFlow issues](https://github.com/infiniflow/ragflow/issues) <br>
- [Troubleshooting examples](examples/troubleshooting.md) <br>
- [API examples](examples/api-examples.sh) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell, Python, cron, launchd, and API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operational runbook guidance and helper-command proposals; users should review commands before execution.] <br>

## Skill Version(s): <br>
0.1.4 (source: frontmatter, CHANGELOG, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
