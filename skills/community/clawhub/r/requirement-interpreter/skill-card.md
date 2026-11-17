## Description:

智能需求解读技能，通过多级分类和案例匹配帮助用户准确表达需求，并提供标准化交付物清单。

This skill is ready for commercial/non-commercial use.

## Publisher:

[samwang-001](https://clawhub.ai/user/samwang-001)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn vague or complex requests into clearer requirement classifications, structured interview questions, best-practice guidance, and standardized delivery checklists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recent requirement text may remain in process-local interaction history during a run.

Mitigation: Avoid submitting secrets or regulated data unless that local retention is acceptable; maintainers should document or remove the logging behavior.

Risk: Auto-activation behavior may be unclear to users when vague requirements trigger the workflow.

Mitigation: Document when the skill activates and allow users or deployers to review activation behavior before use.

## Reference(s):

- [Requirement Patterns](references/requirement_patterns.md)
- [Simple Requirement Template](assets/templates/simple_requirement_template.md)
- [Technical Requirement Template](assets/templates/technical_requirement_template.md)
- [Requirement Completeness Checklist](assets/checklists/requirement_completeness_checklist.md)
- [AI Communication Checklist](assets/checklists/ai_communication_checklist.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown or structured text containing requirement classifications, clarifying questions, best practices, and delivery checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-first guidance; command-line script output is also supported by the artifact.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
