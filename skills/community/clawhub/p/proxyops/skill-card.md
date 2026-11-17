## Description:

ProxyOps is a local-first proxy inventory, routing planner, and health tracking engine for organizing proxy assets, comparing metadata, tracking expiry and quality, assigning sessions, and choosing a fit-for-purpose proxy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[projectsnowwork](https://clawhub.ai/user/projectsnowwork)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to maintain a local proxy inventory, compare proxy metadata, update health signals, and choose a fit-for-purpose proxy for a task.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Proxy records can contain sensitive infrastructure metadata such as hosts, providers, regions, auth type labels, and operational notes.

Mitigation: Keep secrets out of labels and notes, store only necessary metadata, and restrict access to the local storage directory on shared machines.

Risk: Proxy recommendations depend on user-maintained status, expiry, success-rate, latency, and quality metadata.

Mitigation: Update health and expiry fields before relying on recommendations for routing decisions.

## Reference(s):

- [Proxy Philosophy](references/philosophy.md)
- [ProxyOps ClawHub Skill Page](https://clawhub.ai/projectsnowwork/skills/proxyops)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Text guidance and shell command invocations that read and write local JSON inventory files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores proxy metadata locally under ~/.openclaw/workspace/memory/proxy; no external sync or proxy provider API is required.]

## Skill Version(s):

1.0.0 (source: release evidence and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
