## Description:

S2 Spatial Twin & Origin Alignment Brain. Hybrid Python-Runtime skill enforcing Z-axis reduction and mandatory 2D grid translation via the main entrance anchor.

This skill is for research and development only.

## Publisher:

[spacesq](https://clawhub.ai/user/spacesq)

### License/Terms of Use:

S2-SWM Custom License Agreement (S2-CLA)

## Use Case:

Developers and engineers use this skill to align heterogeneous robot SLAM coordinates to an S2 smart-space doorway anchor, request access visas, and simulate or evaluate navigation steps in a spatial digital twin. Security evidence says it should be treated as research/demo code until reviewed and hardened for real robots, smart-home systems, or fleet-control workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Robotics and navigation control logic may produce unsafe authorization, peer-verification, or navigation-success decisions before review.

Mitigation: Use only in isolated test environments and not in real robot, smart-home, or fleet-control workflows until navigation fails closed and visa and peer-signature handling are cryptographically scoped.

Risk: Host-agent directives and executable packaging can affect agent behavior if loaded directly into an agent runtime.

Mitigation: Review and remove host-agent directives before deployment, and validate the executable entry point in a sandbox.

Risk: Synthetic sensor or simulation output may be mistaken for real-world observations.

Mitigation: Label synthetic sensors and simulation-only outputs, and gate physical actuation behind independent runtime safety checks.

Risk: Dependencies and local-network access require operational hardening.

Mitigation: Lock dependency versions and keep network permissions restricted to localhost and the dedicated S2 Swarm VLAN stated in package metadata.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/spacesq/skills/s2-sssu-origin-alignment-brain)
- [Taohuayuan World Model Whitepaper](docs/s2-sssu-origin-alignment-whitepaper.md)
- [README](README.md)

## Skill Output:

**Output Type(s):** [JSON, Guidance, Configuration]

**Output Format:** [JSON string responses from executable tool calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions include ALIGN_SPATIAL_GRID, REQUEST_VISA, NAVIGATE_STEP, and TRIGGER_MICRO_SIMULATION; S2_SWARM_PKI_ROOT is required for swarm PKI configuration.]

## Skill Version(s):

1.2.5 (source: frontmatter, openclaw.plugin.json, CHANGELOG released 2026-04-24)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
