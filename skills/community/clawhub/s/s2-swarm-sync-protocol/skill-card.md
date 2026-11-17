## Description:

Instructs the OpenClaw Agent to authenticate peer agents before right-of-way yielding or sensor federation in multi-agent swarm coordination.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spacesq](https://clawhub.ai/user/spacesq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to guide multi-agent coordination where peer broadcasts may affect sensor sharing, trajectory decisions, and right-of-way arbitration. It is intended for normal ClawHub release use, but safety-critical robotic or vehicle deployments require independent engineering review and stronger authentication controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A forged peer broadcast could be accepted if authentication remains token-based or otherwise weak.

Mitigation: Replace the hard-coded signature check with real cryptographic verification rooted in S2_SWARM_PKI_ROOT before any deployment.

Risk: Outputs may influence braking, trajectory, or sensor federation decisions in physical systems.

Mitigation: Require local safety vetoes, operator visibility, authorization checks, replay protection, and privacy limits before using the skill with robots, vehicles, drones, or other safety-relevant systems.

## Reference(s):

- [S2-SWM Special Protocol Whitepaper](artifact/S2_SWM_Special_Protocol_Whitepaper.md)
- [ClawHub Skill Page](https://clawhub.ai/spacesq/skills/s2-swarm-sync-protocol)

## Skill Output:

**Output Type(s):** [json, guidance, configuration]

**Output Format:** [JSON responses with status, authentication result, federated sensor data, right-of-way decision, and action guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires S2_SWARM_PKI_ROOT configuration and an execute_swarm_sync tool entry point.]

## Skill Version(s):

1.1.0 (source: server release evidence, SKILL.md frontmatter, package.json, openclaw.plugin.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
