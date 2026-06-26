## Description: <br>
Windows desktop WeChat message automation skill that uses keyboard simulation to send messages to specified contacts or groups with the wt shortcut. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangpuego123](https://clawhub.ai/user/zhangpuego123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and operators with WeChat for Windows installed and logged in use this skill to send one-off or batch messages to named contacts or groups from an agent-controlled desktop session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send real WeChat messages from the user's logged-in desktop session with limited safeguards. <br>
Mitigation: Install only from trusted publishers, watch the WeChat window during use, test with harmless contacts first, and add manual confirmation before live sends when possible. <br>
Risk: Interrupted batch sends may leave queued contact and message content in local state. <br>
Mitigation: Delete send_queue.json after interrupted batches and avoid sensitive batch content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhangpuego123/wechat-talk) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/zhangpuego123) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text status messages and CLI or MCP tool responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Batch sends can create a local send_queue.json state file until the queue completes or is cleared.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
