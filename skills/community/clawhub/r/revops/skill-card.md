## Description: <br>
Enables an agent to create and use a SendClaw email address for limited, task-oriented professional communication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codejika](https://clawhub.ai/user/codejika) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent builders use this skill to give an agent a SendClaw mailbox for sending, receiving, replying to, and checking email under explicit human communication rules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill lets an agent send real external email from a SendClaw mailbox. <br>
Mitigation: Set explicit human rules for when the agent may send or reply, and require review for sensitive or first-time messages. <br>
Risk: The SendClaw API key represents the agent email identity. <br>
Mitigation: Store SENDCLAW_API_KEY in a secrets manager and only send it to SendClaw API endpoints. <br>
Risk: Webhook notifications can expose mailbox activity if pointed at an endpoint outside the user's control. <br>
Mitigation: Configure webhooks only to endpoints the user controls, or leave webhook notifications disabled. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/codejika/revops) <br>
- [Publisher profile](https://clawhub.ai/user/codejika) <br>
- [SendClaw homepage](https://sendclaw.com) <br>
- [SendClaw API base](https://sendclaw.com/api) <br>
- [SendClaw skill documentation](https://sendclaw.com/skill.md) <br>
- [SendClaw heartbeat documentation](https://sendclaw.com/heartbeat.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls, markdown] <br>
**Output Format:** [Markdown with HTTP and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SENDCLAW_API_KEY for authenticated SendClaw API use.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter reports 1.7.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
