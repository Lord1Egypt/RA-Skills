## Description: <br>
Connects to a ROS Noetic navigation stack through rosbridge to read maps, manage waypoints, query AMCL pose, and send single- or multi-waypoint navigation goals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[threelevelchord](https://clawhub.ai/user/threelevelchord) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and robotics operators use this skill to operate ROS Noetic AMCL-based navigation workflows from an agent, including map inspection, waypoint storage, current-pose lookup, and route execution through rosbridge. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send navigation goals that move real robot hardware without a confirmation step. <br>
Mitigation: Use only in a supervised, cleared area with emergency stop access, and verify localization, map frame, and waypoint coordinates before execution. <br>
Risk: Exposed rosbridge access could allow unintended control of the robot. <br>
Mitigation: Keep rosbridge limited to trusted local access and avoid exposing it on untrusted networks. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/threelevelchord/ros-noetic-nav) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces command-line workflows for ROS navigation and waypoint management; some commands can send movement goals to live robot hardware.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
