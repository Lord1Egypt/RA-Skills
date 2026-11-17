## Description:

Create enhanced implementation plans with milestone timelines, data flow diagrams, mockups, and risk tables.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paudyyin](https://clawhub.ai/user/paudyyin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill before complex multi-step implementation work to create repository-aware plans with milestones, data flow, mockups, risks, and bite-sized execution tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated plans may contain incorrect or misleading implementation guidance.

Mitigation: Review each plan before execution and confirm that proposed files, data flows, risks, and tasks match the repository.

Risk: Plans may propose subagent handoff, git add, or git commit commands.

Mitigation: Require explicit approval before executing subagent handoffs or any git staging and commit commands.

Risk: The skill creates persistent planning markdown files in the repository.

Mitigation: Inspect generated docs/plans files before keeping or committing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paudyyin/skills/writing-plans-enhanced)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown implementation plan with headings, diagrams, mockups, risk tables, task steps, code blocks, and command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Plans are intended to be saved as persistent markdown files under docs/plans and reviewed before execution.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
