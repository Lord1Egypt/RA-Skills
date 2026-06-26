## Description: <br>
Broadcast a message to multiple OpenClaw group sessions simultaneously. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Zero2Ai-hub](https://clawhub.ai/user/Zero2Ai-hub) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to send coordination messages, alerts, and announcements to multiple OpenClaw Telegram or Discord group sessions through a local gateway. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can broadcast to every configured group, including bundled chat IDs, without a confirmation step. <br>
Mitigation: Replace or clear bundled group IDs, avoid default all-groups targeting, and verify every destination before use. <br>
Risk: Gateway credentials could allow messages to be sent beyond the intended audience. <br>
Mitigation: Use a least-privilege OpenClaw gateway token limited to the intended send destinations. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Zero2Ai-hub/skill-agent-broadcast) <br>
- [Zero2Ai-hub Publisher Profile](https://clawhub.ai/user/Zero2Ai-hub) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Text] <br>
**Output Format:** [Command-line delivery receipts and status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and an OpenClaw gateway with intended send permissions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
