## Description:

Complete DevOps toolkit for AI-assisted software development, including release pipeline, license compliance, copyright enforcement, repository visibility guard, identity file protection, manifest reconciliation, and MCP-callable core tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[parkertoddbrooks](https://clawhub.ai/user/parkertoddbrooks)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to guide agents through installing and operating AI DevOps tooling for releases, repository management, license checks, identity-file protection, and safe private-to-public publishing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent hooks, global CLIs, user-scope MCP servers, and release tools can change developer environments and repositories.

Mitigation: Install only in trusted workspaces, run documented dry-runs first, and review enabled hooks and MCP servers before granting repository or publishing access.

Risk: Confirmed unsafe shell-command paths can be risky on untrusted repositories.

Mitigation: Avoid using the affected installer and license-scanning paths on untrusted code until command execution is hardened with argument-vector execution.

Risk: Bundled browser-cookie tooling may read local browser session cookies into automation.

Mitigation: Do not load or use cookie-import features unless that behavior is explicitly intended; prefer isolated browser profiles for automation.

Risk: Repository, release, npm, GitHub, and publishing workflows can act with the user's existing credentials.

Mitigation: Use least-privilege credentials, inspect dry-run output, and require explicit approval before real publish, sync, or release operations.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/parkertoddbrooks/skills/wip-ai-devops-toolbox)
- [Project Homepage](https://github.com/wipcomputer/wip-ai-devops-toolbox)
- [Technical Documentation](TECHNICAL.md)
- [Universal Interface Spec](tools/wip-universal-installer/SPEC.md)
- [Dev Guide](DEV-GUIDE-GENERAL-PUBLIC.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides agent actions across installation, release, compliance, repository-management, and guard workflows.]

## Skill Version(s):

1.9.72 (source: server release, SKILL.md frontmatter, package.json; released 2026-04-21)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
