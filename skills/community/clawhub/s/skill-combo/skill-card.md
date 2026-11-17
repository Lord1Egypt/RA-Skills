## Description:

Skill Combo coordinates multiple installed skills so an agent can parse a combined request, assign responsibilities, orchestrate execution, and merge the results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rfdiosuao](https://clawhub.ai/user/rfdiosuao)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and users use this meta-skill to combine skills for complex tasks that benefit from division of labor, sequencing or parallel execution, and consolidated Markdown results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can coordinate and dynamically load other installed skills, which may make the combined capability broader than the user expected.

Mitigation: Use explicit triggers, review the selected subskills before execution, and limit the combination to the skills needed for the task.

Risk: Combined skills may create reminders, modify state, use credentials, or call external services through delegated behavior.

Mitigation: Require user confirmation before any delegated action that changes state, uses credentials, or reaches an external service.

Risk: Large skill combinations can create unclear responsibility boundaries and harder-to-review outputs.

Mitigation: Prefer small combinations, inspect the execution plan, and review the final integrated result before acting on it.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/rfdiosuao/skills/skill-combo)
- [ClawHub Publisher Profile](https://clawhub.ai/user/rfdiosuao)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown with structured task breakdowns, execution plans, and integrated results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include layered, fused, or summary-style result integration depending on the combined skills and task.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
