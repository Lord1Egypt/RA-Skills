# 📋 Feishu Doc Manager — 飞书文档管理系统

<div align="center">

**Wiki + Drive + Bitable 三层架构 · 自动归档 · 智能分类 · 全局检索**

[![ClawHub](https://img.shields.io/badge/ClawHub-feishu--doc--manager-blue)](https://clawhub.ai)
[![GitHub](https://img.shields.io/badge/GitHub-uuoov%2Ffeishu--doc--manager-black?logo=github)](https://github.com/uuoov/feishu-doc-manager)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

---

## 这是什么？

一个 [OpenClaw](https://openclaw.ai) Agent Skill，统一管理飞书知识库、云盘和导航表。

它不只是一个文件管理器——它是一个**三层架构**的文档生命周期系统：

- 🌳 **Wiki 知识库**：按主题组织的树状目录，适合浏览和阅读
- 📁 **Drive 云盘**：按文件类型归档，方便批量操作和备份
- 📋 **Bitable 导航表**：全局索引，跨层检索，元数据管理

创建文档时自动归位三层，检索时一键跨层查找。

## 核心功能

### 📥 doc-sync — 创建即归位

创建新文档时自动完成三件事：
1. 移入 drive 对应文件夹（按文件类型）
2. 在 wiki 创建节点（按主题分类）
3. 在 bitable 导航表新增记录

根据文档标题关键词自动判断分类，无需手动选择。

### 📦 doc-archive — 按时间自动归档

- 晨报创建超过 7 天 → 归档
- 数据池/索引超过 14 天 → 归档
- 备份超过 30 天 → 归档
- 配置/指南/模板 → 不自动归档

归档操作在 wiki + drive + bitable 三层同步，标记 `📁归档` 状态。

### 💾 doc-backup — 定期备份

可配置备份清单，支持：
- 本地文件定期同步到飞书（MEMORY.md、配置文件等）
- 自定义备份频率（daily/weekly）
- 自动清理超过上限的旧备份
- 备份自动归位到 wiki + drive + bitable

### 🔍 doc-find — 全局检索

"帮我找xxx文档" → 搜索 bitable 索引 → wiki 节点 → 返回匹配结果。

支持：
- 按关键词搜索
- 按分类筛选
- 按标签检索
- 模糊匹配

### 📝 doc-template — 模板生成

内置 4 种模板：周报、会议纪要、项目复盘、技术方案。

"创建周报" → 自动填充日期 → 创建文档 → doc-sync 归位。

### 🧹 doc-tidy — 文档整理

发现并修复：
- 失效链接（bitable 记录指向已删文档）
- 未分类文档（自动判断分类）
- 孤儿文档（drive 中不在 bitable 里的）
- 空 wiki 页面

## 三层架构

```
┌─────────────────────────────────────────────────────┐
│              📋 Bitable 导航表（索引层）              │
│   全局索引：分类 / 标签 / 状态 / 链接 / 元数据       │
└──────────────────┬──────────────────────────────────┘
                   │ 双向同步
      ┌────────────┴────────────┐
      ▼                         ▼
┌───────────────┐      ┌───────────────┐
│ 🌳 Wiki       │      │ 📁 Drive      │
│ 知识树（主题） │      │ 归档层（类型） │
│               │      │               │
│ 📰 晨报存档   │      │ 01-系统管理   │
│ 🛠️ 系统运维   │      │ 02-系统备份   │
│ 🧠 记忆日志   │      │ 03-记忆备份   │
│ 📊 工作报告   │      │ 04-晨报数据   │
│ 📖 模板库     │      │ 归档/YYYY-MM  │
│ 📎 未分类     │      │               │
└───────────────┘      └───────────────┘
```

**为什么两层存储？**

Wiki 按主题组织——"晨报"和"配置指南"放不同分支，浏览体验好。
Drive 按类型组织——所有备份文件放一起，方便批量操作和清理。

同一个文档同时存在于两个视角，通过 bitable 索引关联。

## 自动分类规则

| 关键词 | 一级分类 | Drive 文件夹 |
|--------|---------|-------------|
| 晨报/新闻 | 📰 晨报数据 | 04-晨报数据 |
| 数据池/查重/索引 | 📰 晨报数据 | 04-晨报数据 |
| 配置/指南/教程 | 🛠️ 系统运维 | 01-系统管理 |
| 备份/快照 | 🛠️ 系统运维 | 02-系统备份 |
| MEMORY/记忆/日志 | 🧠 记忆日志 | 03-记忆备份 |
| 总结/报告/复盘 | 📊 工作报告 | 01-系统管理 |
| 模板 | 📖 模板 | 01-系统管理 |
| 其他 | 📎 未分类 | 文件合集 |

规则可自定义，编辑 `data/classification-rules.json`。

## 安装

### 从 ClawHub

```bash
clawhub install feishu-doc-manager
```

### 手动

```bash
git clone https://github.com/uuoov/feishu-doc-manager.git ~/.openclaw/workspace/skills/feishu-doc-manager
```

## 配置

### 前置依赖

| 依赖 | 说明 |
|------|------|
| **飞书应用** | 需要开启 wiki、doc、drive、bitable 权限 |
| **feishu_doc** | OpenClaw feishu channel 内置 |
| **feishu_wiki** | OpenClaw feishu channel 内置 |
| **feishu_drive** | OpenClaw feishu channel 内置 |

### 初始化

1. 编辑 `data/config.json`，填入你的 wiki spaceId、drive folder token、bitable appToken 等
2. 编辑 `data/backup-sources.json`，配置需要定期备份的本地文件
3. 编辑 `data/classification-rules.json`，自定义分类规则（可选）

### 首次运行

对 agent 说 **"初始化飞书文档管理系统"**，它会：
1. 在 wiki 中创建一级页面（晨报存档/系统运维/记忆日志/工作报告/模板库/未分类）
2. 为晨报存档创建当前月份子页面
3. 将现有 drive 文档同步到 wiki
4. 补全 bitable 中缺失的 wiki 链接

## 文件结构

```
feishu-doc-manager/
├── SKILL.md                      # 完整流程指引（agent 运行时读取）
├── README.md                     # 本文件
├── .gitignore
├── data/
│   ├── config.json               # 飞书 ID 配置（wiki/drive/bitable）
│   ├── backup-sources.json       # 备份源清单
│   ├── classification-rules.json # 自动分类规则
│   └── templates/                # 文档模板
│       ├── weekly-report.md      # 周报
│       ├── meeting-notes.md      # 会议纪要
│       ├── project-review.md     # 项目复盘
│       └── tech-proposal.md      # 技术方案
```

## 使用示例

```
你：帮我创建一个项目复盘文档
阿舟：→ 识别模板 → 填充内容 → 创建文档 → 三层归位 → 返回链接

你：帮我找晨报相关的文档
阿舟：→ 搜索 bitable → 返回分类列表

你：整理一下文档
阿舟：→ 扫描三层 → 发现问题 → 生成建议 → 确认后执行

你：备份 MEMORY.md
阿舟：→ 读取本地文件 → 创建飞书文档 → 三层归位 → 清理旧备份
```

## 与晨报系统集成

`morning-briefing` skill 创建每日晨报时，可调用本 skill 的 `doc-sync` 功能：
- 晨报自动归入 wiki/📰晨报存档/当月
- 晨报数据池自动归入 drive/04-晨报数据
- bitable 自动新增记录

## FAQ

**Q: 必须同时有 wiki + drive + bitable 吗？**
A: 不必须。只有 drive 也能用基础功能（归档、备份）。wiki 和 bitable 是增强功能，建议都配置。

**Q: 分类规则不够用怎么办？**
A: 编辑 `classification-rules.json`，添加新规则。关键词匹配是按顺序的，第一个匹配到的生效。

**Q: 可以自定义模板吗？**
A: 可以。在 `data/templates/` 目录下添加 `.md` 文件，用 `{变量名}` 标记动态字段。

**Q: 备份会占很多空间吗？**
A: 每个备份源有 `maxCopies` 上限，超出自动清理最旧的。MEMORY.md 每天备份保留 30 份，配置每周备份保留 12 份。

## 致谢

- [OpenClaw](https://openclaw.ai) — Agent 运行时
- [飞书开放平台](https://open.feishu.cn) — API 支持
- [ClawHub](https://clawhub.ai) — Skill 分发

## License

[MIT](LICENSE)
