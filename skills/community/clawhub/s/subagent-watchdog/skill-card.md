## Description: <br>
Watchdog for OpenClaw subagent runs: enforce a completion marker by deadline and alert if missing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gleb-urvanov](https://clawhub.ai/user/gleb-urvanov) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to monitor subagent tasks that must create completion marker files before a deadline, with optional alerting when the marker is missing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Timeout alerts may include the subagent label. <br>
Mitigation: Avoid sensitive task names or identifiers in labels. <br>
Risk: Optional notifications can be sent to the wrong destination if channel settings are misconfigured. <br>
Mitigation: Set WATCHDOG_CHAT_ID and WATCHDOG_CHANNEL only to intended destinations before enabling notifications. <br>
Risk: The default timer reads local OpenClaw configuration when wait_seconds is omitted. <br>
Mitigation: Pass an explicit wait_seconds value or verify OPENCLAW_CONFIG_PATH or ~/.openclaw/openclaw.json before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gleb-urvanov/subagent-watchdog) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes a local watchdog shell script, a marker-file contract, and optional OpenClaw notification setup.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
