## Description:

Run a Trello-backed closed-loop delivery workflow for OpenClaw multi-agent execution that moves cards across workflow lists, uses local-first routing, requires reviewer-gated completion, and retries rejected work until accepted or blocked.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeremiahdingal](https://clawhub.ai/user/jeremiahdingal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and delivery managers use this skill to let an agent coordinate Trello cards through a defined intake, scoping, routing, build, review, and completion workflow while preserving reviewer control over final acceptance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill updates Trello cards, descriptions, comments, and list placement using Trello credentials.

Mitigation: Use credentials limited to the intended Trello workspace or board and review trello-workflow-map.json before running.

Risk: Task objectives, acceptance criteria, risk notes, and review outcomes may be written to Trello cards.

Mitigation: Avoid placing sensitive task details in cards unless those details are appropriate for Trello.

Risk: Moving work to Done without real review would weaken the workflow's acceptance gate.

Mitigation: Require explicit reviewer ACCEPT against the original objective before any card is moved to Done.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, API Calls, Configuration, Guidance]

**Output Format:** [Markdown summary with Trello card metadata and workflow status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Trello API credentials and a workspace-level trello-workflow-map.json; updates Trello cards, comments, descriptions, and list placement.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
