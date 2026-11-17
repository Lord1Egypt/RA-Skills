## Description:

Audits Chinese technical resumes for timeline and quantification issues, offers improvement guidance, optionally anonymizes contact details, and generates a formatted DOCX resume.

This skill is ready for commercial/non-commercial use.

## Publisher:

[putao2882-ui](https://clawhub.ai/user/putao2882-ui)

### License/Terms of Use:

MIT-0

## Use Case:

Job seekers and career-support agents use this skill to review Chinese technical resumes, identify logic or evidence gaps, protect contact information when needed, and produce a cleaner Word document for sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Resume content can contain sensitive personal data.

Mitigation: Use anonymized mode before sharing output externally and install only when comfortable providing resume text to the skill.

Risk: The generated DOCX uses a fixed output filename and may overwrite an existing file.

Mitigation: Run the skill in a dedicated working directory or rename existing AI_Beautified_Resume.docx files before generation.

Risk: Dependencies are not pinned in the artifact requirements.

Mitigation: Prefer a release with pinned dependencies or pin and review dependencies before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/putao2882-ui/skills/resume-auditor)
- [Publisher profile](https://clawhub.ai/user/putao2882-ui)

## Skill Output:

**Output Type(s):** [Text, Guidance, Files]

**Output Format:** [Diagnostic text and a generated DOCX file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The generated resume file uses the fixed filename AI_Beautified_Resume.docx.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
