## Description:

视频分镜演示动画生成技能：每个镜头产出一个独立 HTML（统一播放器底盘+每页不同视觉风格），覆盖风格分配、双角色立绘素材、口播时间轴对齐、批量截图质检与 index 总览的完整工具链。适用于制作技术实测、产品发布、课程、叙事类分镜演示视频。

This skill is ready for commercial/non-commercial use.

## Publisher:

[unclecheng-li](https://clawhub.ai/user/unclecheng-li)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use this skill to turn video outlines, narration scripts, and shot lists into independent HTML demonstration shots with coordinated visual styles, character reactions, timing cues, screenshots, and an index overview.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Helper scripts may execute commands or write generated content outside the intended output area when given hostile project plans, output filenames, or browser paths.

Mitigation: Use only trusted shot-list and plan JSON files, avoid attacker-controlled filenames and browser paths, and run the workflow in an isolated project directory.

Risk: Generated HTML may carry unsafe content if untrusted plan data is inserted into page titles, paths, or markup.

Mitigation: Review generated HTML before use, keep generated outputs inside the intended workspace, and add path containment plus HTML escaping before production use.

Risk: The authoritative scanner verdict is suspicious despite no enumerated risk findings.

Mitigation: Review the helper scripts and security guidance before installing or using the skill on untrusted projects.

## Reference(s):

- [README](README.md)
- [Mechanics Reference](references/mechanics.md)
- [Style Cards](references/style-cards.md)
- [Character Reactions](references/character-reactions.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated HTML/CSS/JavaScript file instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce per-shot HTML pages, project plan JSON, screenshot artifacts, and an index overview through bundled Node.js helper scripts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
