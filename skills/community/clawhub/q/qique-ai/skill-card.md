## Description:

Use this skill when an agent needs to answer or plan operations for QiQue business requests in pure text protocol mode for customer/profile lookup, wallet change records, appointments, order and goods queries, SMS/card sending, delivery/verification, and create/update/cancel workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edmon](https://clawhub.ai/user/edmon)

### License/Terms of Use:

MIT-0

## Use Case:

External QiQue business users use this skill to convert Chinese operational requests for customers, wallet records, appointments, orders, goods, SMS/card sending, delivery, verification, and create/update/cancel workflows into structured text plans. The skill checks required parameters and requires explicit confirmation before write-operation plans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is flagged suspicious because the security evidence reports a plaintext distribution credential and user API secret persistence in chat or text state.

Mitigation: Remove and rotate the distribution credential before use, and replace chat or text-state secret handling with secure secret entry and storage.

Risk: The skill can plan write operations against customer, wallet, appointment, delivery, SMS/card, and related business records.

Mitigation: Keep the explicit write confirmation workflow and require review of the final method and parameters before any write execution.

## Reference(s):

- [QiQue SDK Methods](references/methods.md)
- [Intent Routing Notes](references/intent-routing.md)
- [Local Config Template](config/qique.config.example.json)

## Skill Output:

**Output Type(s):** [text, JSON, guidance, configuration]

**Output Format:** [Structured text containing a JSON routing frame plus concise user-facing next-action guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write-operation plans require explicit user confirmation; sensitive credential values must not be exposed in user-facing text.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
