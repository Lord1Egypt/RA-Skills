## Description:

Sets up Solana/Anchor development environments, prepares dApps for deployment, runs build/test/deploy workflows, and guides safe devnet/mainnet release operations with verifiable builds, buffer-based upgrades, priority-fee tuning, structured failure recovery, and memory logging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gwapupward-hub](https://clawhub.ai/user/gwapupward-hub)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to prepare Solana and Anchor projects for localnet, devnet, and mainnet-beta deployment. It helps inspect toolchains and project configuration, produce deployment checklists and reports, run build/test/deploy workflows, and triage release failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide high-impact setup and deployment activity on machines with wallets, RPC provider keys, or production deployment authority.

Mitigation: Review before installation in privileged environments, require explicit approval before mainnet actions, and confirm signer, RPC, cluster, and authority state before deployment.

Risk: Installer and toolchain guidance may involve unsafe or insufficiently verified installation patterns.

Mitigation: Prefer pinned and verified tool installers, record selected versions, and avoid replacing global tools without explicit approval.

Risk: Deployment reports or memory files could expose API-bearing RPC URLs or other sensitive operational details.

Mitigation: Redact full RPC URLs, API-bearing endpoints, private keys, seed material, and production secrets before writing reports or memory logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gwapupward-hub/skills/solana-deploy-engineer)
- [Anchor framework](https://github.com/coral-xyz/anchor)
- [Anza Solana CLI installer](https://release.anza.xyz/stable/install)
- [Solana devnet faucet](https://faucet.solana.com)
- [Solana devnet RPC endpoint](https://api.devnet.solana.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code blocks, checklists, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or update deployment checklists, release reports, environment examples, and memory log entries.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
