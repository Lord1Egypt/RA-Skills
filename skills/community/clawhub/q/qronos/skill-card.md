## Description:

Qronos helps agents consult an external Qronos API for decisive guidance on timing, trust, relationships, career, finance, and other life-direction questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qronos-ai](https://clawhub.ai/user/qronos-ai)

### License/Terms of Use:


## Use Case:

External users and their agents use Qronos when a human asks a single decision, timing, or trust question and wants the Qronos service's formatted guidance relayed back with the required disclaimer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive decision questions, timing data, and optional personal details may be sent to and retained by an external service.

Mitigation: Use the skill deliberately, avoid names and identifying details, and omit date of birth or gender unless the human explicitly decides those fields are needed.

Risk: The service may return decisive guidance for high-stakes domains with limited independent correction by the agent.

Mitigation: Do not use Qronos for medical, legal, financial-advice, crisis, self-harm, violence, or illegal-activity requests; route those cases to appropriate professional or emergency support.

Risk: Purchase links and returned guidance originate from the external Qronos provider.

Mitigation: Present purchase links and guidance as external-provider content, preserve the required disclaimer, and let the human decide whether to continue.

## Reference(s):

- [ClawHub Qronos skill page](https://clawhub.ai/qronos-ai/skills/qronos)
- [Qronos Terms and Conditions](https://qronos.ai/terms)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Configuration, Guidance]

**Output Format:** [Markdown and plain text guidance, often preserving the API response display text verbatim]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires QRONOS_API_KEY for authenticated consultation requests; API responses may include remaining credits and purchase URLs.]

## Skill Version(s):

1.0.7 (source: server release metadata; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
