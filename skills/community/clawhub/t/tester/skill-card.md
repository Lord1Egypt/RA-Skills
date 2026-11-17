## Description:

Manage GitHub issues by listing, filtering, spawning fix agents, creating pull requests, and tracking review comments using the authenticated GitHub CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tsiontesfayechromaway](https://clawhub.ai/user/tsiontesfayechromaway)

### License/Terms of Use:


## Use Case:

Developers and repository maintainers use this skill to triage GitHub issues, delegate fixes to agents, open pull requests, and monitor review feedback in repositories accessible to the authenticated GitHub CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents may change repository content or create pull requests based on issue text that can contain untrusted instructions.

Mitigation: Restrict work to a dedicated repository or worktree and require human review before commits are pushed, pull requests are opened, or comments are posted.

Risk: GitHub credentials can grant broad repository permissions if over-scoped or exposed through environment variables.

Mitigation: Use least-privilege GitHub authentication and prefer GitHub CLI credential storage over exported tokens.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tsiontesfayechromaway/skills/tester)
- [Publisher profile](https://clawhub.ai/user/tsiontesfayechromaway)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an installed and authenticated GitHub CLI with repository access.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
