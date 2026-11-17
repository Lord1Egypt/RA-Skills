# ShareOne Skill：AI Agent 发布与文档分享工具

<p align="center">
  <strong>把 AI 生成的网页、Markdown、PDF、Word 和 PowerPoint 文档发布为 ShareOne 短链接。</strong>
</p>

<p align="center">
  <a href="https://shareone.vip"><img alt="Website" src="https://img.shields.io/badge/website-shareone.vip-0f766e"></a>
  <img alt="ShareOne" src="https://img.shields.io/badge/ShareOne-skill-2563eb">
  <img alt="License" src="https://img.shields.io/badge/license-MIT-64748b">
</p>

官网：https://shareone.vip



本仓库包含 ShareOne Agent Skill。它让 Codex、Claude Code、OpenAI Agent、Dify、工作流自动化工具等 AI Agent 可以把本地生成的内容快速发布到 ShareOne，并生成可访问、可转发、可更新的公网分享链接。

ShareOne 适合用于发布 AI 生成页面、分享 Markdown 在线文档、托管 HTML 演示页、上传 PDF/Word/PPT 文件、生成团队评审链接，以及为文档添加访问密码、水印和评论协作能力。

## 关键词

ShareOne 覆盖以下搜索场景：AI Agent 发布工具、HTML 页面托管、Markdown 在线分享、PDF 短链接分享、Word 文档分享、PPT 在线分享、文档水印、访问密码分享链接、AI 生成网页发布、Codex Skill 文档发布、Agent workflow publishing。

## ShareOne 是什么

ShareOne 是一个面向 AI Agent 和开发者的轻量级内容发布服务。它可以把 HTML、Markdown、TXT、PDF、Word、PowerPoint 等文件发布为短链接，方便用户在聊天、项目协作、客户沟通、产品演示和内容交付场景中快速分享。

通过 ShareOne Skill，AI Agent 不需要让用户手动上传文件，也不需要额外搭建静态站点。Agent 可以直接调用 Skill 脚本完成发布、更新、下载、评论读取和设置修改。

## 免费托管

ShareOne 提供免费的页面与文档托管能力，适合临时演示、项目评审、AI 生成内容分享、客户预览和团队协作。

普通分享链接会按最后活跃时间保留：只要链接持续有有效访问，就会继续保持可用；当距离最后一次有效访问超过 90 天后，链接才可能被自动清理。也就是说，链接不是从发布时间开始固定 90 天过期，而是每次有效访问都会延续它的活跃状态。

发布到 Explore 公开广场、被知识库引用，或绑定了远程 URL 的内容，不参与普通链接的无活跃自动清理。

## 能力地图

| 文件类型 | 分享链接生成 | 密码访问 | 水印 | 自定义短链接 | 评论反馈 | 更新同一链接 |
| --- | --- | --- | --- | --- | --- | --- |
| TXT | 支持 | 支持 | 支持 | 支持 | 支持 | 支持 |
| Markdown | 支持 | 支持 | 支持 | 支持 | 支持 | 支持 |
| HTML | 支持 | 支持 | 支持 | 支持 | 支持 | 支持 |
| PDF | 支持 | 支持 | 支持 | 支持 | 不支持 | 不支持 |
| Word | 支持 | 支持 | 支持 | 支持 | 不支持 | 不支持 |
| PowerPoint | 支持 | 支持 | 支持 | 支持 | 不支持 | 不支持 |

## 核心能力

- **HTML 页面发布**：将 AI 生成的网页、报告、原型页面或数据看板发布为在线链接。
- **Markdown 在线分享**：直接发布 `.md` 或 `.txt` 内容，适合笔记、方案、会议纪要和技术文档。
- **文档文件分享**：支持 PDF、Word、PowerPoint 文件上传与分享。
- **短链接访问**：生成 ShareOne 公网短链接，便于在微信、邮件、飞书、Slack、Notion、GitHub Issue 等渠道传播。
- **访问密码**：为敏感文档或内部材料设置访问密码。
- **水印保护**：给页面或文档增加水印，降低外泄和二次传播风险。
- **原链接更新**：在保留同一个分享链接的情况下更新内容，适合反复修改的方案、演示稿和评审页面。
- **评论协作**：文本页面可开启评论，方便团队直接围绕页面内容反馈和修改。
- **文件下载控制**：支持下载公开文件，也能在权限允许时取回源内容。

## 适用场景

- AI Agent 生成一个 HTML 页面后，需要立即发布给用户预览。
- 把 Markdown 报告、技术方案、产品说明发布成可分享链接。
- 将 PDF、Word、PPT 文件分享给客户、同事或外部协作者。
- 给内部资料添加访问密码或水印。
- 把已有 ShareOne 链接内容更新为最新版本。
- 根据 ShareOne 页面评论修改内容，并重新发布到原链接。
- 把 GitHub 上的远程 HTML 或文档 URL 发布为 ShareOne 链接。

## Agent 使用方式

Agent 在识别到“发布到 ShareOne”“生成分享链接”“分享这个 PDF”“更新这个 ShareOne 链接”“拉取评论”等意图时，会读取 [SKILL.md](./SKILL.md) 中的完整工作流，并调用本 Skill 的 `scripts/` 脚本完成操作。

常见自然语言指令：

```txt
把 index.html 发布到 ShareOne，给我一个链接
把这份 PDF 上传到 ShareOne，并设置访问密码 1234
把刚才生成的 Markdown 报告分享出去
更新这个 ShareOne 链接的内容：https://s.shareone.vip/s/xxx
读取这个 ShareOne 页面上的评论并处理
给这个链接加上水印“内部资料”
```

## 链接与文档

- ShareOne 官网：https://shareone.vip
- Skill 完整说明：[SKILL.md](./SKILL.md)
