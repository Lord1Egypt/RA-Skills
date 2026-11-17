## Description:

Professional resume analysis and optimization for the UK job market, including job-description matching, ATS compatibility scoring, keyword suggestions, quantified bullet-point improvements, and .docx resume generation with annotations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phonedog](https://clawhub.ai/user/phonedog)

### License/Terms of Use:


## Use Case:

External job seekers and career-support users use this skill to assess UK resumes against job descriptions, improve ATS keyword coverage, strengthen quantified achievements, and generate an optimized .docx resume with annotations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Resume contents and supplemental answers may be written to local JSON, .docx, and backup files.

Mitigation: Use the skill only with local file handling you are comfortable with, then review and delete intermediate or backup files when finished.

Risk: The current implementation does not create native Word tracked changes or native Word comments.

Mitigation: Review generated [COMMENT] annotations manually in the output document before treating the resume as final.

## Reference(s):

- [ATS Keywords by Industry](references/ats_keywords.md)
- [UK Professional Resume Templates](references/resume_templates.md)
- [ClawHub skill listing](https://clawhub.ai/phonedog/skills/resume-optimizer-uk)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with shell commands, JSON analysis files, and .docx resume output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes local .docx resumes and may write parsed_resume.json, analysis_report.json, supplemental_data.json, optimized_resume.docx, and optional backup files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
