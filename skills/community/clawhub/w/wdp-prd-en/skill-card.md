## Description:

PRD Backlog Conductor manages requirement cards, backlog scheduling, and parallel dispatch of confirmed requirements to background subagents with review and acceptance workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luckystar513](https://clawhub.ai/user/luckystar513)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to capture product requirements as project-specific backlog cards, confirm dispatchable work, coordinate dependencies and conflicts, and move completed implementation through review and acceptance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A project-controlled `.wdp-prd` pointer can direct the skill to read from or write to an unintended location outside the current project.

Mitigation: Before running the skill in an existing or downloaded repository, inspect `.wdp-prd` and proceed only if it points to the intended project directory under the chosen PRD root.

Risk: Dispatch and acceptance workflows can create branches, run subagents, merge code, and update persistent planning files.

Mitigation: Review the scheduling state and resulting changes before acceptance, and run the required integration tests and code review gates before marking a requirement done.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/luckystar513/skills/wdp-prd-en)
- [Requirement card template](references/card-template.md)
- [Test scenarios](references/test-scenarios.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown requirement cards, scheduling summaries, implementation guidance, command-oriented workflow steps, and review reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates per-project backlog files, execution plans, implementation plan archives, and acceptance records.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
