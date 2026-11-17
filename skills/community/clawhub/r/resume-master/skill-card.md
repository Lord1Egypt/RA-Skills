## Description:

简历工作台 creates or tailors resumes by directly authoring editable HTML source files and exporting print-ready PDFs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangyafu](https://clawhub.ai/user/wangyafu)

### License/Terms of Use:

MIT-0

## Use Case:

Job seekers, students, and agents assisting them use this skill to create new resumes, tailor existing resumes to job descriptions, and export editable HTML into print-ready PDF files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Resume rendering can silently contact outside sites while exporting PDF files.

Mitigation: Replace remote fonts and photos with local assets before rendering when network access is not expected.

Risk: PDF export runs active HTML from the resume source.

Mitigation: Render only trusted HTML in a network-restricted environment and review generated files before sharing.

Risk: The skill writes local HTML, PDF, and image files.

Mitigation: Run it in a workspace where creating or overwriting resume artifacts is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangyafu/skills/resume-master)
- [Skill instructions](artifact/SKILL.md)
- [Example job description](artifact/assets/examples/jd.example.txt)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Editable HTML source files, print-ready PDFs, Markdown planning notes, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May also produce local PDF page images when reviewing resume layout.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
