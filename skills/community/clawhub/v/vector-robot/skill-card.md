## Description:

Control Anki Vector robot via wire-pod. Speak through Vector, see through its camera, move head/lift/wheels, change eye colors, trigger animations. Use when user mentions Vector robot, wants to speak through a robot, control a physical robot, or interact with wire-pod.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bogorman](https://clawhub.ai/user/bogorman)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to control an Anki Vector robot running wire-pod, including speech, camera snapshots, movement, settings, and built-in actions. It also provides optional OpenClaw integration guidance for receiving voice commands through a local proxy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control a physical robot and camera.

Mitigation: Use it only when robot and camera control are intended, supervise movement, and keep the robot on a safe surface.

Risk: The optional proxy and LaunchAgent can introduce unauthenticated local service exposure and login persistence.

Mitigation: Restrict the proxy to loopback, add authentication before broader exposure, and enable auto-start only with a documented uninstall path.

Risk: Speech text and snapshot paths are treated as unsafe inputs by the security evidence.

Mitigation: Validate and quote inputs before unattended use, and write camera snapshots only to expected local paths.

## Reference(s):

- [wire-pod SDK API Reference](references/api.md)
- [wire-pod project](https://github.com/kercre123/wire-pod)
- [Vector-Robot ClawHub release page](https://clawhub.ai/bogorman/skills/vector-robot)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown guidance with bash, JSON, and HTTP API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce commands that operate a physical robot, access its camera stream, or configure a local proxy.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
