## Description: <br>
TencentDB DatabaseClaw Skill helps agents send signed messages to a TencentDB DatabaseClaw instance and process streaming CreateChatCompletion responses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tencent-adm](https://clawhub.ai/user/tencent-adm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to connect an AI workflow to TencentDB DatabaseClaw for database inspection, SQL execution, analysis, and health checks through the supported chat APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Credentials used for TencentCloud API signing could expose database access if mishandled. <br>
Mitigation: Use least-privilege credentials and avoid sharing or logging secret keys. <br>
Risk: Agent-driven SQL or database inspection can affect sensitive or production data. <br>
Mitigation: Prefer non-production or read-only access and require explicit confirmation before destructive, broad, or production queries. <br>
Risk: The skill does not support DatabaseClaw instance lifecycle operations. <br>
Mitigation: Use the DatabaseClaw Console to start, restart, isolate, or recover instances before invoking chat APIs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tencent-adm/tencentdb-databaseclaw-skill) <br>
- [Python Integration Reference](references/python-integration.md) <br>
- [DatabaseClaw Console](https://console.cloud.tencent.com/tdai/claw/instance) <br>
- [TencentCloud TDAI SSE API endpoint](https://tdai.ai.tencentcloudapi.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code snippets and shell commands; the bundled CLI returns plain text responses from SSE streams.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Verbose mode can emit tool calls, reasoning, and diagnostics to stderr; public cloud use requires TencentCloud credentials.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
