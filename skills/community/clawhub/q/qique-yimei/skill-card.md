## Description: <br>
Helps agents answer or plan QiQue medical beauty system operations in text-only protocol mode, including customer lookup, appointments, orders, wallet changes, SMS/card sending, delivery, verification, and create/update/cancel workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edmon](https://clawhub.ai/user/edmon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business operators and support agents use this skill to route Chinese-language QiQue medical beauty system requests into a method, normalized parameters, missing required fields, a read/write safety decision, and the next user-facing action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive QiQue API credentials may be exposed or retained insecurely. <br>
Mitigation: Use least-privilege, revocable credentials, avoid pasting production secrets into normal chat, rotate any exposed values, and prefer a vault or scoped configuration mechanism. <br>
Risk: Write-operation plans could affect customer or business records if executed without clear authorization. <br>
Mitigation: Require explicit confirmation before write operations and review the planned method and parameters before execution. <br>


## Reference(s): <br>
- [QiQue SDK Methods](references/methods.md) <br>
- [Intent Routing Notes](references/intent-routing.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Configuration, Guidance] <br>
**Output Format:** [Structured text with a JSON frame] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit confirmation before write-operation plans and must not expose stored credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
