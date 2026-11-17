## Description:

Track and report token usage and estimated cost for the current conversation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zty-f](https://clawhub.ai/user/zty-f)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent for current-session token usage, estimated cost, cache hit rate, and context usage, especially after long or complex conversations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may proactively surface token and cost information after long or complex work, even when a user expects reports only on direct request.

Mitigation: Narrow the trigger wording during deployment if usage reports should appear only when explicitly requested.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown summary with token, cost, cache, and context metrics]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Current-session metrics only; actual cost from session_status is authoritative.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
