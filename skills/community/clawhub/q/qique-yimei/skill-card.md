## Description:

Use this skill when an agent needs to answer or plan operations for QiQue business requests in pure text protocol mode for customer lookup, wallet records, appointments, orders, goods, messaging, delivery, verification, and create/update/cancel workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edmon](https://clawhub.ai/user/edmon)

### License/Terms of Use:

MIT-0

## Use Case:

External QiQue medical aesthetics operators and support agents use this skill to route Chinese business requests into structured method, parameter, missing-field, safety, and next-action text plans. It supports read workflows and write workflows that require explicit user confirmation before execution planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact includes a credential-like distribution secret.

Mitigation: Treat the bundled value as exposed, rotate it before production use, and distribute replacement credentials through a protected secret manager or platform credential binding.

Risk: The skill asks agents to collect and retain QiQue API secrets.

Mitigation: Do not paste app secrets into chat or store them in generic agent memory; bind app_id and app_secret through the deployment platform's protected credential mechanism.

Risk: Write workflows can affect customer, wallet, appointment, delivery, messaging, and coupon records.

Mitigation: Limit write plans to explicitly confirmed user requests and echo the final method and parameters before execution.

## Reference(s):

- [Intent Routing Notes](references/intent-routing.md)
- [QiQue SDK Methods](references/methods.md)
- [ClawHub Skill Release](https://clawhub.ai/edmon/skills/qique-yimei)

## Skill Output:

**Output Type(s):** [text, JSON, configuration, guidance]

**Output Format:** [Structured JSON text with a short user-facing next action]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write-operation plans require explicit confirmation; credentials must not be exposed in user-facing text.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
