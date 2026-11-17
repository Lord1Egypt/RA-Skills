## Description:

Run a conversational task list with Inbox, Today, Upcoming, recurring tasks, waiting items, projects, and review loops that stay trustworthy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users use this skill to manage personal or work task lists through conversation, including capture, clarification, recurring work, waiting items, projects, and review loops.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Activation preferences may be saved outside the declared ~/task-list/ storage boundary.

Mitigation: Require clear user opt-in before saving activation preferences and document how to inspect, change, or remove them.

Risk: Task records may contain personal or sensitive commitments in local Markdown files.

Mitigation: Keep task data under ~/task-list/, avoid storing unrelated sensitive details, and make the local files easy for the user to inspect or delete.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/task-list)
- [Skill Homepage](https://clawic.com/skills/task-list)
- [Capture and Clarify](capture-and-clarify.md)
- [Views and Sorting](views-and-sorting.md)
- [Recurrence and Waiting](recurrence-and-waiting.md)
- [Review Rhythm](review-rhythm.md)
- [Workspace Format](workspace-format.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Conversational text and Markdown task records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local Markdown files under ~/task-list/ when the user opts into continuity.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
