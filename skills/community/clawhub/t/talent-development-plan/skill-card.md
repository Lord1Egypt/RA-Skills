## Description:

Generates vocational-education talent development plans by combining professional teaching standards, occupational analysis reports, national public-course requirements, and built-in templates into Markdown and DOCX-ready program documentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flyboat403](https://clawhub.ai/user/flyboat403)

### License/Terms of Use:

MIT-0

## Use Case:

External education and curriculum staff use this skill to draft vocational program talent development plans from a target major, teaching standards, occupational reports, and optional sample templates. It supports secondary vocational, higher vocational, and integrated program planning workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatically retrieved teaching-standard PDFs may come from sources that require review before download.

Mitigation: Review the teaching-standard PDF source before allowing download or using extracted content.

Risk: The advertised built-in retrieval workflow may be incomplete because referenced search and index assets are missing.

Mitigation: Confirm the required standards assets are present, or have users upload the teaching standard files directly.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/flyboat403/talent-development-plan)
- [ClawHub skill page](https://clawhub.ai/flyboat403/skills/talent-development-plan)
- [Course Objective Generation Rules](references/course-objective-generation.md)
- [Error Recovery Guide](references/error-recovery.md)
- [National Standards Reference](references/national-standards.md)
- [Self-Check List](references/self-check-list.md)
- [Teaching Schedule Rules](references/teaching-schedule-rules.md)
- [Template Chapters](references/template-chapters.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell and Python command examples; generated plan content is intended for Markdown-to-DOCX output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local Markdown, DOCX-ready content, and curriculum-structure PNG files when the referenced scripts are available.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
