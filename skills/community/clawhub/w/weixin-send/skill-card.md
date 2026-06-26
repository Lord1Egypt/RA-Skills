## Description: <br>
Sends proactive text messages to WeChat ClawBot users as a fallback when the openclaw-weixin native message tool is unavailable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luhuiwang](https://clawhub.ai/user/luhuiwang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation operators use this skill to send WeChat text notifications from scripts, cron jobs, or agent sessions when the native OpenClaw messaging tool is not available. It is intended as a fallback path, not the preferred messaging channel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send WeChat messages using local bot credentials outside OpenClaw's normal controls and logs. <br>
Mitigation: Install only when an out-of-band WeChat text-sending fallback is intentionally needed, prefer the native OpenClaw message tool when available, and protect local openclaw-weixin account files. <br>
Risk: Incorrect recipient IDs or unauthorized automation can send unwanted messages. <br>
Mitigation: Verify recipient IDs before sending and avoid unsolicited or automated messages without clear authorization. <br>
Risk: A successful HTTP response does not confirm message delivery. <br>
Mitigation: Treat the send result as API acceptance only and confirm that the recipient has a valid recent context token when delivery matters. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/luhuiwang/weixin-send) <br>
- [OpenClaw project](https://github.com/openclaw/openclaw) <br>
- [WeChat ilink endpoint](https://ilinkai.weixin.qq.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Bash and Python examples; command execution returns JSON status.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Text-only WeChat messages; requires local openclaw-weixin account files and recent context tokens.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
