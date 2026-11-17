## Description:

Guides Chinese-language test planning for AI agents, covering behavior, tool use, hallucinations, prompt injection, and safety controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kokxi](https://clawhub.ai/user/kokxi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and QA teams use this skill to design AI-agent test plans and traceable cases for tool calls, factuality, prompt-injection resistance, and human oversight.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad agent-testing triggers may activate the skill during general discussions.

Mitigation: Confirm that the user wants a testing plan before following its workflow.

Risk: Declared Bash and WebFetch access may run commands or retrieve external content.

Mitigation: Use these tools only for explicit validation or research tasks the user approves.

## Reference(s):

- [Testing dimensions and checklists](references/dimensions.md)
- [Typical test cases](references/typical-cases.md)
- [Agent testing scenarios](references/scenarios.md)
- [Test case template](assets/case-template.md)
- [ClawHub skill release](https://clawhub.ai/kokxi/skills/qa-agent-testing)

## Skill Output:

**Output Type(s):** [Guidance, Markdown]

**Output Format:** [Chinese-language Markdown test plans, case tables, and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Nine testing dimensions; traceable case identifiers and coverage notes.]

## Skill Version(s):

1.8.0 (source: release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
