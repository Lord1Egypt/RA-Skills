## Description:

把一张栅格参考图（图标表、牌面表、UI 截图、设计稿切图）复刻成 SVG / Canvas 手绘图形时，用像素级测量代替目测：自动切分网格、按色系采样真色、连通域量出每个元素的位置尺寸并换算成 viewBox 坐标，最后生成「参考图 vs 本项目」并排对照页验证，再用结构计数断言（n 个点 = n 个圆）把结果钉死。当用户说「按这张图的图案改」「照着这个图做图标」「复刻这套牌面 / 表情 / 图标」「颜色不对，按参考图调」，或给出的参考图是低分辨率截图（有压缩噪点）时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[oracis](https://clawhub.ai/user/oracis)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and designers use this skill to convert raster reference images such as icon sheets, card faces, UI screenshots, and design slices into SVG or Canvas drawing specifications. It emphasizes measured grid detection, color sampling, connected-component measurement, side-by-side visual comparison, and structure-count assertions instead of visual guessing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can read and analyze user-provided images and may create local verification scripts or comparison pages.

Mitigation: Use only intended reference images, review generated scripts and pages before running them, and keep generated artifacts within the project workspace.

Risk: Measurement or color-sampling mistakes can produce SVG or Canvas output that looks close but does not match the reference.

Mitigation: Use the skill's side-by-side comparison page and structure-count assertions to verify layout, color, and element counts before accepting output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/oracis/skills/ref-image-to-svg-spec)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with code snippets and verification guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose project-local measurement scripts, comparison pages, and structural assertions when useful.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
