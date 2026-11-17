# 科研工作区组织技能包（research-ops）

> 🔍 **不知道这是干什么的？** 装好后直接问 AI「这个是做什么的」，AI 会给你介绍，不用读文档。

把「一个课题组 / 一个研究项目」的**四层真源**组织好的 AI 技能包：本地文件 · Zotero · Obsidian · 飞书。核心是**每类内容只有一个真源**，其余都是它的投影。

## 它解决什么

| 痛点 | 本技能的答案 |
|---|---|
| 同一份内容在四处复制，改一处不同步 | **四层真源**：每类内容指定唯一权威，其余只做投影/链接 |
| 项目散落、找不到"某个项目在哪" | **项目 ID + 组级 `INDEX.md`**（模型自定位入口）|
| 目录随人习惯乱长 | **项目目录模板**：`README / STATE / scripts / data / results / output`（+ `chats/` 会话存档）|
| 多台机器之间对不上 | **跨机同步纪律**（Syncthing / Obsidian LiveSync / Zotero），同步操作「双端确认」|
| 与 AI 的对话没留档 | `chats/` 对话存档（可脱敏导出）|
| 文献 / 笔记 / 交付物各归各的库 | 项目 ↔ **Zotero collection** ↔ **Obsidian 笔记夹** ↔ **飞书云盘目录** 一一映射 |

## 它是什么

一套**通用、零项目专有路径**的方法论 + 参数化脚本；**具体组/项目**由各自的 `AGENTS.md` 特化（把组名、路径、映射填进通用规则）。

配套技能：[`project-organization`](https://github.com/TOMUIV/project-organization-skill)（大项目分层 + buffer + .trash）。

## 安装

- **ClawHub**：`clawhub install research-ops`
- **手动**：把本目录放进 OpenCode / OpenClaw 的 `skills/` 下。

## 脚本

| 脚本 | 作用 |
|---|---|
| `new_subproject.py` | 按科研项目模板建子项目（含 STATE 当前基线）|
| `doctor.py` | 工作区自检（结构 / 索引 / 同步状态）|

## 缓存与凭据

`creds/` 内是**通用加密保险箱模板**（不含任何真实密钥）；真凭据永远在**密文** `runtime/credentials.enc`，且 `runtime/` 已 `.gitignore`。

## 开源与发布

本技能包**完全开源**；**最新版以下面两处为准**：

| 渠道 | 地址 | 查看 / 获取 |
|---|---|---|
| **GitHub**（源码） | **https://github.com/TOMUIV/research-ops-skill** | 看完整代码、Fork、提 Issue |
| **ClawHub**（技能市场） | slug **`research-ops`** | `clawhub install research-ops` |

> 想确认「最新版是多少 / 改了什么」——去上面任一渠道看即可；本仓库与 ClawHub 同源同版本。

## 许可

MIT-0（No Attribution，见 `LICENSE`）。
