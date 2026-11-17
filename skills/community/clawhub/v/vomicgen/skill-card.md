## Description:

将长篇小说转换为 Seedance 2.0 平台的 15 秒动态漫画分镜脚本，包含剧情容量分析、角色卡、6-8 个分镜头、微动作、镜头运动、配音和音效设计。

This skill is ready for commercial/non-commercial use.

## Publisher:

[fslong520](https://clawhub.ai/user/fslong520)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and agents use this skill to turn provided novel chapters or story excerpts into short VOMIC storyboard scripts optimized for Seedance 2.0. It guides the agent through story-capacity analysis, style and aspect-ratio confirmation, narration voice selection, and a checked final plaintext shot script.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may convert dangerous criminal or explosive scenes into clearer production scripts.

Mitigation: Review source material before use and require safeguards that keep criminal, explosive, or otherwise dangerous scenes non-actionable and lawful.

Risk: Use on arbitrary novels or user-submitted text can surface unsafe scene content during adaptation.

Mitigation: Apply host-side content review before storyboard generation and revise or refuse unsafe passages instead of making them more operational.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fslong520/skills/vomicgen)
- [Publisher profile](https://clawhub.ai/user/fslong520)
- [动态漫画定义.md](artifact/动态漫画定义.md)
- [技术规格.md](artifact/技术规格.md)
- [故事结构规范.md](artifact/故事结构规范.md)
- [创作规范.md](artifact/创作规范.md)
- [检查清单.md](artifact/检查清单.md)
- [章节.md](artifact/章节.md)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Plaintext storyboard script with staged conversational prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Final scripts are intended to be wrapped in plaintext and avoid markdown formatting symbols.]

## Skill Version(s):

1.2.0 (source: server release metadata, skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
