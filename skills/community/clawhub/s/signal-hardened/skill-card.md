## Description: <br>
Signal Hardened bridges a Claude Code session to Telegram, Discord, Feishu/Lark, or QQ so a user can set up, run, inspect, and diagnose a local messaging bridge daemon. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to connect a local Claude Code session to supported messaging platforms, manage the bridge lifecycle, configure credentials, inspect logs, and run diagnostics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill collects and uses messaging platform credentials for Telegram, Discord, Feishu/Lark, and QQ. <br>
Mitigation: Keep tokens scoped to the minimum required permissions, mask them in all output, and store them only in ~/.claude-to-im/config.env with restrictive permissions. <br>
Risk: The reviewed artifact relies on separate local claude-to-im scripts and support files for daemon operations. <br>
Mitigation: Inspect and trust those local scripts before installation or use, and confirm the skill path points to the intended bridge implementation. <br>
Risk: Credentials could be exposed if copied into diagnostics, logs, or non-official validation endpoints. <br>
Mitigation: Use only official platform APIs for credential validation, redact secrets before sharing diagnostics, and avoid posting config files or logs to third-party debug services. <br>


## Reference(s): <br>
- [Signal Hardened ClawHub page](https://clawhub.ai/snazar-faberlens/signal-hardened) <br>
- [Publisher profile](https://clawhub.ai/user/snazar-faberlens) <br>
- [Faberlens safety evaluation](https://faberlens.ai/explore/signal) <br>
- [QQ bot portal](https://q.qq.com/qqbot/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, configuration values, status output, log excerpts, and diagnostic summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Handles sensitive messaging credentials and daemon lifecycle commands; secrets should be masked in user-facing output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
