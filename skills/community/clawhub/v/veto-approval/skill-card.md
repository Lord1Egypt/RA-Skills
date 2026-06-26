## Description: <br>
Pause your agent for human approval before high-risk actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mrchop](https://clawhub.ai/user/mrchop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to pause an agent before sensitive actions and require a human approver to accept or reject the request by email before the agent continues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Approval details, approver email addresses, and provided context are sent to VetoAPI. <br>
Mitigation: Avoid secrets or regulated data in approval titles or context, protect VETO_API_KEY, and review VetoAPI suitability before production use. <br>
Risk: The approval request blocks while polling for a decision. <br>
Mitigation: Add operational timeouts or cancellation handling around agent workflows that cannot wait indefinitely. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/mrchop/veto-approval) <br>
- [VetoAPI API Reference](https://vetoapi.com/docs) <br>
- [VetoAPI API key setup](https://vetoapi.com/get-key) <br>
- [VetoAPI homepage](https://vetoapi.com) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Guidance, API Calls] <br>
**Output Format:** [Python function return value, command-line status text, and setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns True when approved and False when rejected or on request errors; polls VetoAPI until a decision is available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
