## Description: <br>
Deploys and manages Solana gRPC Geyser streaming nodes with Ansible guidance for Yellowstone gRPC or Richat plugin configurations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[poppin-fumi](https://clawhub.ai/user/poppin-fumi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and infrastructure operators use this skill to configure, deploy, update, and monitor Solana gRPC Geyser streaming nodes over SSH with Ansible. It helps collect deployment variables, generate inventory configuration, and run lifecycle playbooks after user confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to manage Solana infrastructure over SSH and run powerful local SLV Ansible playbooks. <br>
Mitigation: Verify the generated inventory, target host, and intended playbook before execution, and run Ansible with --check before applying changes. <br>
Risk: Runtime playbooks may come from the local SLV template directory rather than only the artifact's reference files. <br>
Mitigation: Inspect and pin the SLV template directory under ~/.slv/template/ before deployment or updates. <br>
Risk: The setup script can install local prerequisites through package managers or pip. <br>
Mitigation: Run scripts/setup.sh only after reviewing and accepting its local package-manager changes. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/poppin-fumi/slv-grpc-geyser) <br>
- [Yellowstone gRPC](https://github.com/rpcpool/yellowstone-grpc) <br>
- [Richat](https://github.com/lamports-dev/richat) <br>
- [ValidatorsDAO SLV](https://github.com/ValidatorsDAO/slv) <br>
- [ERPC Global](https://erpc.global) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and YAML inventory configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Ansible dry-run and deployment commands; users should review generated inventory and target hosts before execution.] <br>

## Skill Version(s): <br>
0.13.15 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
