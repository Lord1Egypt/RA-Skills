---
name: wenqu-publish
description: >-
  将中文草稿整理为可对外发布的版本：清理创作标记、生成候选标题、简介与封面图，并输出独立的发布目录，
  适用于文章、报告、教程、项目介绍和说明材料。当用户要求“发布这篇内容”“生成发布版”
  “准备发布”或“导出发布版”，或使用 "publish this article", "prepare a release version",
  "export a publication-ready draft" 等英文表达时使用。
slug: wenqu-publish
displayName: 文曲·发布
version: 0.1.19
summary: 把定稿清洗成发布版：删创作痕迹、生成标题、简介与封面、输出发布目录。
license: MIT
homepage: https://github.com/gogoingai/wenqu-skills
metadata:
  openclaw:
    homepage: https://github.com/gogoingai/wenqu-skills/tree/master/wenqu-publish
---

# 文章发布 Skill

> 📦 项目仓库与源码：<https://github.com/gogoingai/wenqu-skills>

## 用户输入工具

当本技能需要用户确认选择、补充必要信息或授权有副作用的操作时：

1. 优先使用当前运行时提供的原生用户输入工具，例如 `AskUserQuestion`、`request_user_input`、`clarify`、`ask_user` 或等价能力。
2. 若没有此类工具，使用带编号或字母选项的文本问答。
3. 同一决策阶段中彼此独立的问题可合并提问；后一个问题依赖前一回答时，按优先级逐个问。
4. 已由用户当前指令、调用方或文章偏好提供的信息，不重复询问。
5. 文中出现的具体工具名均为示例；应替换为当前运行时的等价能力。

## 工具等价说明（非 Claude Code 环境）

本文档里的 `Skill` 是 Claude Code 的工具名。在没有该工具的 agent 上运行本技能时：

- `Skill` 工具（调用 wenqu-image 生成封面）→ 没有跨技能调用机制就直接 Read `wenqu-image` 的 `SKILL.md` 和 `references/` 文件，照其内联执行

---

## 触发识别

| 用户信号 | 说明 |
|---------|------|
| "发布这篇文章"、"生成发布版"、"准备发布"、"导出发布版" | 进入「发布流程」 |

调用前提：文章通常已经通过 `wenqu-write` 走过完整写作流程（有对应的 `wenqu-skills/{文件名}/` 存储）。若没有该存储（用户直接拿一篇现成 Markdown 要求发布），走「降级模式」（见 `references/workflow.md`）。

---

## 发布流程

→ 查 `references/workflow.md`（完整步骤：定位存储 → 就绪检查 → 清洗正文 → 标题 → 简介 → 封面图 → 写入产物 → 记版本）

核心动作概览：
1. 读取本篇 `wenqu-skills/{文件名}/references/changelog.md` 确定当前草稿版本号
2. 检查全文是否还有未处理的配图占位、未生成的画图提示，用 `AskUserQuestion` 确认是否要先补齐
3. 清洗正文：去掉项目生成标识引用块、去掉所有 `# 画图提示` 代码块（只保留图片本身）
4. 用 `AskUserQuestion` 确认标题（→ `references/title-summary.md`）
5. 用 `AskUserQuestion` 确认约 100 字的简介（→ `references/title-summary.md`）
6. 用 `Skill` 工具调用 **wenqu-image** 生成封面图（→ `references/cover-prompt.md` 的专属规范，不同于文中说明性配图）
7. 产物写入 `{项目根目录}/wenqu-skills/{文件名}/publish/v{N}/`，不覆盖历史发布版本。**发布版正文保留原标题层级不变（原 H1 仍为 H1、原 H2 仍为 H2，不降级、不删改任何原标题）；选定的发布标题、简介、封面图只进 `meta.md`，不插入正文顶部、不替换原文 H1；发布版文件名沿用文章文件名（`{文件名}.md`）**
8. 在 `references/changelog.md` 追加一行发布记录

---

## 依赖

- **wenqu-write** 的存储结构（`wenqu-skills/{文件名}/`）——非必需但强烈推荐，缺失时降级为仅清洗当前文件
- **wenqu-image**（可选但推荐）：生成封面图；未安装时跳过封面，仅产出清洗后的正文、标题、简介，并告知用户手动配图

---

## 自动发布扩展点

当前版本只写本地文件，不做任何网络推送。`references/auto-publish.md` 是预留的扩展说明文档，记录了未来接入公众号、掘金、个人博客等平台自动发布时的接口约定与注意事项，目前是占位文档。
