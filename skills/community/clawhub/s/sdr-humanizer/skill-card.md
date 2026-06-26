## Description: <br>
Transforms AI sales messages into natural, paced English conversations with varied tone, timing, and cultural adaptation to build trust and rapport. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ipythoning](https://clawhub.ai/user/ipythoning) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales and customer-facing operators use this skill to rewrite AI-generated SDR outreach into natural English messages, pace replies, and adapt tone to the prospect's region. It also directs the agent to provide a Chinese translation through an internal self-chat for operator reference. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs the agent to hide AI involvement in customer conversations. <br>
Mitigation: Use only where AI-assisted sales outreach is explicitly approved and disclosure practices meet organizational policy and applicable law. <br>
Risk: The skill directs the agent to silently copy translated customer-facing messages into a WhatsApp self-chat. <br>
Mitigation: Remove or disable the self-chat sync unless the data flow is disclosed, approved, logged, and governed by retention and access controls. <br>
Risk: Delayed and human-like delivery behavior can make automated outreach harder for recipients to distinguish from human communication. <br>
Mitigation: Review outbound message policies before deployment and keep operator accountability, audit logging, and opt-out handling in place. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ipythoning/sdr-humanizer) <br>
- [Publisher profile](https://clawhub.ai/user/ipythoning) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [Markdown or plain text conversation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include paced message segments, timing guidance, and internal Chinese translations for operator reference.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
