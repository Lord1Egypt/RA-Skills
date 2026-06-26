## Description: <br>
Universal operational digest for agent skill stacks: scheduled skills append outcomes to a local log, Pulse Board summarizes the log through the configured OpenClaw agent when available, delivers the digest to Telegram, Discord, or a local log, and falls back to a mechanical summary if agent composition fails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LittleJakub](https://clawhub.ai/user/LittleJakub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use Pulse Board to turn scheduled skill and cron-job outcomes into concise operational digests. It is intended for agent skill stacks that need local logging, scheduled summaries, and optional delivery to Telegram, Discord, or a local file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cron job output stored in Pulse Board logs may contain sensitive operational data. <br>
Mitigation: Avoid logging secrets from wrapped jobs, review local log contents, and restrict access to ~/.pulse-board. <br>
Risk: When LLM composition is enabled, raw log content is sent to the configured OpenClaw agent and may leave the host if that agent uses a remote provider. <br>
Mitigation: Use a local-only agent for sensitive environments and review agent configuration before enabling digest composition. <br>
Risk: Telegram bot tokens, Discord webhooks, and related configuration grant delivery access if exposed. <br>
Mitigation: Protect pulse.yaml and any secrets env file, prefer environment-based secret storage, and rotate tokens or webhooks after exposure. <br>
Risk: The installer and plug scripts modify the user crontab. <br>
Mitigation: Review the prompted crontab changes before confirming installation or plugging jobs, and use unplug.sh to remove registered entries. <br>


## Reference(s): <br>
- [Pulse Board ClawHub page](https://clawhub.ai/LittleJakub/pulse-board) <br>
- [Publisher profile](https://clawhub.ai/user/LittleJakub) <br>
- [CHANGELOG.md](CHANGELOG.md) <br>
- [_meta.json](_meta.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Plain text and Markdown digests, plus shell-driven cron and configuration updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local log files and optional Telegram or Discord messages from cron outcome logs.] <br>

## Skill Version(s): <br>
1.1.3 (source: server release evidence, _meta.json, CHANGELOG.md released 2026-03-09) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
