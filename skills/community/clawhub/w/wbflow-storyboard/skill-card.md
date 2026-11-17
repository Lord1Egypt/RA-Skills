## Description:

流水线第3环——读取 02_script/episodes.json 与 01_story/story.json，产出标准化分镜表 03_storyboard/storyboard.json（镜头号/景别/运镜/画面/时长/角色id）。供 wbflow-prompt 消费。（WBFlow 8 环流水线套件之一，须与 wbflow-pipeline 总控及本流水线其余环节 skill 配套安装才能运行。）

This skill is ready for commercial/non-commercial use.

## Publisher:

[junci003](https://clawhub.ai/user/junci003)

### License/Terms of Use:

MIT-0

## Use Case:

WBFlow users use this storyboard stage to turn story and episode-script files into a structured shot list, including shot size, camera movement, duration, characters, action, continuity, and audio notes. It is designed to be installed with the WBFlow pipeline controller and companion stages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Storyboard continuity, character IDs, or total duration may not match the source script or companion-stage assets.

Mitigation: Review character IDs and continuity against the stage-5 character designs, verify total duration against the episode estimate, and review companion skills separately.

## Reference(s):

- [WBFlow·第3环 分镜表 on ClawHub](https://clawhub.ai/junci003/skills/wbflow-storyboard)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [JSON storyboard file (storyboard.json)]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Structured shots with shot IDs, episode and scene IDs, shot size, camera movement, duration, subject, character IDs, in-frame action, continuity, and audio notes.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
