## Description:

Manages VMware AVI virtual services, pool members, certificates, analytics, and service engines, and troubleshoots AKO Kubernetes operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zw008](https://clawhub.ai/user/zw008)

### License/Terms of Use:

MIT-0

## Use Case:

Infrastructure engineers and Kubernetes operators use this skill to inspect and manage AVI load balancing and diagnose AKO ingress, pod, configuration, and synchronization issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Controller credentials and Kubernetes access can expose infrastructure data and enable changes to live traffic or AKO configuration.

Mitigation: Grant only the intended controller and cluster access, inspect the target and change preview, and confirm before applying state changes. Review the image reference when using a container deployment.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/zw008/skills/vmware-avi)
- [Project homepage (release metadata)](https://github.com/vmware-skills/VMware-AVI)
- [Setup guide](artifact/references/setup-guide.md)
- [Capabilities and risk gates](artifact/references/capabilities.md)
- [CLI reference](artifact/references/cli-reference.md)
- [Agent guardrails](artifact/references/agent-guardrails.md)

## Skill Output:

**Output Type(s):** [Text, Analysis, Shell commands, Configuration guidance]

**Output Format:** [Markdown with command examples and operational findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings depend on the configured AVI Controller and Kubernetes context; state-changing actions use confirmation gates.]

## Skill Version(s):

2.5.2 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
