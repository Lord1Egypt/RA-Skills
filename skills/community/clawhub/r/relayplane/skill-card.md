## Description:

Agent ops layer for OpenClaw: observability, governance, cost optimization, and automatic failover for LLM traffic.

This skill is ready for commercial/non-commercial use.

## Publisher:

[relayplane](https://clawhub.ai/user/relayplane)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use RelayPlane to configure an optional local LLM proxy for model routing, usage visibility, budget controls, and fallback behavior in OpenClaw or compatible SDK-based tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive agent traffic may be routed through mutable globally installed RelayPlane packages.

Mitigation: Review the RelayPlane package source and install an exact trusted package version before use.

Risk: Exporting provider BASE_URL variables can route all compatible SDK traffic through the proxy without the documented fallback behavior.

Mitigation: Prefer the OpenClaw relayplane configuration method and avoid provider BASE_URL overrides unless the routing impact is intentionally accepted.

Risk: Telemetry or proxy routing may be unsuitable for sensitive workloads.

Mitigation: Turn telemetry off or run the proxy in offline mode for sensitive workloads.

## Reference(s):

- [ClawHub RelayPlane Skill Page](https://clawhub.ai/relayplane/skills/relayplane)
- [RelayPlane Documentation](https://relayplane.com/docs)
- [RelayPlane Homepage](https://relayplane.com)
- [RelayPlane npm Package](https://www.npmjs.com/package/@relayplane/proxy)
- [RelayPlane Proxy GitHub Repository](https://github.com/RelayPlane/proxy)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell, JSON, and TypeScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-only skill; output focuses on setup, commands, configuration, and operational guidance.]

## Skill Version(s):

4.1.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
