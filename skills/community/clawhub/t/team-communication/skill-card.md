## Description:

Team Communication guides agents on using sessions_send and sessions_list for internal team coordination, task handoffs, help requests, and status updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ebly](https://clawhub.ai/user/ebly)

### License/Terms of Use:


## Use Case:

Agents and team operators use this skill to route messages to named team sessions, request help, assign testing, coordinate design or support work, and keep communication concise.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Messages sent with sessions_send may become shared task context and could expose secrets or private data.

Mitigation: Do not include secrets or private data unless sharing that information is explicitly appropriate.

Risk: The documented session keys are team-specific and may misroute messages in teams that use different session names.

Mitigation: Install only for teams that use these session keys, and verify available sessions with sessions_list before relying on the directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ebly/skills/team-communication)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language guidance with predefined team session keys.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
