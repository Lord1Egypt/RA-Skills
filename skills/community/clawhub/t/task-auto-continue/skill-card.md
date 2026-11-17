## Description:

Checks a workspace in_progress.md file for unfinished tasks and reminds the agent to continue them.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to detect unfinished workspace tasks and prompt continuation of work that may otherwise be interrupted.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may prompt an agent to continue tasks from in_progress.md without clear user confirmation.

Mitigation: Review in_progress.md and confirm the intended actions before letting the agent continue work from it.

Risk: The skill depends on the trustworthiness of a workspace-local task file.

Mitigation: Install and use it only in workspaces where the contents of in_progress.md are expected and trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freedompixels/skills/task-auto-continue)
- [ClawHub publisher profile](https://clawhub.ai/user/freedompixels)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown or plain text status reminders]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports task status from workspace in_progress.md; the artifact states it does not modify files.]

## Skill Version(s):

1.2.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
