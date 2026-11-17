## Description:

Run complex tasks with explicit role separation (operator, researcher, builder, editor), structured handoff contracts, and memory hygiene to prevent context pollution and role blur.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cwheeler67](https://clawhub.ai/user/cwheeler67)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to coordinate complex, multi-step tasks through defined researcher, builder, editor, and operator roles. It is intended for tasks where explicit handoff contracts and memory hygiene reduce role blur and context pollution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Memory logging could preserve temporary discussion, external content, or sensitive context longer than intended.

Mitigation: Show proposed daily or long-term memory entries to the user before saving them, especially when they come from external content or transient task discussion.

## Reference(s):

- [Handoff Contract Template](references/handoff-contract.md)
- [ClawHub Skill Page](https://clawhub.ai/cwheeler67/skills/team-agents-orchestrator)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Structured handoff contracts, role-scoped task summaries, concise final results, unresolved risks, and next actions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
