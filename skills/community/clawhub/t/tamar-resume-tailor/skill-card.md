## Description:

Tailor resumes for specific job applications using the Tamar AI API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[evgenyshneyderman](https://clawhub.ai/user/evgenyshneyderman)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to guide Tamar CLI workflows for uploading or selecting a resume, analyzing a job description, tailoring the resume, applying feedback, and downloading PDF or JSON results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Resume files, job descriptions, feedback, and generated resume data may be sent to a third-party service.

Mitigation: Use only with materials the user is comfortable sending to Tamar, and confirm each upload, tailoring, feedback, and download step before running CLI commands.

Risk: Unsafe shell examples can become command-injection risks if untrusted pasted text is interpolated into shell commands.

Mitigation: Write job descriptions and feedback to safely created temporary files or pass values as safely separated arguments; do not interpolate untrusted text into shell commands.

Risk: Installing an unpinned global npm CLI can introduce unexpected behavior from later package versions.

Mitigation: Install tamar-cli from a pinned, trusted version and verify the intended binary before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/evgenyshneyderman/skills/tamar-resume-tailor)
- [Tamar API documentation](https://ask-tamar.com/developers)
- [Tamar website](https://ask-tamar.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and summaries of Tamar CLI JSON results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide generation of PDF or JSON resume artifacts through the Tamar CLI; resume content and job descriptions are handled by the third-party Tamar service.]

## Skill Version(s):

1.4.1 (source: server release evidence; artifact/claw.json lists 1.4.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
