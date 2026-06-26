## Description: <br>
S2 Spatial Twin & Origin Alignment Brain. Hybrid Python-Runtime skill enforcing Z-axis reduction and mandatory 2D grid translation via the main entrance anchor. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spacesq](https://clawhub.ai/user/spacesq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and robotics or smart-space teams use this skill to align a local SLAM coordinate frame to an S2 main-entrance anchor and obtain JSON responses for grid alignment, access visa requests, navigation steps, and sandboxed spatial simulation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill combines origin alignment with robotics control-plane behavior. <br>
Mitigation: Review behavior before use and keep evaluation isolated from real robots and home devices until operator approval gates are added. <br>
Risk: The skill can handle sensor, geolocation, and spatial-state data. <br>
Mitigation: Define scoped network access plus privacy and retention rules before deployment. <br>
Risk: Safety paths may affect navigation halt or control decisions. <br>
Mitigation: Add tests that confirm the intended safety paths run before connecting the skill to physical devices. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/spacesq/s2-sssu-origin-alignment-brain) <br>
- [Publisher profile](https://clawhub.ai/user/spacesq) <br>
- [S2-SWM Indoor Spatial Frame Alignment & Origin Anchoring Specification](docs/s2-sssu-origin-alignment-whitepaper.md) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, text, configuration, guidance] <br>
**Output Format:** [JSON strings returned by local Python tool actions, with human-readable status and instruction fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include a 2D transform matrix, WGS84 anchor data, visa status, generated spatial state, or navigation halt status.] <br>

## Skill Version(s): <br>
1.2.5 (source: server release metadata, SKILL.md frontmatter, openclaw.plugin.json, CHANGELOG top entry released 2026-04-24) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
