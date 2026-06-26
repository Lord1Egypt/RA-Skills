## Description: <br>
Control a Reachy Mini robot (by Pollen Robotics / Hugging Face) via its REST API and SSH. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[afalk42](https://clawhub.ai/user/afalk42) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to control and monitor a Reachy Mini robot, including movement, recorded expressions, camera snapshots, audio direction sensing, app management, and status checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can move a physical robot and manage robot apps, services, and raw API endpoints. <br>
Mitigation: Install only on robots you own or administer, verify the target host, review commands before execution, and avoid raw or app-management commands unless intentional. <br>
Risk: The skill can capture camera snapshots and use microphone-derived direction sensing. <br>
Mitigation: Use patrol and audio-sensing behavior only where people have consented and where local privacy expectations allow it. <br>
Risk: The skill supports SSH-based snapshot handling and artifact evidence references default robot credentials. <br>
Mitigation: Change default SSH credentials, prefer SSH keys, and avoid storing passwords in environment variables where other users or processes can read them. <br>


## Reference(s): <br>
- [Reachy Mini REST API Reference](references/api-reference.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/afalk42/reachy-mini) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and REST API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local image file paths for camera snapshots.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
