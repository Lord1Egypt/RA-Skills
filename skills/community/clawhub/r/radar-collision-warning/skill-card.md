## Description: <br>
Calls a Raspberry Pi ROS2 radar warning service through rosbridge WebSocket to retrieve the nearest obstacle distance and return collision-warning status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[33-code](https://clawhub.ai/user/33-code) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators of a controlled Raspberry Pi ROS2 lidar setup use this skill to query or continuously monitor a radar collision-warning service and receive machine-readable distance and warning results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill connects to rosbridge over the network and depends on a Raspberry Pi ROS2 environment. <br>
Mitigation: Use it only with a controlled Raspberry Pi and ROS2 setup, and keep rosbridge off untrusted networks. <br>
Risk: The bundled startup script restarts ROS, lidar, and radar-warning processes. <br>
Mitigation: Review the startup script before execution and run it only in the intended ROS workspace. <br>
Risk: Continuous monitor mode can keep polling in the background. <br>
Mitigation: Run monitor mode deliberately and stop the background process when monitoring is finished. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/33-code/radar-collision-warning) <br>
- [ROS2 radar warning node](artifact/references/radar_collision_warning_node.py) <br>
- [ROS bridge startup script](artifact/references/start_radar_rosbridge.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, code] <br>
**Output Format:** [Markdown guidance with shell commands and JSON stdout from the Node.js helper] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 18+ and a reachable rosbridge WebSocket configured through RADAR_HOST/RADAR_PORT or local workspace configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
