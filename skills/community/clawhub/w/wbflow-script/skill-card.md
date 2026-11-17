## Description:

流水线第2环——读取 01_story/story.json，产出分集剧本 02_script/episodes.json（场次/对白/旁白/时长估算），角色 id 必须原样引用。供 wbflow-storyboard 消费。（WBFlow 8 环流水线套件之一，须与 wbflow-pipeline 总控及本流水线其余环节 skill 配套安装才能运行。）

This skill is ready for commercial/non-commercial use.

## Publisher:

[junci003](https://clawhub.ai/user/junci003)

### License/Terms of Use:

MIT-0

## Use Case:

面向 WBFlow 流水线使用者，将项目故事整理为逐集剧本，为后续分镜环节提供文本骨架。需与 WBFlow 总控及其他配套环节共同安装。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads 01_story/story.json and writes 02_script/episodes.json, so running it in the wrong project could use or replace unintended files.

Mitigation: Run it from the intended project and review the generated episodes.json.

Risk: This is one stage of a multi-skill WBFlow pipeline and cannot run as a standalone workflow.

Mitigation: Install the WBFlow controller and companion stages, and review those skills separately.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/junci003/skills/wbflow-script)
- [Publisher profile](https://clawhub.ai/user/junci003)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [JSON (02_script/episodes.json)]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Structured episode and scene scripts with dialogue, narration, and estimated duration; character IDs are retained from the source story.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
