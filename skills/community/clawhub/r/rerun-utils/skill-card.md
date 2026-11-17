## Description:

Static 3D visualization utilities wrapping Rerun SDK for adding point clouds, trajectories, cameras, planes, and chessboards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangyendt](https://clawhub.ai/user/wangyendt)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to add Rerun SDK visualizations for point clouds, trajectories, cameras, planes, and chessboards when debugging SLAM, robot poses, calibration targets, and 3D scenes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on the external Rerun SDK resolved by gettool.

Mitigation: Install the Rerun SDK from a trusted source and prefer a pinned, reviewed version.

Risk: Visualization calls may consume image or data paths supplied by the user.

Mitigation: Only pass paths and datasets that are intended for visualization.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wangyendt/skills/rerun-utils)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration]

**Output Format:** [Markdown with Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the Rerun SDK and numeric inputs in the documented shapes and data types.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
