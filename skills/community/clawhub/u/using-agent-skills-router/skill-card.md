## Description:

Route ambiguous agent work to the right skill, command style, and effort level.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zack-dev-cm](https://clawhub.ai/user/zack-dev-cm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to route ambiguous agent requests to an appropriate skill, workflow, or direct response path while keeping effort proportional to the task.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can route high-risk requests such as credential, deletion, production, or release work to an insufficient review path if the agent ignores its selection rules.

Mitigation: Follow the skill's high-risk routing rule and apply normal confirmation practices for risky edits, destructive commands, credentials, production systems, and releases.

Risk: The selected downstream skill or workflow may introduce behavior outside this router's clean security profile.

Mitigation: Review and rely on the security posture of the selected underlying skill before executing risky changes.

## Reference(s):

- [Routing Patterns](references/routing-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Short plain-text or Markdown routing response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a route, reason, and next action for the agent.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
