## Description:

Guides an agent through a Chinese-language workflow for collecting styrene distillation section parameters, calling jixietools.com APIs, creating a guest production sheet, and monitoring CAD drawing generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[realsanyu](https://clawhub.ai/user/realsanyu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and engineering agents use this skill to collect design inputs, submit calculation requests, create unauthenticated guest production sheets, and retrieve CAD drawing job status for a styrene distillation section workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends user-supplied engineering parameters to jixietools.com and uses unauthenticated guest links or codes to access job status and outputs.

Mitigation: Review parameters before use, avoid submitting confidential or regulated data, and share generated guest links only with intended recipients.

Risk: Server security evidence reports a mismatch between the stated styrene-distillation purpose and gear or mechanical ordering workflow details.

Mitigation: Confirm that selected products and API category identifiers match the intended styrene distillation workflow before creating a production sheet.

Risk: Shell command examples interpolate request data into curl JSON payloads.

Mitigation: Construct requests with structured JSON serialization and validate user-provided values before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/realsanyu/skills/styrene)
- [Jixietools API Base](https://jixietools.com/api/v1)
- [Jixietools Products Endpoint](https://jixietools.com/api/v1/products?category_id=8)
- [Jixietools Guest Production Status Endpoint](https://jixietools.com/api/v1/production_sheets/guest_show?code=GUEST_CODE)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, API calls, guidance]

**Output Format:** [Chinese-language Markdown with tables, browser links, and inline bash curl commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maintains a filename across incremental calculations and a guest_code for status polling.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
