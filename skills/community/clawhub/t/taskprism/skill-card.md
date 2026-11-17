## Description:

Task Prism is a Chinese-language project planning skill that turns ambiguous business needs into structured task breakdowns, skill profiles, workflows, budgets, risk plans, change controls, and feasibility recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qomob](https://clawhub.ai/user/qomob)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, project managers, and operations teams use this skill to clarify vague business requests and produce actionable project plans with WBS, RACI, stakeholder communication, budget, risk, change-control, retrospective, and Go/No-Go sections.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate on broad planning phrases and produce a full project-planning workflow when the user wanted a narrow answer.

Mitigation: Confirm the requested scope or use a single-dimension mode such as WBS, skills, cost, risk, change, retro, or status.

Risk: The skill is written for Chinese-language planning and may answer in Chinese when the conversation expects another language.

Mitigation: State the desired response language before invoking the skill and translate or adapt generated planning artifacts for the target audience.

Risk: Generated estimates, budgets, risk ratings, and Go/No-Go recommendations can be incorrect if user-provided project facts are incomplete.

Mitigation: Review assumptions, dependencies, cost inputs, legal or regional constraints, and high-risk items with qualified project owners before execution.

## Reference(s):

- [Task Prism Examples](references/examples.md)
- [Task Prism Templates](references/templates.md)
- [Server-resolved GitHub provenance](https://github.com/qomob/TaskPrism)
- [ClawHub skill page](https://clawhub.ai/qomob/skills/taskprism)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with structured sections, tables, checklists, and WBS-style code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language project planning output that may include clarification questions, task decompositions, skill profiles, RACI matrices, budgets, risk registers, change logs, retrospectives, and Go/No-Go recommendations.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata; artifact metadata reports 4.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
