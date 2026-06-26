## Description: <br>
Sets up Solana/Anchor development environments, prepares dApps for deployment, runs build/test/deploy workflows, and guides safe devnet/mainnet release operations with verifiable builds, buffer-based upgrades, priority-fee tuning, structured failure recovery, and memory logging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gwapupward-hub](https://clawhub.ai/user/gwapupward-hub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and deployment engineers use this skill to prepare Solana and Anchor projects for localnet, devnet, and mainnet-beta releases. It helps inspect toolchains and project configuration, produce safe deployment commands and checklists, troubleshoot failures, and record deployment decisions without exposing secrets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mainnet deployment guidance can affect production Solana programs, spend real SOL, or change upgrade authority if commands are executed without review. <br>
Mitigation: Require explicit confirmation for mainnet actions, rehearse the same commit on devnet, use dedicated mainnet RPC, and review buffer, authority, priority-fee, and verification steps before execution. <br>
Risk: Wallet keypairs, seed phrases, private keys, RPC credentials, and custody paths are sensitive and may be exposed through logs or generated notes. <br>
Mitigation: Use hardware wallets or Squads multisig for production authority, keep raw secrets out of chat, memory files, and commits, and record only public keys, paths, and placeholder values. <br>
Risk: Generated commands and checklists may be wrong for a repository's actual Solana, Anchor, Rust, Node, cluster, or program-ID configuration. <br>
Mitigation: Inspect project files and installed versions first, verify cluster and program IDs before deployment, and rerun the narrowest validation step after any fix. <br>


## Reference(s): <br>
- [Solana Deploy Engineer on ClawHub](https://clawhub.ai/gwapupward-hub/solana-deploy-engineer) <br>
- [Anza Solana CLI Installer](https://release.anza.xyz/stable/install) <br>
- [Anchor Framework](https://github.com/coral-xyz/anchor) <br>
- [Solana Devnet RPC](https://api.devnet.solana.com) <br>
- [Solana Faucet](https://faucet.solana.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, checklists, and structured deployment notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce deployment reports, release checklists, and memory log entries for Solana deployment workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
