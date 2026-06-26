## Description: <br>
Real-time security monitor for AI agents. Watches every tool call, flags threats, and alerts you before damage is done. Works with OpenClaw and Claude Code. Free, open source. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wow-leeroy-jenkins05](https://clawhub.ai/user/wow-leeroy-jenkins05) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Shoofly Basic to monitor OpenClaw or Claude Code tool activity for prompt injection, tool response injection, out-of-scope writes, runaway loops, and data exfiltration signals. It logs evaluations and sends alerts, but does not block tool calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persistently records tool activity and security evaluations in ~/.shoofly/logs/alerts.log. <br>
Mitigation: Protect the log directory, avoid placing secrets in alert summaries, and periodically delete or rotate the log file. <br>
Risk: Alert text may be sent to configured messaging channels or local notification systems. <br>
Mitigation: Enable only notification channels you control and review channel configuration before using the skill. <br>
Risk: Shoofly Basic alerts on suspicious behavior but does not block tool calls. <br>
Mitigation: Treat alerts as review signals and keep normal approval controls in place for sensitive tool use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wow-leeroy-jenkins05/shoofly-basic) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions, JSONL log records, terminal messages, desktop notifications, and optional messaging-channel alerts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires jq and curl; alert text is truncated to 500 characters by the bundled notifier.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
