## Description: <br>
ROS Noetic navigation support for Cartographer-based robots, using TF for pose lookup and rosbridge to send move_base waypoint goals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[threelevelchord](https://clawhub.ai/user/threelevelchord) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and robotics engineers use this skill to manage Cartographer-specific waypoints, read robot pose from TF, and send single-point or multi-waypoint navigation goals through rosbridge to move_base. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Navigation commands can publish movement goals to a ROS robot over rosbridge. <br>
Mitigation: Confirm rosbridge host, waypoint coordinates, TF frames, and robot surroundings before running navigation commands. <br>
Risk: Waypoint management can modify local waypoint JSON files. <br>
Mitigation: Review intended waypoint additions or removals and keep a backup of deployment-specific waypoint data. <br>
Risk: Security evidence reports a clean verdict but advises command review before workflows that can affect local files or authenticated services. <br>
Mitigation: Review commands before execution and run them only in the intended ROS and ClawHub environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/threelevelchord/ros-noetic-nav-cartographer) <br>
- [Skill documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands, Python script usage, and JSON waypoint files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces or updates waypoint JSON and emits console status for TF pose lookup and navigation commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
