## Description:

Diagnoses VMware, vSphere, ESXi, and NSX incidents by correlating evidence into a timeline, ranking likely causes, and suggesting next checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zw008](https://clawhub.ai/user/zw008)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and VMware administrators use this skill to investigate incidents from collected events, logs, and companion-skill results. It builds a timeline, ranks hypotheses, records a local case history, and recommends follow-up checks without connecting to or changing VMware systems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment is medium confidence and partial because three local references could not be resolved.

Mitigation: Review the unresolved references and assess the complete skill contents before relying on the scan result.

Risk: Local case records can contain sensitive host, address, log, and event details and persist until deleted.

Mitigation: Keep case records access-controlled, never include credentials or secrets, and delete cases when they are no longer needed.

## Reference(s):

- [ClawHub release](https://clawhub.ai/zw008/skills/vmware-debug)
- [Project homepage](https://github.com/vmware-skills/VMware-Debug)
- [Capabilities](references/capabilities.md)
- [Event envelope](references/event-envelope.md)
- [Routing guide](references/routing.md)
- [Setup guide](references/setup-guide.md)
- [CLI reference](references/cli-reference.md)
- [Agent guardrails](references/agent-guardrails.md)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown, Guidance]

**Output Format:** [Structured incident timeline and ranked hypotheses, with next-check guidance; case records in JSON and Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Case records and a separate audit trail are written locally; no VMware API calls or remediation are performed.]

## Skill Version(s):

2.3.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
