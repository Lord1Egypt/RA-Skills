## Description: <br>
S2 Spatial Element Layer & 4D Semantic Tensor Map integrates L0-L4 layer architecture, 20 material physics tensors, and Chronos backward-persistence time-slicing via S2-GeoJSON. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spacesq](https://clawhub.ai/user/spacesq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and robotics engineers can use this skill to interpret S2-GeoJSON spatial layers, material tensor data, and time-sliced hazard annotations for local embodied-navigation analysis. It is best treated as an experimental spatial-mapping aid unless additional validation is added for real robot control. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives safety-sensitive robot-navigation guidance while evidence.security says its time-validation safeguards are overstated. <br>
Mitigation: Treat outputs as advisory only and add timestamp validation before using Chronos or hazard directives for real robot control. <br>
Risk: Robot behavior based on spatial layers and material tensors may be unsafe if inputs are malformed, stale, or outside the expected local environment. <br>
Mitigation: Use input allowlisting, controlled-environment testing, and human review before connecting the guidance to physical navigation systems. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/spacesq/s2-sel-4d-semantic-tensor-map) <br>
- [S2-SEL 4D Chronos whitepaper](docs/s2-sel-4d-chronos-whitepaper.md) <br>
- [S2 material tensor library](data/s2_material_tensor_library.json) <br>
- [Sample S2-GeoJSON room layers](examples/sample_room_layers.json) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, configuration, markdown] <br>
**Output Format:** [Markdown guidance with Python and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce robot-navigation intervention guidance derived from local S2-GeoJSON and material tensor inputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package.json, changelog released 2026-04-07) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
