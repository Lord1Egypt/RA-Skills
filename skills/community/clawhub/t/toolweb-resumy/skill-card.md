## Description:

Generate professional resumes and cover letters from structured data with optional resume parsing capabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, recruiters, HR teams, career service platforms, and applicant tracking systems use this skill to generate ATS-friendly resumes and tailored cover letters from structured candidate data, parse existing resumes into structured fields, and retrieve generated document download links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Resume and cover-letter requests can include highly personal candidate, employee, or applicant data that is sent to ToolWeb's external API.

Mitigation: Use only data approved for external processing, and obtain acceptable privacy, retention, deletion, and security terms from the publisher before processing confidential or regulated personal data.

Risk: Generated document download links may expose candidate documents if shared, retained, or accessed outside the intended workflow.

Mitigation: Treat returned download URLs as sensitive, limit distribution to authorized users, and review the publisher's document retention and deletion practices before production use.

## Reference(s):

- [Resumy API Docs](https://api.toolweb.in:8166/docs)
- [Resumy API Gateway Route](https://api.toolweb.in/tools/resumy)
- [ClawHub Skill Page](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/toolweb-resumy)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, files, guidance]

**Output Format:** [Markdown guidance with JSON request and response examples; API responses include JSON metadata and generated document download URLs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated documents are retrieved through download URLs returned by the external API.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
