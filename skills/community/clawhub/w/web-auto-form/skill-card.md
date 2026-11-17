## Description:

Web Auto Form lets agents drive browser-based form filling, submission, conditional branching, and structured data extraction from JSON-defined workflows with PII redaction support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duz1287](https://clawhub.ai/user/duz1287)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and agent builders use this skill to automate authorized web form workflows such as registrations, applications, data entry, form testing, file uploads, and confirmation data extraction. It is intended for workflows where the user can provide an explicit automation purpose and review the target destination.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent broad browser-control authority, including form submission and file upload.

Mitigation: Use it only for authorized workflows, review JSON steps before execution, and prefer HTTPS destinations that the user has verified.

Risk: Sensitive form data, credentials, or uploaded files may be exposed to unintended destinations if a workflow is misconfigured.

Mitigation: Avoid credentials and sensitive uploads unless the destination is verified, keep PII redaction enabled, and require a clear consent statement for each run.

Risk: Failure diagnostics and debug artifacts may capture page contents or submitted data.

Mitigation: Disable diagnostics and debug artifact collection for sensitive forms, or store generated artifacts only in controlled locations with appropriate access controls.

Risk: Server-resolved GitHub import provenance is unavailable for this version.

Mitigation: Pin the package version and review the installed Python package or source before production use.

## Reference(s):

- [Web Auto Form ClawHub listing](https://clawhub.ai/duz1287/skills/web-auto-form)
- [WebAutoForm project homepage](https://github.com/DUZ1287/WebAutoForm)

## Skill Output:

**Output Type(s):** [JSON, Files, Configuration, Shell commands, Guidance]

**Output Format:** [JSON execution results with status, per-step records, extracted fields, warnings, and optional diagnostic artifacts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can include redacted values, skipped or failed step records, extracted fields, and debug screenshots or traces when enabled.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
