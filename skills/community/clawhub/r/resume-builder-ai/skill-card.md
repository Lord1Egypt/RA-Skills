## Description:

Resume Builder helps users create, update, tailor, review, and export resumes, CVs, cover letters, ATS checks, and interview-prep guidance through conversation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mkpareek0315](https://clawhub.ai/user/mkpareek0315)

### License/Terms of Use:


## Use Case:

External users use this skill to build and manage resume materials from chat, including structured profile data, tailored resume versions, cover letters, ATS-oriented feedback, and interview preparation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores sensitive resume and cover-letter data locally under ~/.openclaw/resume-builder/.

Mitigation: Install only when local storage of that information is acceptable, and review or delete the stored files when they are no longer needed.

Risk: Broad prompts such as "summary" may activate resume-related behavior outside an intended resume workflow.

Mitigation: Use the skill in clear resume, CV, cover-letter, or job-application contexts and review generated output before saving or reusing it.

## Reference(s):

- [Resume Builder Skill Page](https://clawhub.ai/mkpareek0315/skills/resume-builder-ai)
- [Publisher Profile](https://clawhub.ai/user/mkpareek0315)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and plain text with occasional JSON examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces user-facing resume content and stores profile, settings, versions, and cover-letter data locally under ~/.openclaw/resume-builder/.]

## Skill Version(s):

1.1.0 (source: server-resolved release metadata; changelog: Removed exec permission)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
