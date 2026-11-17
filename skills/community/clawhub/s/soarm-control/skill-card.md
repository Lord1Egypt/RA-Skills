## Description:

Control the robotic arm through the OpenClaw SOARM API for reading current joint state, moving by joint angles, moving by XYZ coordinates, and handling SOARM robot-control requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuyoujiang](https://clawhub.ai/user/yuyoujiang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to read SOARM robot state, send supervised joint or XYZ movement commands, and trigger local pick tasks through the OpenClaw SOARM API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill controls a physical robot and can issue safety-critical movement and pick actions.

Mitigation: Use only with a supervised SOARM setup, a clear workspace, a physical emergency stop, and explicit operator approval before movement or pick commands.

Risk: The local service exposes motion, detection, and pick endpoints without visible authentication or safety gating.

Mitigation: Keep the service bound to loopback or place it behind access controls; do not expose it to untrusted networks.

Risk: Camera-based detection and autonomous picking can choose or track the wrong object.

Mitigation: Treat detection-driven pick tasks as supervised actions and verify the target and workspace before starting `/pick`.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuyoujiang/skills/soarm-control)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce commands that call local robot-control endpoints and should be reviewed before execution.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
