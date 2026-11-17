## Description:

Before any destructive or irreversible action, run a safety pre-flight to check risks, reversibility, and timing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cutthemustard](https://clawhub.ai/user/cutthemustard)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill before destructive, irreversible, high-stakes, or production-impacting actions to assess safety checklist items, reversibility, and timing before proceeding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Action descriptions, platform or resource names, and timezone metadata may be sent to AgentUtil services.

Mitigation: Avoid including secrets, customer data, or sensitive internal details in action descriptions.

Risk: Paid service calls may incur disclosed x402 charges.

Mitigation: Review the per-check pricing before using paid endpoints.

## Reference(s):

- [AgentUtil homepage](https://agentutil.net)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown recommendation with structured findings and optional MCP or HTTP command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use third-party AgentUtil services for safety, reversibility, and timing checks.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
