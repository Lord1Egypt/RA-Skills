## Description:

Use this when a user proposes a project or task that needs planning. Guide them through staged questions with options and descriptions to clarify goals, constraints, scope, and technical approaches. When knowledge is insufficient, launch subagent research. Output a complete plan.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phallusophy](https://clawhub.ai/user/phallusophy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn vague project ideas into staged plans with clarified goals, constraints, scope, risks, and technical approaches. It is intended for planning conversations where the agent should present options with consequences and confirm decisions before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate for broad planning-like requests and guide the agent through a multi-stage planning workflow.

Mitigation: Review whether planning mode is appropriate for the request before relying on the plan or moving to execution.

Risk: The skill may consult prior memory or launch research subagents when it determines that more context is needed.

Mitigation: Ask the agent to confirm before using memory or spawning research when tighter control is required.

Risk: If research cannot be completed, plan details may remain pending or incomplete.

Mitigation: Keep unresolved items marked as pending confirmation and resolve them before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/phallusophy/skills/situated-planning-mode)
- [Dynamic Question Generation Mechanism](artifact/references/dynamic-questions.md)
- [Error Reference](artifact/references/errors.md)
- [Output Format Templates](artifact/references/templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Conversational Markdown with optional structured JSON completion records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include staged selections, a planning summary, next action, or incomplete-stage details.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
