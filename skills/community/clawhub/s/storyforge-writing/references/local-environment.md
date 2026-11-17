# 本地环境适配（可选）— 电影大师 agent 环境

> **定位**：本技能的契约与校验器**与环境无关**；本文件只记录**特定 agent 环境**（作者的「电影大师」agent）
> 的本地约定。其它环境使用本技能时**可以忽略本文件**，或仿照本文件写自己的适配。
> 本文件内容的证据等级 = **`INFERRED`（环境内置约定）**，**不属于** StoryForge 数据契约基线。

## 1. 上游来源的本地镜像

| 用途 | 本地路径 |
| --- | --- |
| 主基线（唯一数据契约基线） | `H:\storyforge-main`（= `github.com/yuanbw2025/storyforge` 的本地 checkout） |
| 辅助来源（仅 agent 纪律 / 证据分级） | `H:\StoryForge-master\docs\ai\anti-hallucination.md` |
| 技能原件（WSL） | `\\wsl.localhost\OpenClawGateway\home\openclaw\.openclaw\agents\main\workspace\skills\storyforge-writing` |

基线审计记录：`REV-20261005-015`（逐文档版本表的来源）。

## 2. 项目目录约定

- 项目资产位于 `projects/<项目>/`（设定 md）与 `knowledge/`（考据库）。
- **白名单项目**（如长铗传）可直接开工；非白名单项目先向用户汇报再动手。
- 长篇试点：`projects/长铗传/storyforge-framework.json`（首个闭环验证）；字段 → 来源 md 的映射示例见 `contracts/A-longform.md` §2。

## 3. 环境来源的外部工具约定

- 「达芬奇」相关条目来自 **agent 环境（`ai-memory`）**，**非源仓库基线**（在上游仓库全文检索 0 命中，见 `REV-20261005-015` #5）。
- 凡涉及达芬奇（环境来源）的操作：**必须先在 `ai-memory` 检索到对应条目**（如「达芬奇 MCP 15 条铁律」「agent-change-safety」）再执行；
  检索不到就停下问用户，不得以契约行文当操作依据。详见 `contracts/C-post.md` §7。

## 4. 工作副本与发布

工作副本、回写与发布流程（含三层树清单工具、发布清单）见 `COMPAT.md`。
