## Description:

Validates whether an XML file matches China's fully digital electronic invoice, or 数电票, format by checking XML structure, required fields, invoice-number characteristics, and signature-related elements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hanw2039](https://clawhub.ai/user/hanw2039)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, finance operations teams, and agents handling Chinese e-invoice XML use this skill for local format triage before deeper tax, compliance, or authenticity review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The sample validator performs shallow XML format checks and may be mistaken for proof of invoice authenticity or regulatory compliance.

Mitigation: Use it only as local triage, then apply full schema validation, trusted tax authority checks, and real digital-signature verification before making compliance, fraud, or payment decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hanw2039/skills/validate-einvoice-xml)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with Python code blocks and validation-report text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local pass/fail format checks and human-readable error details; it does not prove invoice authenticity or tax compliance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
