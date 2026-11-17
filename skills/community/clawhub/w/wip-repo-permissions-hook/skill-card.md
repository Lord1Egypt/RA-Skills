## Description:

Repo visibility guard. Blocks repos from going public without a -private counterpart.

This skill is ready for commercial/non-commercial use.

## Publisher:

[parkertoddbrooks](https://clawhub.ai/user/parkertoddbrooks)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and repository maintainers use this skill to check whether a GitHub repository can be made public under a public/private repository workflow. It can run as a CLI, Claude Code hook, OpenClaw plugin, or MCP tool to check individual repositories and audit public repositories in an organization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The guard is advisory and can miss cases because hook parsing and audit behavior are limited.

Mitigation: Review the skill before relying on it, compensate for missed command forms and the 200-repository audit limit, and use server-side GitHub organization controls for critical visibility policy.

Risk: The hook can fail open and may allow an action when input parsing or execution fails.

Mitigation: Treat local hook behavior as a convenience check, not a complete enforcement boundary, and add independent repository visibility controls.

Risk: The MCP dependency is unpinned.

Mitigation: Pin or otherwise control dependency versions before deployment in sensitive environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/parkertoddbrooks/skills/wip-repo-permissions-hook)
- [Project Homepage](https://github.com/wipcomputer/wip-ai-devops-toolbox)
- [npm Package](https://www.npmjs.com/package/@wipcomputer/wip-repo-permissions-hook)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with JSON configuration examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and GitHub CLI access for repository checks.]

## Skill Version(s):

1.9.72 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
