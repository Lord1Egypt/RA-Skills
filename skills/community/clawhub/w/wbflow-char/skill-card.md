## Description:

流水线第5环——读取 01_story/story.json 的角色设定，为每个角色生成"定妆参考图"（正面全身、中性背景、锁定配色与 identity_lock 强符号），并回写 ref_image 路径到 story.json。这是解决跨镜头角色一致性的关键一环。（WBFlow 8 环流水线套件之一，须与 wbflow-pipeline 总控及本流水线其余环节 skill 配套安装才能运行。）

This skill is ready for commercial/non-commercial use.

## Publisher:

[junci003](https://clawhub.ai/user/junci003)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this workflow stage to generate consistent, full-body character reference images from the story's character definitions and record each image path in story.json. It requires the WBFlow controller and companion stages to operate as part of the full pipeline.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Character descriptions may be sent to the selected image-generation service.

Mitigation: Confirm the service and its data-handling terms before sending character descriptions.

Risk: The workflow writes character image paths into story.json.

Mitigation: Review the story.json changes and generated character references before continuing the pipeline.

## Reference(s):

- [WBFlow Char Skill on ClawHub](https://clawhub.ai/junci003/skills/wbflow-char)

## Skill Output:

**Output Type(s):** [Images, Markdown, JSON]

**Output Format:** [PNG character reference images, a Markdown character-to-image mapping table, and updated JSON story data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One front-facing full-body reference image per character; the story data records each image path.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
