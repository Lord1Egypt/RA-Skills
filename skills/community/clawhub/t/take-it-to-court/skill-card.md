## Description:

Use this skill when filing a Disputron case to gather a concrete title, specific statement, well-shaped win conditions, and a lawyer persona that fits the case.

This skill is ready for commercial/non-commercial use.

## Publisher:

[disputron](https://clawhub.ai/user/disputron)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to prepare stronger Disputron case filings before submitting them through the CLI, MCP tool, or public REST API. It helps shape the filing into concrete facts, actionable win conditions, and an appropriate advocacy style.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Preflight cases may use the current conversation as case context.

Mitigation: Confirm the filing inputs with the user and include only details that are relevant to the case.

Risk: Repeated test filings can consume a daily Disputron quota.

Mitigation: Avoid filing test cases in loops and tell the user before submitting any case.

Risk: Vague or extreme win conditions can lead to weak or impractical case filings.

Mitigation: Elicit concrete facts and steer requested outcomes toward actionable remedies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/disputron/skills/take-it-to-court)

## Skill Output:

**Output Type(s):** [Guidance, Text, Markdown, Configuration instructions]

**Output Format:** [Markdown guidance with structured filing fields and inline command or tool references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces case-preparation guidance; does not execute code or submit cases by itself.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
