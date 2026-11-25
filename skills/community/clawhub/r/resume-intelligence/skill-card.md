## Description:

Builds resumes, visual templates, career vaults, and interview preparation materials from verified career evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rahulbsw](https://clawhub.ai/user/rahulbsw)

### License/Terms of Use:

MIT-0

## Use Case:

People preparing or improving resumes and interview materials can use this skill to organize approved career evidence and create tailored resumes, career coaching, job matching, and interview preparation outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation triggers and unclear file access scope may extend a run beyond the intended task or sources.

Mitigation: Invoke the skill for a specific career task, limit each run to approved sources and folders, and review file access before use.

Risk: The security review was benign with medium confidence and partial coverage; some local references and binary thumbnails were not fully analyzed.

Mitigation: Review the skill files and intended access scope before installation or use.

Risk: Career materials can contain credentials, personal information, and confidential employer details.

Mitigation: Keep credentials out of files and outputs, use approved sources, and redact sensitive details before sharing or sending content to external design services.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/rahulbsw/skills/resume-intelligence)
- [Source skill repository (server-resolved provenance)](https://github.com/rahulbsw/resume-builder/tree/master/plugins/resume-intelligence/skills/resume-intelligence)

## Skill Output:

**Output Type(s):** [Text, Markdown, HTML, JSON, DOCX, PDF, Guidance]

**Output Format:** [Markdown, JSON, HTML, DOCX, and PDF documents]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs vary by workflow and the career evidence the user approves.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
