## Description: <br>
Team Communication helps agents coordinate with predefined team sessions by using sessions_send and sessions_list. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ebly](https://clawhub.ai/user/ebly) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to route coordination requests, task handoffs, testing updates, design requests, and support needs to named team sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent may accidentally share secrets, credentials, private customer data, or excessive conversation history with another session. <br>
Mitigation: Verify the sessionKey and recipient authorization before sending, and omit sensitive data unless the recipient is trusted and authorized. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ebly/team-communication) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes team session routing guidance and example sessions_send commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
