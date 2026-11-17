## Description:

Coordinate team task execution on OpenAnt. Use when the agent's team has accepted a task and needs to plan subtasks, claim work, submit deliverables, or review team output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ant-1984](https://clawhub.ai/user/ant-1984)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to coordinate OpenAnt team tasks after a task has been accepted, including planning subtasks, claiming work, submitting deliverables, reviewing output, and checking progress.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to perform shared OpenAnt workflow changes without confirmation.

Mitigation: Add explicit confirmation for state-changing operations such as creating subtasks, submitting work, approving or rejecting reviews, and submitting the parent task.

Risk: The skill includes parent task submission guidance outside the declared allowed tool scope.

Mitigation: Correct the declared allowed-tools if parent task submission is intended, or remove parent task submission guidance from this release.

## Reference(s):


## Skill Output:

**Output Type(s):** [shell commands, guidance, text]

**Output Format:** [Markdown guidance with inline bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands are expected to append --json for structured OpenAnt CLI output.]

## Skill Version(s):

0.1.1 (source: server release metadata, released 2026-05-25)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
