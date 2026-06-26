## Description: <br>
Vmware Pilot designs, supervises, and manages multi-step VMware workflows across companion skills with approval gates, audit logging, state persistence, and rollback support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zw008](https://clawhub.ai/user/zw008) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Infrastructure operators and developers use this skill to plan and supervise cross-skill VMware tasks such as clone-and-test changes, incident response, rolling maintenance, compliance scans, and AKO-aware deployments with review points before high-impact actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: High-impact VMware workflows can affect VM power state, deletion, networking, storage, Kubernetes resources, or guest execution. <br>
Mitigation: Require explicit human approval before those changes and run companion skills with least-privilege accounts. <br>
Risk: Workflow parameters could expose passwords or kubeconfigs if users pass secrets directly through the orchestration flow. <br>
Mitigation: Do not pass passwords or kubeconfigs through workflow parameters; rely on the companion skills' normal authentication mechanisms. <br>
Risk: Local audit and baseline files may contain operationally sensitive infrastructure history. <br>
Mitigation: Protect ~/.vmware/audit.db and baseline files with appropriate filesystem permissions and operational handling. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zw008/skills/vmware-pilot) <br>
- [Project homepage](https://github.com/zw008/VMware-Pilot) <br>
- [Capabilities](references/capabilities.md) <br>
- [Integration Patterns](references/integration-patterns.md) <br>
- [Setup Guide](references/setup-guide.md) <br>
- [Workflow Design](references/workflow-design.md) <br>
- [Templates](references/templates.md) <br>
- [CLI Reference](references/cli-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and YAML or JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces workflow plans, approval checkpoints, rollback guidance, setup snippets, and companion-skill routing guidance.] <br>

## Skill Version(s): <br>
1.6.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
