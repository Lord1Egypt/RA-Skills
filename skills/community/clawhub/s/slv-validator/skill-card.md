## Description: <br>
Deploys and manages Solana validators on mainnet and testnet using guided Ansible playbook workflows for Jito, Agave, and Firedancer validator types. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[poppin-fumi](https://clawhub.ai/user/poppin-fumi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, DevOps engineers, and validator operators use this skill to collect deployment variables, generate validator inventory, and run or review Ansible playbook commands for Solana validator deployment, maintenance, migration, and monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup, cleanup, identity-switching, migration, and monitoring commands can materially affect validator infrastructure. <br>
Mitigation: Confirm the target host, validator identity, RPC endpoint, and rollback plan before running playbooks; use dry-run review when uncertain. <br>
Risk: Validator keys, SSH keys, and RPC API keys may be exposed if copied into commands, logs, or generated configuration carelessly. <br>
Mitigation: Keep private keys and API keys out of logs and shell history, verify key paths before execution, and avoid passing secrets directly in visible command lines. <br>
Risk: Incorrect validator type, binary, or version selection can lead to failed starts or incompatible runtime flags. <br>
Mitigation: Verify the selected validator type and installed CLI binary before deployment or switching, especially when moving between Jito, Agave, and Firedancer modes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/poppin-fumi/slv-validator) <br>
- [Publisher profile](https://clawhub.ai/user/poppin-fumi) <br>
- [ValidatorsDAO/slv](https://github.com/ValidatorsDAO/slv) <br>
- [Anza Agave](https://github.com/anza-xyz/agave.git) <br>
- [Jito Solana](https://github.com/jito-foundation/jito-solana.git) <br>
- [Firedancer](https://github.com/firedancer-io/firedancer.git) <br>
- [ERPC Global](https://erpc.global/en/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown with inline shell commands and YAML configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operational guidance for Ansible playbook selection, variable collection, inventory generation, dry-run review, and validator monitoring.] <br>

## Skill Version(s): <br>
0.13.15 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
