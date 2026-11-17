## Description:

将已准备的演示文稿大纲制作成逐页 HTML 演示文稿，并可按需导出 PPTX。

This skill is ready for commercial/non-commercial use.

## Publisher:

[sensenova-skills](https://clawhub.ai/user/sensenova-skills)

### License/Terms of Use:

MIT-0

## Use Case:

演示文稿制作者在 Entry/Story 已提供任务资料和大纲后，用此 Agent 生成逐页 HTML、PNG 预览、讲稿和演示播放器；需要 PPTX 时可一并导出。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: 当前版本可能终止无关浏览器进程、从共享临时目录执行被替换的代码，或删除已有演示文稿素材。

Mitigation: 优先使用修正后的版本。在此之前，限于一次性、非特权容器中运行，隔离进程可见性、限制网络和执行时间，并仅提供所需凭据；先备份演示文稿与字体，避免在图片查询中暴露机密，并独立核验请求的 PPTX。

Risk: 静态审查未对供应代码进行全面审计。

Mitigation: 在部署前进行安全审查，并遵循隔离运行、备份和最小凭据建议。

## Reference(s):

- [Planning contract](artifact/references/planning-contract.md)
- [Design rules](artifact/references/design-rules.md)
- [Layout patterns](artifact/references/layout-patterns.md)
- [Editing contract](artifact/references/editing-contract.md)
- [Quality checklist](artifact/references/quality-checklist.md)

## Skill Output:

**Output Type(s):** [Files, HTML, PNG, Markdown, PPTX]

**Output Format:** [逐页 HTML（1600×900）、PNG 预览、Markdown 讲稿、present.html，以及按需生成的 PPTX]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [基于已准备的大纲制作；PPTX 是否交付取决于任务设置。]

## Skill Version(s):

2026.10.29 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
