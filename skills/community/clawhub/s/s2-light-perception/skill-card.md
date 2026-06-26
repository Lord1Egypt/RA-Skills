## Description: <br>
S2-SP-OS Light Radar uses real LAN UDP discovery and local Hue/Wiz API calls to read smart-light state and build a 4sqm voxel light memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SpaceSQ](https://clawhub.ai/user/SpaceSQ) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and smart-home users use this skill to discover trusted local Hue or Wiz lights, read authorized device state, and summarize lighting conditions for spatial-memory and circadian-lighting suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill actively scans the local network for smart lights. <br>
Mitigation: Run discovery only on trusted networks where scanning is authorized, and confirm before starting discovery. <br>
Risk: Read operations contact a specified local smart-light device. <br>
Mitigation: Provide target device IPs intentionally, use the consent flag for reads, and avoid shared or unauthorized networks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/SpaceSQ/s2-light-perception) <br>
- [S2-SP-OS homepage](https://space2.world/s2-sp-os) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown instructions with bash commands and JSON script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and access to a trusted local network with target smart-light devices.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
