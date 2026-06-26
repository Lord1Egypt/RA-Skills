## Description: <br>
Use this skill when an agent needs to answer or plan operations for QiQue business requests in pure text protocol mode, including customer/profile lookup, wallet change records, appointments, order and goods queries, SMS/card sending, delivery/verification, and create/update/cancel workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edmon](https://clawhub.ai/user/edmon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business users and agents use this skill to translate Chinese QiQue medical-aesthetic business requests into structured method-routing plans with normalized parameters, missing-field checks, and user-facing next actions. The skill supports read workflows and guarded write workflows for customer, appointment, wallet, order, goods, SMS/card, delivery, verification, and related operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence reports unsafe persistent handling of API secrets for a real business integration. <br>
Mitigation: Use vault-backed or scoped secret storage instead of chat text or persistent config, rotate any credentials already shared, and verify how stored secrets can be deleted or revoked. <br>
Risk: The skill can prepare write-operation plans that affect business records. <br>
Mitigation: Require explicit user confirmation for write operations and review the final method and parameters before execution. <br>


## Reference(s): <br>
- [QiQue skill page](https://clawhub.ai/edmon/qique-ai) <br>
- [Publisher profile](https://clawhub.ai/user/edmon) <br>
- [Method catalog and operation class](references/methods.md) <br>
- [Intent routing behavior](references/intent-routing.md) <br>
- [Local config template](config/qique.config.example.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown text containing structured JSON frames and short user-facing guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Routes intents to method names and parameters; write operations require explicit confirmation before final execution planning.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
