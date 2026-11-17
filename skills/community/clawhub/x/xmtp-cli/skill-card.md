## Description:

Run and script the XMTP CLI to test, debug, and interact with XMTP conversations, groups, messages, permissions, sync, and content commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[humanagent](https://clawhub.ai/user/humanagent)

### License/Terms of Use:

MIT

## Use Case:

Developers and XMTP operators use this skill to set up the XMTP CLI, inspect conversations and inboxes, send messages, manage groups and permissions, sync data, and test content examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet secrets can be exposed if real private keys are pasted into commands, prompts, or `.env` files.

Mitigation: Use ephemeral or test wallets, avoid pasting real private keys, protect `.env` files with strict permissions and source-control exclusion, and limit use to controlled XMTP development environments.

Risk: The skill can run an unpinned external CLI package.

Mitigation: Pin or independently verify the `@xmtp/cli` package version before installing or invoking it.

Risk: Send, group, sync, content, and permissions commands can create real network or account-affecting changes.

Mitigation: Review generated commands before execution and confirm target addresses, group IDs, environments, and permission changes before running them.

## Reference(s):

- [XMTP documentation](https://docs.xmtp.org)
- [XMTP debug agents documentation](https://docs.xmtp.org/agents/debug-agents)
- [XMTP CLI ClawHub skill page](https://clawhub.ai/humanagent/skills/xmtp-cli)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include command examples that affect real XMTP accounts, messages, groups, permissions, or local .env files.]

## Skill Version(s):

1.0.0 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
