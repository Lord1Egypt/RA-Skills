## Description:

Standard PR review and merge workflow for task-driven development. Use when reviewing a programmer agent PR linked to a task, deciding merge vs change request, handling post-merge actions (Trello + branch cleanup), and sending a clear outcome handoff.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anikgnr](https://clawhub.ai/user/anikgnr)

### License/Terms of Use:


## Use Case:

Developers and reviewer agents use this skill to review task-linked pull requests, decide whether to merge or request changes, complete Trello and branch cleanup after merge, and hand off the final outcome.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow includes actions that can change project state, including PR review and merge decisions, Trello card updates, and task branch deletion.

Mitigation: Install this skill only where the agent is authorized to perform those task-scoped repository and Trello actions.

Risk: Branch cleanup could remove the wrong branch if the task branch is not clearly distinguished from protected branches.

Mitigation: Confirm the branch is the task branch before deletion and preserve the main branch.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anikgnr/skills/task-review-workflow)
- [Publisher profile](https://clawhub.ai/user/anikgnr)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or plain text review feedback with optional shell commands and merge handoff status.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include approve or merge notes, change-request comments, local validation command suggestions, and post-merge action guidance.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
