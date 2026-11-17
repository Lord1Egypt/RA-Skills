## Description:

用户可以让 OpenClaw 控制元萝卜下棋机器人进行围棋取落子、机械臂移动、表情控制、语音播报、棋盘管理时使用此技能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[senserobotclawbot](https://clawhub.ai/user/senserobotclawbot)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users use this skill to control a local SenseRobot chess robot for Go stone pickup and placement, robotic arm movement, board cleanup, expression display, Chinese speech playback, photo capture, audio recording, and image display.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can move a physical robotic arm and clear the board through local HTTP commands.

Mitigation: Use only with physical supervision and require explicit user confirmation before arm movement, stone placement, or board cleanup.

Risk: The skill can take photos, record audio, speak, and upload or display local PNG images.

Mitigation: Require explicit consent before camera, microphone, speech, recording stop, or file-upload actions, and limit file paths to intended images.

Risk: The robot API is described as unauthenticated local HTTP.

Mitigation: Operate the robot only on a trusted, isolated network and avoid exposing the API beyond the local robot-control environment.

## Reference(s):

- [元萝卜下棋机器人 API 参考文档](references/API_REFERENCE.md)
- [元萝卜下棋机器人 速查表](references/CHEATSHEET.md)
- [ClawHub skill page](https://clawhub.ai/senserobotclawbot/skills/senserobot)
- [Publisher profile](https://clawhub.ai/user/senserobotclawbot)
- [SenseRobot homepage](https://www.SenseRobotChess.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with curl commands, Python CLI examples, and JSON response descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May instruct an agent to call unauthenticated local HTTP endpoints that move a physical robotic arm, use cameras and microphones, play speech, and upload local PNG images.]

## Skill Version(s):

1.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
