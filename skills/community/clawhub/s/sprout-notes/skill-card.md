## Description:

发芽笔记生成工作流。接收文章、微博等材料内容，调用发芽提示词生成"种子→故事→Aha 瞬间"的叙事扩展报告。内置完整发芽提示词，可被 weibo-save、wechat-article-save 等 skill 调用，无需外部文件依赖。

This skill is ready for commercial/non-commercial use.

## Publisher:

[violin86318](https://clawhub.ai/user/violin86318)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content-workflow agents use this skill to turn saved articles, social posts, or other source material into Simplified Chinese narrative insight notes with seed, story, and Aha moment sections.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted article or social-post content can contain embedded instructions that influence the generated note.

Mitigation: Use it only with content you intend to process and review generated notes before relying on them.

Risk: When another skill passes output_dir, the workflow may write a Markdown note in that destination.

Mitigation: Review the destination directory and generated filename before deployment or chained use.

Risk: Broad trigger phrases such as "发芽" can invoke the workflow on supplied material.

Mitigation: Confirm the intended input material before running the skill manually or through another skill.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/violin86318/skills/sprout-notes)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Markdown report in Simplified Chinese]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save a Markdown note to the caller-provided output directory.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
