## Description:

Ansible playbooks and templates for deploying and managing Solana gRPC Geyser streaming nodes with Yellowstone or Richat plugins.

This skill is ready for commercial/non-commercial use.

## Publisher:

[poppin-fumi](https://clawhub.ai/user/poppin-fumi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Solana infrastructure operators use this skill to plan, configure, and run Ansible workflows for deploying or maintaining gRPC Geyser streaming nodes, including Yellowstone gRPC or Richat plugin builds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote administration playbooks can change node state, restart services, or affect production availability.

Mitigation: Run dry-run or check mode first, review planned variables and target hosts, and require change approval before production restarts or updates.

Risk: Runtime playbooks are resolved from ~/.slv/template/ and may differ from the artifact's reference copies.

Mitigation: Review the resolved template directory and playbook path before execution, and install only from trusted SLV template sources.

Risk: Automatic prerequisite setup may install packages or use elevated package-manager commands on the operator host.

Mitigation: Prefer manually installing pinned prerequisites, and review setup behavior before running automatic installation paths.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/poppin-fumi/skills/slv-grpc-geyser)
- [Yellowstone gRPC](https://github.com/rpcpool/yellowstone-grpc)
- [Richat](https://github.com/lamports-dev/richat)
- [ERPC Snapshot Network](https://erpc.global/en/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and YAML inventory examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces deployment guidance and command proposals; users should review before running commands on target hosts.]

## Skill Version(s):

0.13.15 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
