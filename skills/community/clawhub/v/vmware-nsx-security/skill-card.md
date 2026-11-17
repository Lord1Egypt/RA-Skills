## Description:

Manages VMware NSX security, including distributed firewall policies and rules, security groups, VM tags, Traceflow diagnostics, and IDS/IPS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zw008](https://clawhub.ai/user/zw008)

### License/Terms of Use:

MIT-0

## Use Case:

Network and security administrators use this skill to inspect and manage NSX distributed firewall policies, security groups, VM tags, Traceflow, and IDS/IPS settings for microsegmentation and troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports partial analysis because a local path-like reference in SKILL.md did not match a bundled artifact, and notes setup guidance includes NSX networking and vSphere monitoring tools outside the stated security scope.

Mitigation: Keep this skill focused on NSX security work, route networking or monitoring tasks to their dedicated skills, and review the unavailable reference if complete evidence coverage is needed.

## Reference(s):

- [Setup guide](artifact/references/setup-guide.md)
- [CLI reference](artifact/references/cli-reference.md)
- [Agent guardrails](artifact/references/agent-guardrails.md)
- [Capabilities reference](artifact/references/capabilities.md)
- [Project homepage](https://github.com/vmware-skills/VMware-NSX-Security)
- [ClawHub release page](https://clawhub.ai/zw008/skills/vmware-nsx-security)

## Skill Output:

**Output Type(s):** [Analysis, API Calls, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance and structured tool results, with shell commands when using the CLI.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include findings, proposed NSX changes, or setup instructions depending on the task.]

## Skill Version(s):

1.17.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
