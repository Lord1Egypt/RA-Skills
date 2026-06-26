## Description: <br>
Provides a coordination protocol for running multiple AI agents in one Telegram group chat through role-based messaging, sender validation, turn-taking, blocker escalation, and mission lifecycle control. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Kiril-Shturman](https://clawhub.ai/user/Kiril-Shturman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and operators use this skill to coordinate COO and worker bots in a shared Telegram group, keeping task assignment, status reporting, blocker escalation, and mission completion explicit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unverified bot identities or open command triggers could let the wrong participant drive the workflow. <br>
Mitigation: Verify bot identities, restrict who can trigger commands, use explicit sender allowlists where possible, and keep a human operator able to stop the workflow. <br>
Risk: Telegram group permissions or provider setup may not enforce the protocol by itself. <br>
Mitigation: Configure Telegram permissions separately and test one simple mission before adding status checks, blockers, or parallel work. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Kiril-Shturman/telegram-agent-coordination) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Configuration instructions] <br>
**Output Format:** [Markdown guidance with protocol message examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Text-only protocol; no executable code or credential handling.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
