## Description: <br>
Advanced AI voice assistant for phone calls. Capable of persuasion, sales, restaurant bookings, reminders, and notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cmorillas99-cyber](https://clawhub.ai/user/cmorillas99-cyber) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Employees, external users, and developers can use this skill to initiate Vapi-powered phone calls for defined missions such as sales outreach, bookings, reminders, and notifications. Operators should confirm the recipient, purpose, consent, and applicable calling rules before use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place real autonomous phone calls through the operator's Vapi account. <br>
Mitigation: Confirm each recipient, purpose, consent, and legal basis before execution, and restrict access to trusted operators. <br>
Risk: The webhook must be exposed to the internet while a call is active. <br>
Mitigation: Expose the webhook only through a controlled HTTPS tunnel or deployment, monitor access, and close the tunnel after use. <br>
Risk: Calls may create Vapi usage costs. <br>
Mitigation: Set account-level budgets or monitoring and review call cost fields in returned results. <br>
Risk: Call transcripts and summaries may be written to local logs. <br>
Mitigation: Protect the log directory, limit retention, and delete transcripts when they are no longer needed. <br>
Risk: The release security verdict is suspicious because consent, safety, and transcript-retention risks are under-disclosed. <br>
Mitigation: Review the security guidance before deployment and add operating procedures for consent, AI disclosure, recording, and transcript handling. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/cmorillas99-cyber/vapi-calls) <br>
- [Publisher profile](https://clawhub.ai/user/cmorillas99-cyber) <br>


## Skill Output: <br>
**Output Type(s):** [API calls, JSON, Files, Guidance] <br>
**Output Format:** [JSON call result with status, transcript, summary, cost, duration, and local log file path when available] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can place real outbound phone calls through a configured Vapi account and writes local call result logs.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, package.json, server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
