## Description:

AI plugin for 1Password secrets that resolves op:// references at startup and gives agents tools to read, list, and write secrets through a service account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[parkertoddbrooks](https://clawhub.ai/user/parkertoddbrooks)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to keep API keys, tokens, and credentials in 1Password while allowing compatible agents to resolve configured secrets or request vault items at runtime.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP server can turn tool arguments into local shell commands while holding the 1Password service-account token.

Mitigation: Do not enable the MCP server until command execution uses argument-vector execution and input validation.

Risk: A broadly scoped service account could expose more vault items than the agent needs.

Mitigation: Use a custom vault with the narrowest practical access and prefer read_items permissions.

Risk: Write access allows an agent to create or update 1Password items.

Mitigation: Avoid write_items unless the workflow requires it and review write operations before use.

Risk: Secret values may be exposed if copied into chat, logs, source files, or terminal output.

Mitigation: Keep returned secrets in memory, never log or paste them, and rotate any secret that is exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/parkertoddbrooks/skills/wip-1password)
- [TECHNICAL.md](TECHNICAL.md)
- [SKILL.md](SKILL.md)
- [OpenClaw plugin manifest](openclaw.plugin.json)
- [Universal Interface Spec](https://github.com/wipcomputer/wip-ai-devops-toolbox/blob/main/tools/wip-universal-installer/SPEC.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code, shell commands, JSON configuration, and agent tool calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include secret-handling instructions; returned secret values should remain in memory and not be logged or pasted into chat.]

## Skill Version(s):

0.2.2 (source: CHANGELOG, package.json, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
