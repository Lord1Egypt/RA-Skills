## Description:

Helps users install, configure, use, and troubleshoot the trends-skill-tool CLI for token management, trading, wallet queries, creator rewards, and error recovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[milesxyz](https://clawhub.ai/user/milesxyz)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to get operational guidance for the trends-skill-tool CLI, including setup, wallet configuration, read-only account queries, quote-first trades, token creation, reward claims, and deterministic troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill guides financial write actions for token creation, buying, selling, and reward claims, and the security summary notes confirmation bypasses.

Mitigation: Use quote-first or status-first preflights, require explicit confirmation for writes by default, avoid session-level bypass, and verify transaction parameters before execution.

Risk: The skill installs and operates a wallet-enabled CLI from a global npm package that is not pinned in the provided evidence.

Mitigation: Install only in environments where this dependency posture is acceptable, verify the installed CLI version and help output, and prefer a dedicated low-value wallet.

Risk: The wallet initialization workflow can overwrite an existing keypair with --force.

Mitigation: Do not use wallet init --force unless the previous keypair is backed up and the user understands that overwriting it can permanently remove access to assets.

Risk: Private keys, seed phrases, secretKey arrays, or raw keypair file contents may be exposed if a user asks for backup or debugging help.

Mitigation: Refuse to handle or echo key material, avoid commands that print key files, and continue only with address-level verification such as wallet address.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/milesxyz/skills/trends)
- [Publisher profile](https://clawhub.ai/user/milesxyz)
- [Install and Setup](references/install-and-setup.md)
- [Command Recipes](references/command-recipes.md)
- [Error Playbook](references/error-playbook.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes confirmation-gated write guidance, quote-first trade preflights, wallet-safety handling, and deterministic error-to-fix mappings.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
