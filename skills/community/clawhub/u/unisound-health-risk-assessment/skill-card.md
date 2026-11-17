## Description:

Assesses health-exam reports across cardiovascular, glucose metabolism, tumor, metabolic syndrome, liver, kidney, and thyroid risk dimensions and produces a JSON risk profile plus a health risk report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unisound-llm](https://clawhub.ai/user/unisound-llm)

### License/Terms of Use:

MIT-0

## Use Case:

Health management teams and medical-service developers use this skill to assess de-identified health examination reports, classify major health risks, and draft time-bound management plans for qualified clinical review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive medical-report content and API keys may be sent to a configurable remote LLM endpoint.

Mitigation: Use de-identified reports, keep the default trusted HTTPS endpoint unless an alternate endpoint is verified, and provide credentials through channels that do not expose them in shell history or logs.

Risk: Generated health recommendations can be incomplete, misleading, or clinically inappropriate.

Mitigation: Treat output as advisory health-risk support and require review by qualified medical professionals before patient-facing or care-management use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unisound-llm/skills/unisound-health-risk-assessment)
- [Publisher profile: unisound-llm](https://clawhub.ai/user/unisound-llm)
- [Unisound MaaS chat completions endpoint](https://maas-api.hivoice.cn/v1/chat/completions)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [JSON followed by a plain-text health risk report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May be printed to stdout or saved to a file; requires a health-exam report input and an appkey.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
