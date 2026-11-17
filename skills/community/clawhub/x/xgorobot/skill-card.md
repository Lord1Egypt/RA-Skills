## Description:

Xgorobot helps agents control XGO Mini, Lite, Mini3W, and Rider robots using bundled scripts and Python APIs for motion, preset actions, vision, AI features, sensors, display, and audio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mingyangbj](https://clawhub.ai/user/mingyangbj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and robot operators use this skill to run prepared XGO robot-control scripts or create custom Python control flows for movement, perception, speech, display, and sensor tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe shell execution and privileged hardware helper calls may run unintended commands or alter device state.

Mitigation: Review and remediate shell=True, os.system, and sudo-backed helper calls before installation; constrain command inputs and execute only trusted scripts.

Risk: Untrusted URLs, filenames, and target text can influence downloads, media playback, generated commands, or AI-driven robot actions.

Mitigation: Accept only trusted inputs, validate URLs and file paths, and add allowlists or sanitization before using the skill on hardware.

Risk: Camera and audio data may be sent to DashScope for AI features.

Mitigation: Use the AI features only with informed consent, avoid sensitive scenes or conversations, and manage DASHSCOPE_API_KEY as a secret.

Risk: Robot movement, servos, wheels, and arm controls can create physical safety risks in real environments.

Mitigation: Operate under supervision in a clear area, test low-risk commands first, and keep a stop or power-off path available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mingyangbj/skills/xgorobot)

## Skill Output:

**Output Type(s):** [shell commands, code, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and Python code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke robot hardware, camera, audio, display, serial, and DashScope-backed AI features.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
