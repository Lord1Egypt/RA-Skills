## Description: <br>
OpenClaw Dashboard monitors active OpenClaw agent sessions, token usage, system status, and can format status summaries for Feishu or a local dashboard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[youhaveamydream-spec](https://clawhub.ai/user/youhaveamydream-spec) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to inspect multi-agent session activity, token consumption, and runtime metadata, and to share status summaries in Feishu when appropriate. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Feishu status cards may expose session names, token usage, node/system details, channel, model, and runtime metadata to chat participants. <br>
Mitigation: Use /status-card only in Feishu conversations approved to receive operational metadata. <br>
Risk: The skill runs the local OpenClaw status command to collect runtime information. <br>
Mitigation: Install and run it only where the local OpenClaw CLI is trusted and expected to disclose status output. <br>
Risk: The optional browser dashboard loads third-party assets. <br>
Mitigation: Treat dashboard.html as networked content and review or allowlist external browser assets before use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/youhaveamydream-spec/xc-openclaw-dashboard) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill overview](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, configuration] <br>
**Output Format:** [Markdown-like status text, Feishu interactive card JSON, and optional browser dashboard configuration.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Status summaries may include session names, token usage, node details, channel, model, runtime metadata, and timestamps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
