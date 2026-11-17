## Description:

Instructs the Embodied AI on how to process incoming multimodal sensor data (LiDAR, Camera, Tactile), avoid visual illusions, and output 1s-60s physical causal predictions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spacesq](https://clawhub.ai/user/spacesq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and embodied AI operators use this skill to fuse LiDAR, camera, and tactile inputs, resolve sensor conflicts, and produce 1-60 second physical-world causal predictions. Use it as decision support rather than as the sole authority for robot motion or other safety-critical actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Safety-relevant physical-world predictions may be based on weakly validated sensor data.

Mitigation: Add strict sensor schemas, finite and range checks, stale-data handling, and fail-closed Unknown or Unsafe results before critical use.

Risk: Predictions could be over-trusted for robot movement or other physical actions.

Mitigation: Require independent collision protection and human or system-level authorization for movement decisions.

Risk: Captured environmental sensor data may include sensitive information.

Mitigation: Apply privacy controls for collection, retention, access, and sharing of environmental data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/spacesq/skills/s2-multimodal-fusion-predictor)
- [Taohuayuan World Model Whitepaper V3.1](artifact/s2-swm-v3.1-multimodal-fusion.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [JSON response with structured causal prediction text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns an aligned sensor state and a 1s-60s causal prediction timeline.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, OpenClaw plugin metadata, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
