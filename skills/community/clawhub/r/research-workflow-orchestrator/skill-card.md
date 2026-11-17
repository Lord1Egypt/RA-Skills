## Description:

Use this skill to coordinate local research work across multiple agents and tools when the task needs lightweight routing, decomposition, handoffs, and local orchestration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oceandeepgavin](https://clawhub.ai/user/oceandeepgavin)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent users use this skill to route research tasks, split work only when needed, coordinate handoffs, and track lightweight local status across multiple agents or tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Multi-agent task splitting can introduce coordination overhead or incorrect handoffs when a single agent could complete the work cleanly.

Mitigation: Apply the skill only when the task crosses responsibilities, and keep handoffs limited to goal, scope, output, constraints, and done-when criteria.

Risk: Using the skill for sensitive workflows may expand who or what receives task context during coordination.

Mitigation: Avoid sensitive workflows unless explicit multi-agent coordination is intended, and keep shared context to the current objective, assignments, status, and handoff information.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/oceandeepgavin/skills/research-workflow-orchestrator)
- [ClawHub Publisher Profile](https://clawhub.ai/user/oceandeepgavin)

## Skill Output:

**Output Type(s):** [guidance, markdown]

**Output Format:** [Markdown guidance with concise routing, handoff, and status structures]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces lightweight coordination guidance; it does not execute code, persist data, or handle credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
