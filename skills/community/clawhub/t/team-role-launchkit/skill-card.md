## Description:

Launch clone-like multi-agent workflows using explicit role prompts (researcher, builder, editor), strict handoff contracts, and shared behavior files for consistent long-running execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cwheeler67](https://clawhub.ai/user/cwheeler67)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to coordinate complex or long-running agent tasks across research, implementation, and final-response editing roles while keeping handoffs explicit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can encourage agents to record durable outcomes in memory.

Mitigation: Review memory promotion decisions and keep temporary notes out of durable memory unless explicitly approved.

Risk: Multi-role workflows can blur approval boundaries for external or public actions.

Mitigation: Use the handoff contract to document approval constraints before roles act on sensitive projects.

## Reference(s):

- [Handoff Contract](references/handoff-contract.md)
- [Role Prompts](references/role-prompts.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Role-specific deliverables include final output, role-by-role changes, unresolved risks or questions, and the next best action.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
