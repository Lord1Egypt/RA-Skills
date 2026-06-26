## Description: <br>
Turns an AI agent into a telecom operator for bulk calling, ChatOps, field monitoring, approvals, and call memory retrieval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kflohr](https://clawhub.ai/user/kflohr) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External operations teams and developers use this skill to let an agent create and monitor telecom campaigns, place calls, manage approvals, and retrieve call transcripts through a telecom console. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad calling and campaign authority can place high-volume calls, affect real phone numbers, or incur telecom charges. <br>
Mitigation: Use a limited Twilio account or subaccount, verified opt-in call lists, explicit campaign approvals, spend limits, and rate limits. <br>
Risk: Call recordings and transcripts can expose sensitive personal data. <br>
Mitigation: Require clear recording consent policies, restrict transcript access, and define retention and deletion procedures before deployment. <br>
Risk: Remote Telegram administration can approve high-risk actions if access is not tightly controlled. <br>
Mitigation: Restrict Telegram access to authorized users, require approvals for high-risk actions, and monitor administrative activity. <br>
Risk: The security review notes broad telecom, recording, transcript, and account authority without enough documented limits or privacy controls. <br>
Mitigation: Review the implementation before installing and use only with a trusted operator console and documented operational policies. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kflohr/telecom-agent-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Text, Guidance] <br>
**Output Format:** [Markdown guidance with CLI command examples; runtime results may include JSON status reports and transcript text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce campaign identifiers, call status, recording references, and transcript content.] <br>

## Skill Version(s): <br>
0.1.5 (source: ClawHub release) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
