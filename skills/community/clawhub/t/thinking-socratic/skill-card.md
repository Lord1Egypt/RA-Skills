## Description:

When a request is vague, assumption-laden, or "obvious," ask the few load-bearing questions that expose hidden requirements before building or committing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tjboudreaux](https://clawhub.ai/user/tjboudreaux)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agents, and reviewers use this skill to clarify vague or assumption-laden requests before building, debugging, or committing to a plan. It guides the agent to ask only the few questions needed for decision-ready requirements and to make assumptions explicit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can add unnecessary friction if applied to well-specified tasks.

Mitigation: Use the artifact's over-application guard: do the work when the request is already clear and stop questioning once the next action is decision-ready.

Risk: The agent could ask the user for facts it can resolve from available local context.

Mitigation: Resolve ambiguity by reading code, running commands, or checking available documentation before asking the user.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tjboudreaux/skills/thinking-socratic)

## Skill Output:

**Output Type(s):** [Guidance, Text, Markdown]

**Output Format:** [Markdown guidance with a structured plain-text clarification template]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable code; changes agent behavior for vague or assumption-laden requests.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
