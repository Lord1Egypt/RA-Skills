## Description: <br>
Manages WhatsApp whitelists so agents can send messages only to approved numbers, track delivery status, and verify OpenClaw WhatsApp connectivity through word-trigger commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Santanu-Kumar-prusty](https://clawhub.ai/user/Santanu-Kumar-prusty) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage approved WhatsApp recipient sets, send text or media messages through a connected OpenClaw account, and check message status by ID. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: WhatsApp messages are sent from the user's connected OpenClaw account and may reach unintended recipients if whitelist sets are stale or too broad. <br>
Mitigation: Keep whitelist sets small and reviewed, verify the target set before sending, and confirm WhatsApp connectivity before message actions. <br>
Risk: Local whitelist and message-store files can contain sensitive phone numbers and message metadata. <br>
Mitigation: Use the skill only from a trusted, non-shared workspace and protect or delete the local data files when they are no longer needed. <br>
Risk: The skill invokes the openclaw command available in PATH. <br>
Mitigation: Ensure the openclaw command resolves to the trusted OpenClaw CLI before using the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Santanu-Kumar-prusty/whatclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with shell command examples and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local JSON files for whitelist sets and message status records.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
