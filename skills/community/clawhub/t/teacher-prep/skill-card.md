## Description:

teacher-prep helps elementary Chinese-language teachers gather lesson materials and generate Markdown preparation notes, PowerPoint lesson plans, and Word exercise sheets for common primary-school text types.

This skill is ready for commercial/non-commercial use.

## Publisher:

[870021840](https://clawhub.ai/user/870021840)

### License/Terms of Use:

MIT-0

## Use Case:

Teachers and education-support agents use this skill to prepare elementary Chinese-language lessons for poems, modern prose, fables, fairy tales, and expository texts. It supports gathering reference material, structuring lesson notes, and producing classroom-ready draft files for teacher review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tavily searches may expose sensitive student, classroom, or proprietary content if such content is included in prompts.

Mitigation: Avoid sensitive or proprietary details in search prompts and review search-derived material before including it in lesson resources.

Risk: Generated lesson materials and bundled document scripts can produce draft templates or incomplete lesson-specific answers.

Mitigation: Have a teacher review and adapt all Markdown notes, PPT lesson plans, exercises, and answer material before classroom use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/870021840/skills/teacher-prep)

## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance plus generated .md, .pptx, and .docx files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Tavily search when configured with TAVILY_API_KEY and writes local files named like 备课资料_<lesson>.md, 教案_<lesson>.pptx, and 练习题_<lesson>.docx.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
