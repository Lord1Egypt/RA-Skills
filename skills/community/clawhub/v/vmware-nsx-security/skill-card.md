## Description:

Manage VMware NSX distributed firewall policies and rules, security groups, VM tags, Traceflow diagnostics, and IDPS profiles and status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zw008](https://clawhub.ai/user/zw008)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and infrastructure security engineers use this skill to inspect and manage NSX distributed firewall rules and groups, tag VMs, trace packet paths, and review IDPS configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A DFW rule or VM tag change can alter traffic enforcement or leave intended VMs outside protection.

Mitigation: Check target, group membership, DFW exclusions, and rule order; verify the intended path with Traceflow before enabling deny rules. Review delete previews before confirming a deletion.

Risk: The supplied security scan is partial, and it notes a mismatch between the security scope and setup guidance that also covers networking and monitoring.

Mitigation: Review the setup and networking/monitoring guidance and versioning for the intended deployment before installation; treat the scan verdict as incomplete evidence.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/zw008/skills/vmware-nsx-security)
- [Project homepage](https://github.com/vmware-skills/VMware-NSX-Security)
- [Setup guide](artifact/references/setup-guide.md)
- [Capabilities reference](artifact/references/capabilities.md)
- [CLI reference](artifact/references/cli-reference.md)
- [Agent guardrails](artifact/references/agent-guardrails.md)
- [Detailed guide](artifact/references/detailed-guide.md)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Shell commands, Configuration, Operational guidance]

**Output Format:** [Structured JSON tool results and Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results reflect the configured NSX Manager target; write operations can change security policy and VM tags.]

## Skill Version(s):

1.17.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
