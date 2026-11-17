## Description:

Generates classroom-ready teaching presentation outlines and PPTX courseware from lesson plans, web content, or topic keywords, with content classification, classroom flow structure, interaction planning, role mapping, and teacher-facing speaker notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flyboat403](https://clawhub.ai/user/flyboat403)

### License/Terms of Use:

MIT-0

## Use Case:

Teachers and instructional-content creators use this skill to turn lesson plans, teaching materials, web content, or topic keywords into classroom-oriented presentation plans and PPTX courseware. It emphasizes classroom progression, interaction design, and teacher speaker notes rather than static knowledge summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may process lesson files or webpage content supplied by the user.

Mitigation: Provide only teaching materials that are appropriate to use for presentation generation, and review generated classroom content before use.

Risk: The skill expects Chinese-language teaching presentation workflows and may depend on related helper references or a PPTX generation skill.

Mitigation: Confirm the target agent environment has compatible PPTX generation capability and review outputs when adapting the workflow outside Chinese-language classroom contexts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/flyboat403/skills/teaching-presentation)
- [Publisher Profile](https://clawhub.ai/user/flyboat403)
- [Server-Resolved GitHub Repository](https://github.com/flyboat403/teaching-presentation)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Files, Code, Guidance]

**Output Format:** [Structured JSON outline followed by PPTX presentation files when a compatible PPTX generation skill is available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May consume lesson-plan documents, webpage content, or topic keywords; generated slides are expected to include teacher-facing speaker notes.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
