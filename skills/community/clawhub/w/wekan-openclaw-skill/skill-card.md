## Description:

Manage a self-hosted Trello-like board via `wekancli`, including creating, moving, and archiving cards, lists, and boards on a WeKan server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[madsmith](https://clawhub.ai/user/madsmith)

### License/Terms of Use:


## Use Case:

Developers, operators, and team agents use this skill to inspect and update self-hosted WeKan boards from a configured agent environment. It is suited for task-board workflows such as creating cards, moving work between lists, archiving items, and retrieving board details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify live WeKan boards using the configured token.

Mitigation: Use a dedicated least-privileged WeKan account and require explicit confirmation before create, move, archive, or delete operations.

Risk: Authentication tokens or login output could be exposed in chat or logs.

Mitigation: Avoid admin tokens, keep `WEKAN_TOKEN` secret, and do not echo token values or login output into shared transcripts.

Risk: The CLI is installed from an unpinned Git source.

Mitigation: Review and pin a trusted `wekan-cli` revision before deployment.

Risk: Delete operations may be destructive and may require admin privileges.

Mitigation: Prefer archive and restore workflows, and reserve delete APIs for reviewed admin-only maintenance.

## Reference(s):

- [Wekan Skill on ClawHub](https://clawhub.ai/madsmith/skills/wekan-openclaw-skill)
- [CLI Examples](references/cli-examples.md)
- [User Installation Notes](references/user-install.md)
- [wekan-cli install source](https://github.com/madsmith/wekan_cli.git)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce commands that read from or modify a configured WeKan server and may summarize JSON returned by the CLI.]

## Skill Version(s):

1.5.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
