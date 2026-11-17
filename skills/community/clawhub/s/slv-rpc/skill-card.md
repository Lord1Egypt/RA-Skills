## Description:

Guides an agent through deploying, managing, updating, and benchmarking Solana RPC nodes across mainnet, testnet, and devnet using Ansible-based SLV workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[poppin-fumi](https://clawhub.ai/user/poppin-fumi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and infrastructure operators use this skill to collect node parameters, generate inventories, and run or review Ansible commands for Solana RPC deployment, lifecycle management, plugin setup, and endpoint benchmarking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to make real infrastructure changes to Solana RPC nodes.

Mitigation: Confirm the target server, generated inventory, selected playbook, and extra variables before execution; run Ansible check mode first when practical.

Risk: Runtime playbooks may come from a mutable local template directory outside the reviewed package.

Mitigation: Verify the exact ~/.slv/template version, source, ownership, and contents before running playbooks; prefer pinned or checksummed playbooks.

Risk: Some workflows may involve disk formatting, ledger cleanup, sudo package installation, or curl-to-shell installer steps.

Mitigation: Manually review these operations before approving them and ensure private keys, tokens, and credentials are never logged or embedded in generated files.

## Reference(s):

- [Slv Rpc on ClawHub](https://clawhub.ai/poppin-fumi/skills/slv-rpc)
- [ERPC Snapshot Network](https://erpc.global/en/)
- [ValidatorsDAO/slv](https://github.com/ValidatorsDAO/slv)
- [Yellowstone gRPC](https://github.com/rpcpool/yellowstone-grpc)
- [Richat](https://github.com/lamports-dev/richat)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and YAML configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate Ansible inventory values and benchmark configuration snippets; recommends confirmation and dry-run before high-impact playbooks.]

## Skill Version(s):

0.13.15 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
