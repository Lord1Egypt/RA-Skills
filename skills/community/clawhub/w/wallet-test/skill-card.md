## Description:

A multi-chain wallet skill for AI agents, with local sandbox signing, secure PIN handling, and configurable risk controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[willjefferson0](https://clawhub.ai/user/willjefferson0)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill to install and operate a local wallet sandbox, inspect wallet status and addresses, bind wallets, sign messages or transactions, transfer assets, and review wallet policy controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and upgrades by downloading remote scripts and binaries without pinned integrity checks.

Mitigation: Review the installer and binaries before use, and require publisher-supplied pinning and verification for remote assets.

Risk: The skill may print or expose bearer tokens used for authenticated wallet sandbox calls.

Mitigation: Do not display bearer tokens in chat or logs; read them only from local configuration when making authenticated sandbox requests.

Risk: Authenticated sandbox calls can affect wallet state or execute transactions.

Mitigation: Require explicit user confirmation before transaction execution, reinstall, upgrade, or uninstall actions, and validate that API calls target the trusted local sandbox origin.

Risk: The skill includes a remote marketplace command-execution workflow unrelated to wallet operations.

Mitigation: Remove or disable remote marketplace installation and command execution paths before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/willjefferson0/skills/wallet-test)
- [Publisher profile](https://clawhub.ai/user/willjefferson0)
- [Claw Wallet skill homepage](https://github.com/ClawWallet/Claw-Wallet-Skill)
- [Claw Wallet skill distribution host](https://www.clawwallet.cc/skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, API request guidance, and wallet status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local sandbox URLs, wallet addresses, UID values, and configuration paths; sensitive tokens should not be printed.]

## Skill Version(s):

0.1.19 (source: server release evidence and skill.yml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
