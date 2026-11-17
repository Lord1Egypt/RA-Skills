## Description:

Use when a form displays a value but validation or dependent state disagrees; report whether the input actually took effect without submitting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tdw8147-crypto](https://clawhub.ai/user/tdw8147-crypto)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill to determine whether a form field was accepted by the application, record the supporting signals and evidence gaps, and propose a bounded next observation without submitting the business form.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: There is ambiguity between the stated no-submit workflow and instructions about submitting through available tools; ClawScan marks the release suspicious with medium overall confidence.

Mitigation: Before use, clarify what those tool-submission instructions refer to. Do not submit or replay the business form to gather evidence; keep the check to observation and a written record. Treat the scan as guidance, not a safety guarantee.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/tdw8147-crypto/skills/reactive-form-input)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown form input effectiveness record]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Separates observed evidence from missing information and proposed actions; sensitive values should be masked.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
