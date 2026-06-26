## Description: <br>
Tamper-evident audit trail for AI agent decisions. Use when logging LLM decisions, setting up AI compliance, auditing agents for EU AI Act, HIPAA, GDPR or SOC 2, or when a user asks about AI decision audit trails, explainability, or SealVera. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ahessami123](https://clawhub.ai/user/ahessami123) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and compliance teams use SealVera to connect OpenClaw agents to an audit logging service that records decisions, reasoning summaries, inputs, outputs, and status for review. It is intended for AI governance, observability, and compliance workflows in regulated settings such as finance, healthcare, legal, and insurance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan verdict is suspicious because the skill can persistently change agent behavior and send broad task, transcript, reasoning, workspace, and credential-linked data to a remote service. <br>
Mitigation: Install only after confirming the workspace is allowed to transmit that information to SealVera, and review AGENTS.md and SOUL.md after setup. <br>
Risk: Automatic logging and autoload behavior can capture prompts, outputs, model activity, and workspace context beyond a narrow manual audit event. <br>
Mitigation: Use a dedicated API key, scope what is logged, and avoid NODE_OPTIONS autoloading in sensitive projects unless the capture policy is approved. <br>
Risk: Transcript backfill can read completed sub-agent session transcripts and send synthesized records to the remote service. <br>
Mitigation: Do not run subagent-watcher.js unless transcript backfill is explicitly intended and governed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ahessami123/sealvera) <br>
- [Publisher profile](https://clawhub.ai/user/ahessami123) <br>
- [SealVera application](https://app.sealvera.com) <br>
- [SealVera API reference](references/api.md) <br>
- [SealVera compliance mapping](references/compliance.md) <br>
- [SealVera integrations](references/integrations.md) <br>
- [SV-10 standard](https://app.sealvera.com/standard) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JavaScript, Python, JSON, and shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May configure local workspace files and send audit records to SealVera when setup or logging commands are run.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
