## Description: <br>
Force agent responses to scheduled/automated messages by using `openclaw agent` instead of `openclaw message send` to trigger actual agent turns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eliranwong](https://clawhub.ai/user/eliranwong) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to make trusted scheduled jobs, monitoring scripts, and automation reliably trigger an agent response and deliver that response back to a chat channel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automation can trigger agent responses and post them into chat channels. <br>
Mitigation: Use the scripts only for trusted automation and restrict which agent IDs and group IDs are allowed. <br>
Risk: Responses or task content may expose confidential information in shared channels. <br>
Mitigation: Avoid sending confidential data to shared chats and review the target channel before delivering responses. <br>
Risk: The scripts execute the OpenClaw binary from OPENCLAW_PATH or a default local path. <br>
Mitigation: Verify the OpenClaw executable path before use. <br>
Risk: Task activity and response snippets may be written to ~/agent_task.log. <br>
Mitigation: Review or clear the log when tasks may involve private information. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/eliranwong/self-prompt) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown with inline bash and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs operational patterns and helper script usage for OpenClaw agents.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
