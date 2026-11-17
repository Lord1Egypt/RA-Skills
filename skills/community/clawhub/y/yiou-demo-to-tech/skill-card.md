## Description:

Converts Chinese-language business demos, prototypes, and requirements into structured technical planning documents with page flows, fields, interface needs, acceptance criteria, open questions, task breakdowns, and maturity ratings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yiou](https://clawhub.ai/user/yiou)

### License/Terms of Use:

MIT-0

## Use Case:

Product, engineering, and delivery teams use this skill before development to turn business-oriented demos or requirements into documents that support technical review, estimation, decomposition, scheduling, and acceptance planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may infer fields, APIs, data ownership, and development tasks from incomplete demo or requirement inputs.

Mitigation: Review all inferred content before implementation and preserve the required source labels and pending-confirmation markers for uncertain items.

Risk: Planning documents generated from missing required inputs could be mistaken for development-ready specifications.

Mitigation: Use the maturity rating and blocking gaps to prevent documents with missing business goals, roles, page flows, core fields, data sources, or acceptance criteria from being treated as ready for development.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yiou/skills/yiou-demo-to-tech)
- [Technical document template](artifact/templates/tech_doc_template.md)
- [Structured output template](artifact/templates/structured_output_template.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Markdown technical document plus structured JSON, question tables, development task breakdowns, acceptance criteria, and maturity rating]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs must distinguish provided facts from inferred or defaulted content, mark uncertain interfaces as pending confirmation, and identify blocking gaps before development.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
