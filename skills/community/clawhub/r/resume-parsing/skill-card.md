## Description:

Parses PDF/DOCX resumes into structured JSON Resume data for English and Chinese resumes, including contact details, work history, education, skills, projects, and parser traceability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[casperkwok](https://clawhub.ai/user/casperkwok)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, recruiting teams, and ATS workflow builders use this skill to extract single resumes or folders of resumes into JSON Resume records, readable summaries, and batch candidate indexes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The extraction script can install an unpinned pdfmuse dependency at first run.

Mitigation: Review and pin the pdfmuse dependency in a controlled virtual environment before installing or running the skill.

Risk: Parsed resume outputs can persist sensitive personal data such as contact details to disk.

Mitigation: Process only authorized resumes and write JSON, Markdown, CSV, and extraction sidecar files to restricted storage.

Risk: Same-named resumes from different folders can overwrite each other's extraction files.

Mitigation: Use unique output directories or rename inputs before batch processing folders that may contain duplicate filenames.

## Reference(s):

- [JSON Resume Mapping Rules](artifact/reference/schema.md)
- [Mapping Examples](artifact/examples.md)
- [JSON Resume](https://jsonresume.org)
- [pdfmuse Project](https://github.com/casperkwok/pdfmuse)
- [pdfmuse Package](https://pypi.org/project/pdfmuse/)
- [ClawHub Skill Page](https://clawhub.ai/casperkwok/skills/resume-parsing)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON Resume files, Markdown summaries, CSV batch indexes, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include personal contact details and parser traceability metadata.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
