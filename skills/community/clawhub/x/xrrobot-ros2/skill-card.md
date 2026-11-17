## Description:

Controls, checks, and troubleshoots an XRRobot running ROS 2 Jazzy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ceoifung](https://clawhub.ai/user/ceoifung)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, robotics engineers, and supervised XRRobot operators use this skill to inspect ROS 2 system state, run bounded robot-control commands, manage navigation waypoints, and coordinate camera, LiDAR, navigation, YOLO, voice, and grasp workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Robot-control paths can move or disrupt a real robot without enough local safety checks.

Mitigation: Install only on a supervised XRRobot host where operators can see the robot, clear the area, stop it manually, and enforce explicit speed, duration, and stop commands on every motion path.

Risk: Conflicting ROS controllers or /cmd_vel publishers can cause unsafe or unexpected movement.

Mitigation: Check ROS mode, node readiness, localization state, and /cmd_vel publisher conflicts before movement; avoid manual motion while navigation, autopilot, lane keeping, or follower control is active.

Risk: Vision, YOLO, and grasp workflows can act on bad detections or expose sensitive camera data.

Mitigation: Validate model availability and target classes, prefer observe or dry-run checks before real grasping, keep web services on trusted local networks, and confirm image-data handling requirements before collection or training.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ceoifung/skills/xrrobot-ros2)
- [Operations](references/operations.md)
- [Orchestration](references/orchestration.md)
- [Base Drive](references/base.md)
- [Navigation](references/navigation.md)
- [Mapping](references/mapping.md)
- [Camera](references/camera.md)
- [LiDAR](references/lidar.md)
- [Grasp](references/grasp.md)
- [Task Orchestrator](references/task_orchestrator.md)
- [YOLO](references/yolo.md)
- [Vision](references/vision.md)
- [Autopilot](references/autopilot.md)
- [Lane Keeping](references/lanekeeping.md)
- [Follower](references/follower.md)
- [Guard](references/guard.md)
- [Voice](references/voice.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, ROS 2 command output interpretation, and concise operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce bounded ROS 2 command sequences and waypoint configuration updates when explicitly authorized.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
