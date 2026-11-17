## Description:

Provides shared Knowledge Planet CLI guidance for authentication, diagnostics, direct API calls, share-link construction, safe write/delete rules, NPS feedback prompts, and common error handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zsxq](https://clawhub.ai/user/zsxq)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to operate zsxq-cli for Knowledge Planet authentication, account diagnostics, direct API calls, share-link generation, and safe handling of write or delete workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide zsxq-cli actions against a user's Knowledge Planet account, including raw API calls, writes, deletes, and NPS feedback submission.

Mitigation: Review and explicitly approve write, delete, raw API, and feedback actions before execution, and confirm resource IDs before modifying or deleting content.

Risk: Authentication tokens grant account access and could be exposed if printed or shared.

Mitigation: Do not display, log, or share authentication tokens; use zsxq-cli status and diagnostic commands without revealing credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zsxq/skills/zsxq-shared)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls]

**Output Format:** [Markdown guidance with inline shell command examples and URL templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires zsxq-cli and an authenticated Knowledge Planet account for account operations.]

## Skill Version(s):

1.3.1 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
