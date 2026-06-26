## Description: <br>
Ansible playbooks and templates to deploy, manage, and update Solana RPC nodes on mainnet, testnet, and devnet with support for RPC, indexing, and gRPC. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[poppin-fumi](https://clawhub.ai/user/poppin-fumi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to guide deployment and lifecycle management of Solana RPC nodes across mainnet, testnet, and devnet. It helps collect node configuration, prepare inventory values, and propose Ansible commands for RPC, indexing, gRPC, and validator-client setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide high-impact remote Ansible playbooks for Solana RPC servers, including service restarts, firewall changes, disk formatting, ledger cleanup, and key copying. <br>
Mitigation: Confirm the exact playbook, inventory target, and variables before execution; limit inventory targets; run Ansible check mode first; and review any restart, firewall, disk, ledger, or key-copying step before applying it. <br>
Risk: The security review notes that runtime playbooks in ~/.slv/template are not included in the package. <br>
Mitigation: Use the skill only when you trust the SLV/ValidatorsDAO toolchain and can inspect the exact ~/.slv/template Ansible playbooks that will run. <br>
Risk: Private keys, SSH credentials, and API secrets could be exposed if pasted into agent chat or logs. <br>
Mitigation: Do not paste private keys or API secrets into the agent chat; rely on local SSH configuration, key files, or the SSH agent where possible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/poppin-fumi/slv-rpc) <br>
- [README](artifact/README.md) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Agent behavior guide](artifact/AGENT.md) <br>
- [Example inventory](artifact/examples/inventory.yml) <br>
- [Yellowstone gRPC](https://github.com/rpcpool/yellowstone-grpc) <br>
- [Richat](https://github.com/lamports-dev/richat) <br>
- [ERPC](https://erpc.global/en/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with shell commands and YAML or TOML configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose Ansible inventory values, geyserbench config.toml content, health-check commands, and dry-run playbook commands after collecting required user inputs.] <br>

## Skill Version(s): <br>
0.13.15 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
