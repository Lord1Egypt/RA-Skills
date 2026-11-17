## Description:

Generates K-12 teaching materials such as PPT courseware, lesson plans, student task sheets, teaching-resource summaries, and optional mind maps for Chinese and mathematics classroom workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ahao2001](https://clawhub.ai/user/ahao2001)

### License/Terms of Use:

MIT-0

## Use Case:

Teachers and education-content creators use this skill to prepare classroom materials, including slide decks, teaching designs, student worksheets, and resource folders. It is especially oriented toward Chinese K-12 mathematics and language-arts preparation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact asks users for education-site usernames and passwords and stores them in a local accounts.json file.

Mitigation: Do not provide reusable passwords to the agent; replace the workflow with manual login, scoped browser sessions, or a secure credential manager before deployment.

Risk: The artifact describes automatic fetching, downloading, clipping, screenshots, and integration of external teaching resources.

Mitigation: Limit fetching to trusted public sources, review copyright and platform terms, scan downloaded files, and require user confirmation before storing or embedding resources.

Risk: Generated documents and downloaded resources are written to fixed local course folders.

Mitigation: Confirm output paths before execution and review generated files before sharing them with students or staff.

## Reference(s):

- [Teaching Materials Skill Page](https://clawhub.ai/ahao2001/skills/teaching-materials)
- [Courseware Guide](artifact/references/ppt_guide.md)
- [Mind Map Guide](artifact/references/mindmap_guide.md)
- [Education Platform Reference](artifact/references/edu_platforms.md)
- [Teaching Design Template](artifact/references/teaching_design_template.md)
- [Student Task Sheet Template](artifact/references/task_sheet_template.md)
- [National Smart Education Platform](https://basic.smartedu.cn/)
- [PEP Smart Education Platform](https://pep.smartedu.cn/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with document outlines, template-filled content, command snippets, configuration examples, and generated-file paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to create PPTX, DOCX, Markdown, Mermaid, DrawIO, Excalidraw, image, screenshot, and resource files in a course-specific workspace.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
