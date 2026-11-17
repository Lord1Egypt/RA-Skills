## Description:

长篇网文规划与写作。支持只讨论结构、只写大纲或指定细纲，明确要求正文后再写章节。触发方式：/story-long-write、/写长篇、「帮我开书」「定设定」「出卷纲」「规划剧情」「写大纲」「补细纲」「日更」「续写」「继续写」「修改第X章」「回炉」「重写第X章」。

This skill is ready for commercial/non-commercial use.

## Publisher:

[worldwonderer](https://clawhub.ai/user/worldwonderer)

### License/Terms of Use:

MIT

## Use Case:

供中文网文作者规划长篇故事、设定人物与关系、编排卷纲和章节细纲，并按明确要求创作或修改正文。作者可限定只讨论结构或只交付某一规划阶段，技能按请求范围推进。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags the ability to write to explicit output paths as a concern.

Mitigation: Check the destination path and intended file changes before accepting generated or revised story files.

Risk: The security review notes a possible loss of outline identifiers during file changes.

Mitigation: Review outline identifiers after edits and preserve a recoverable copy of the outline.

Risk: Security scan coverage was partial: 8 of 87 components were only partially inspected.

Mitigation: Review the partially inspected files before relying on the skill in your environment.

## Reference(s):

- [Writing workflow and scope controls](references/workflow-setup.md)
- [Volume planning workflow](references/workflow-volume.md)
- [Chapter writing workflow](references/workflow-chapter.md)
- [Writing craft](references/writing-craft.md)
- [Outline methods](references/outline-methods.md)
- [Project files and outputs](references/project-files.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Code, Shell commands]

**Output Format:** [Chinese-language story guidance, outlines, and manuscript or project files, usually in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Work is limited to the requested planning or writing scope; file changes may use explicit output paths.]

## Skill Version(s):

1.2.13 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
