## Description:

Diagnoses VMware, vSphere, ESXi, and NSX incidents by correlating collected evidence, ranking root-cause hypotheses, and recommending next checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zw008](https://clawhub.ai/user/zw008)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and infrastructure engineers use this skill to investigate VMware incidents from collected events and logs, build an incident timeline, assess likely causes, and decide what to check next. It records investigation evidence locally and routes remediation to separate skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security review coverage is partial because three local references could not be resolved.

Mitigation: Review the unresolved references and available security evidence before installing.

Risk: Investigation case records and the audit trail may contain sensitive operational details; optional HTTPS uses bearer tokens and TLS key material.

Mitigation: Keep secrets out of case evidence, protect case folders and audit data, and store HTTPS tokens and TLS files as secrets.

## Reference(s):

- [VMware Debug project](https://github.com/vmware-skills/VMware-Debug)
- [Setup guide](references/setup-guide.md)
- [VM performance investigation](references/vm-performance.md)
- [Host alarm investigation](references/host-alarms.md)
- [Agent guardrails](references/agent-guardrails.md)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown, Guidance]

**Output Format:** [Structured incident timelines, ranked hypotheses, next-check recommendations, and Markdown case records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Analysis is based on evidence gathered by the caller; optional case records are written locally.]

## Skill Version(s):

2.4.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
