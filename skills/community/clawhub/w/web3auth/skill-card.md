## Description:

Guides developers integrating MetaMask Embedded Wallets across web, mobile, game, and server applications, including authentication, wallet configuration, and SDK migrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[metamask](https://clawhub.ai/user/metamask)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to plan and implement embedded-wallet integrations, configure social or custom-JWT login, troubleshoot wallet-address mismatches, and migrate SDK versions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet private keys, JWTs, and environment values may be exposed during integration or debugging.

Mitigation: Keep keys and credentials out of shared prompts, logs, and committed files; review handling before exporting private keys.

Risk: Unreviewed external examples or package installations may introduce unsafe changes.

Mitigation: Review live documentation and examples, approve installations, and prefer pinned or reviewed package sources.

Risk: Changing production wallet configuration can yield different wallet addresses.

Mitigation: Preserve the client ID, Sapphire network, auth connection, and key settings when updating an existing integration.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/metamask/skills/web3auth)
- [MetaMask Embedded Wallets documentation](https://docs.metamask.io/embedded-wallets/)
- [Embedded Wallets dashboard guide](https://docs.metamask.io/embedded-wallets/dashboard/)
- [Embedded Wallets migration guides](https://docs.metamask.io/embedded-wallets/migration-guides/)
- [Authentication reference](references/authentication.md)
- [Platform reference](references/platforms.md)
- [Official example index](references/examples.md)

## Skill Output:

**Output Type(s):** [Guidance, Code, Configuration instructions, Shell commands]

**Output Format:** [Markdown with inline code and code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Platform-specific integration and migration guidance.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
