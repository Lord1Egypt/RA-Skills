## Description:

Empowers Embodied AI with the Ego-Centric 9-Grid perception model. Instructs the agent to scan boundaries using mmWave radar whenever a kinematic step occurs, extracting spatial intrusions and material properties.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spacesq](https://clawhub.ai/user/spacesq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and embodied-AI operators use this skill to make an agent perform ego-centric 9-grid boundary scans after movement and summarize intrusion, material, and collision-context signals for downstream reasoning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Simulated radar readings may be mistaken for live sensor results in robotics, mobility, or safety workflows.

Mitigation: Use only with validated sensor input for live operation, clearly label simulation mode, and fail closed when hardware data is unavailable.

Risk: Boundary and collision-context output could influence physical movement decisions.

Mitigation: Keep independent collision-avoidance controls, human oversight, and controlled-environment testing in place before any physical deployment.

## Reference(s):

- [S2-SWM V3 Ego-Centric Prediction Whitepaper](artifact/s2-swm-v3-ego-centric-prediction.md)
- [ClawHub skill page](https://clawhub.ai/spacesq/skills/s2-boundary-scanner)
- [ClawHub publisher profile](https://clawhub.ai/user/spacesq)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [JSON scan results plus concise causal status text for agent reasoning]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports eight peripheral grid states, intrusion percentages, distance-to-boundary values, material inferences, and collision warnings; current security evidence says scan data is simulated.]

## Skill Version(s):

1.0.0 (source: server release evidence, SKILL.md frontmatter, package.json, and openclaw.plugin.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
