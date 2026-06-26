## Description: <br>
Places immediate or scheduled outbound voice reminder calls from contact, reminder content, and simple natural-language timing requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smallkeyboy](https://clawhub.ai/user/smallkeyboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill when a user asks to notify a contact by phone immediately or at a scheduled time. It parses simple Chinese reminder timing phrases and returns JSON task information for the agent to report back to the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place real outbound calls through a hardcoded external call service and account identifiers. <br>
Mitigation: Install only if the call service and account identifiers are trusted, and require manual confirmation of every recipient, message, and scheduled time before execution. <br>
Risk: Delayed reminders use shell-based background scheduling. <br>
Mitigation: Avoid delayed reminders until scheduling is replaced with a supervised scheduler or run only in an environment where background processes are monitored. <br>
Risk: Phone numbers and reminder content may be retained without clear controls. <br>
Mitigation: Do not use sensitive phone numbers or private reminder content unless retention, access, and deletion controls are documented and acceptable. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/smallkeyboy/voice-reminder) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Text] <br>
**Output Format:** [JSON responses with command-line status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Running the scripts may initiate outbound calls or schedule delayed reminders.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
