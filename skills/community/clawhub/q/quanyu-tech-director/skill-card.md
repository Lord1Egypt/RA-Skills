## Description:

A software development director skill for Quanyu Tech that activates a project-manager mode for dispatching tasks, tracking progress, handling timeouts, and reporting results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[worm-tribe](https://clawhub.ai/user/worm-tribe)

### License/Terms of Use:

MIT-0

## Use Case:

Project managers and development leads use this skill to coordinate software development, review, and deployment work through delegated agent tasks. It emphasizes task sizing, status tracking in TASK-TRACKER.json, timeout handling, and progress reports to the designated founder or owner.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mandatory delegation can cause agent work to proceed beyond the user's intended scope.

Mitigation: Require user approval for delegated development, review, build, deployment, and follow-up tasks before agents are launched.

Risk: TASK-TRACKER.json updates may modify project state without clear approval boundaries.

Mitigation: Confirm the tracker path and whether file writes require approval before enabling the skill in a workspace.

Risk: Timeout handling can create repeated follow-up tasks without an explicit retry limit.

Mitigation: Set a maximum retry count and require review of intermediate outputs before continuing timed-out work.

Risk: Progress reports may be sent to an ambiguous founder or owner recipient.

Mitigation: Define the reporting recipient and acceptable report contents before use.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown and structured task-tracking updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update TASK-TRACKER.json and produce short status reports during task dispatch, completion, timeout, or failure.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
